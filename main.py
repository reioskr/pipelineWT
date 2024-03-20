import os
import sys
from PyQt5 import QtWidgets
from ui_mainwindow import Ui_MainWindow
from backend import * 

from PyQt5.QtGui import QDoubleValidator, QColor, QPalette, QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt#, QFile, QTextStream, QSize
from functools import partial


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parameters = parameters
        self.config = config
        
        self.setupUI_graphics()
        #self.setStyleSheet(self.load_stylesheet())
        self.init_ui_dict()
        self.set_input_parameters()
        self.connect_ui_signals()
        self.set_numeric_validators()

    def init_ui_dict(self):
        """
        Initializes a dictionary of line edit UI elements.
        Key: line edit object name
        Value:  (1) parameter name in local dictionary
                (2) unit conversion factor

        Returns:
            None
        """
        self.line_edit_mapping = {
            "le_P_design": ("P_design", Barg_to_MPa),
            "le_P_min": ("P_min", Barg_to_MPa),
            "le_P_test": ("P_test", Barg_to_MPa),
            "le_ref_el_design_pressure": ("ref_el_design_pressure", 1),
            "le_ref_el_min_pressure": ("ref_el_min_pressure", 1),
            "le_ref_el_test_pressure": ("ref_el_test_pressure", 1),
            "le_D": ("OD", 1),
            "le_t_cor": ("t_cor", 1),
            "le_t_tol": ("t_tol", 1),
            # "le_t_bendthin": ("t_bendthin", 1),
            "le_alpha_fab": ("alpha_fab", 1),
            "le_alpha_gw": ("alpha_gw", 1),
            "le_fo": ("fo", percent_to_fraction),
            "le_SMYS": ("SMYS", 1),
            "le_SMTS": ("SMTS", 1),
            "le_fytemp": ("fytemp", 1),
            "le_futemp": ("futemp", 1),
            "le_E": ("E", GPa_to_Pa),
            "le_nu": ("nu", 1),
            "le_rho_design": ("rho_design", 1),
            "le_rho_test": ("rho_test", 1),
            "le_rho_min": ("rho_min", 1),
            "le_rho_ext": ("rho_ext", 1),
            "le_water_depth": ("water_depth", 1),
            "le_max_elevation": ("max_elevation", 1),
            "le_min_elevation": ("min_elevation", 1)
        }
        
        self.double_spin_box_mapping = {
             "le_t": ("t", 1)
        }
        
        self.checkbox_mapping = {
            "cb_AddMaterialReq": ("AddMaterialReq",),
            "cb_PressureContainment_operational_enable_corrosion": ("Pressure containment", "operational", "enable_corrosion"),
            "cb_PressureContainment_operational_enable_derating": ("Pressure containment", "operational", "enable_derating"),
            "cb_PressureContainment_systemtest_enable_corrosion": ("Pressure containment", "system test", "enable_corrosion"),
            "cb_PressureContainment_systemtest_enable_derating": ("Pressure containment", "system test", "enable_derating")
            #"cb_Collapse_default_enable_corrosion": ("Collapse", "default", "enable_corrosion"),
            #"cb_Collapse_default_enable_derating": ("Collapse", "default", "enable_derating"),
            #"cb_PropagatingBuckling_default_enable_corrosion": ("Propagating buckling", "default", "enable_corrosion"),
            #"cb_PropagatingBuckling_default_enable_derating": ("Propagating buckling", "default", "enable_derating")
        }

        self.combo_box_mapping = {
            "cmb_ID_OD_selection": ["is_OD"],
            "cmb_DNV_material_selection": ["DNV_material_selection"],
            
            "cmb_PressureContainment_operational_safety_class": ["Pressure containment", "operational", "safety_class"],
            "cmb_PressureContainment_systemtest_safety_class": ["Pressure containment", "system test", "safety_class"],
            #"cmb_Collapse_default_safety_class": ["Collapse", "default", "safety_class"],
            #"cmb_PropagatingBuckling_default_safety_class": ["Propagating buckling", "default", "safety_class"],
        }
        
    def set_numeric_validators(self):
        """
        Sets a QDoubleValidator for each numeric input field.
        This method creates a QDoubleValidator object and sets it as the validator for each numeric input field
        in the line_edit_ui_elements dictionary.
        """
        validator = QDoubleValidator()
        
        # Set the validator for each numeric input field
        for key, value in self.line_edit_mapping.items():
            line_edit = getattr(self.ui, key)
            line_edit.setValidator(validator)

    @staticmethod
    def is_valid_float(text):
        """
        Check if the text represents a valid floating-point number.
        """
        # Remove the first occurrence of '.' and leading '-' if present, then check if the remaining string is a digit
        cleaned_text = text.replace('.', '', 1).lstrip('-')
        return cleaned_text.isdigit()

    def setupUI_graphics(self):
        # Add icon
        icon_name = "resources/icons/32px.png"
        self.app_icon = QIcon(icon_name)
        self.app_icon.addFile("resources/icons/16px.png")  # Add 16x16 icon size
        self.app_icon.addFile("resources/icons/32px.png")  # Add 32x32 icon size
        self.setWindowIcon(QIcon(icon_name))
        
        # Check if the icon is loaded successfully
        if self.app_icon.isNull():
            print("Failed to load the application icon.")
        else:
            print("Application icon loaded successfully.")

    def update_parameter(self, line_edit, name, unit, text):
        if MyMainWindow.is_valid_float(text):
            self.parameters.__setitem__(name, float(text) * unit)
            line_edit.setStyleSheet("")  # Reset stylesheet to default if input is valid
            self.ui.pushButton.setDisabled(False)
            self.ui.pushButton.setStatusTip(self.original_status_tip)
        else:
            line_edit.setStyleSheet("background-color: red;")  # Change background color to red if input is not valid
            self.ui.pushButton.setDisabled(True)
            self.original_status_tip = self.ui.pushButton.statusTip()
            self.ui.pushButton.setStatusTip("Errors in input fields. Please correct the errors before proceeding.")
            
    def connect_ui_signals(self):
        """
        Connects the valueChanged signal of each UI element to update the corresponding variables and configurations.

        LineEdits:
        - Connects and checks if the input is a valid float.

        CheckBoxes:
        - Connects the stateChanged signal of the checkboxes to update the corresponding configuration values.

        ComboBoxes:
        - Connects the currentIndexChanged signal of the combo boxes to update the corresponding configuration values.

        To be implemented:
        - DNV dropdown material selection combo box.
        - ID or OD selection combo box.
        - validity checks for input values (e.g. negative OD etc)

        """


        # LineEdits, connect and check if input is valid float:
        for key, value in self.line_edit_mapping.items():
            line_edit = getattr(self.ui, key)
            parameter_name = value[0]
            unitfix = value[1]
            
            callback = partial(
                lambda line_edit, name, unit, text: self.update_parameter(line_edit, name, unit, text),
                line_edit,
                parameter_name,
                unitfix
            )
            
            line_edit.textChanged.connect(callback)
              
        # DoubleSpinBoxes:
        for key, value in self.double_spin_box_mapping.items():
            double_spin_box = getattr(self.ui, key)
            
            callback = partial(
                lambda box, name, unit, number: self.parameters.__setitem__(name, box.value() * unit),
                double_spin_box,
                value[0],
                value[1]
            )
            double_spin_box.textChanged.connect(callback)        
        
        # CheckBoxes:
        for checkbox_key, config_keys in self.checkbox_mapping.items():
            checkbox = getattr(self.ui, checkbox_key)
            if len(config_keys) == 1:  # Configuration key is at the root level
                config_option = config_keys[0]
                callback = partial(lambda state, option: self.config.update({option: state == QtCore.Qt.Checked}), option=config_option)
                checkbox.stateChanged.connect(callback)
            elif len(config_keys) == 2:  # Configuration key is at the second level
                config_section, config_option = config_keys
                callback = partial(lambda state, section, option: self.config[section].update({option: state == QtCore.Qt.Checked}), section=config_section, option=config_option)
                checkbox.stateChanged.connect(callback)
            else:  # Configuration key is nested within sections and subsections
                config_section, config_subsection, config_option = config_keys
                callback = partial(lambda state, section, subsection, option: self.config[section][subsection].update({option: state == QtCore.Qt.Checked}), section=config_section, subsection=config_subsection, option=config_option)
                checkbox.stateChanged.connect(callback)

        # ComboBoxes:
        for key, value in self.combo_box_mapping.items():
            combo_box = getattr(self.ui, key)
            callback = partial(lambda combo_box, keys, index: self.config[keys[0]][keys[1]].update({keys[2]: combo_box.currentText()}), combo_box, value)
            combo_box.currentIndexChanged.connect(callback)        

        # To be implemented:
        # For DNV dropdown material selection combo box
        # self.ui.cmb_DNV_material_selection.currentIndexChanged.connect(lambda index: self.ACTION: self.ui.cmb_DNV_material_selection.currentText()}))
        # For ID or OD selection combo box
        # self.ui.cmb_ID_OD_selection.currentIndexChanged.connect(lambda index: self.ACTION: self.ui.cmb_ID_OD_selection.currentText()}))

        # input validity checks
        
    def is_it_ID_or_OD(self):
        pass
        
    def set_input_parameters(self):
        """
        Sets the input parameters in the UI based on the values stored in the `parameters` and `config` dictionaries.
        This method inserts default parameters to the UI LineEdits and sets default values for comboboxes and checkboxes.
        """
        
        # LineEdits:
        for key, value in self.line_edit_mapping.items():
            line_edit = getattr(self.ui, key)
            parameter_name = value[0]
            unitfix = value[1]

            if parameter_name not in self.parameters:
                raise KeyError(f"Key '{parameter_name}' not found in parameters")

            parameter_value = self.parameters.get(parameter_name, "")
            line_edit.setText(str(parameter_value / unitfix))  # opposite unit conversion here

        # DoubleSpinBoxes:
        for key, value in self.double_spin_box_mapping.items():
            double_spin_box = getattr(self.ui, key)
            parameter_name = value[0]
            unitfix = value[1]

            if parameter_name not in self.parameters:
                raise KeyError(f"Key '{parameter_name}' not found in parameters")

            parameter_value = self.parameters.get(parameter_name, "")
            double_spin_box.setValue(float(parameter_value / unitfix))  # opposite unit conversion here

        # CheckBoxes:
        for key, value in self.checkbox_mapping.items():
            checkbox = getattr(self.ui, key)
            config_value = self.config
            for config_key in value:
                if config_key not in config_value:
                    raise KeyError(f"Key '{config_key}' not found in configuration")
                config_value = config_value[config_key]
            if not isinstance(config_value, bool):
                raise TypeError(f"Expected a boolean, but got {type(config_value).__name__}")
            checkbox.setChecked(config_value)
              
        # Comboboxes:
        for key, value in self.combo_box_mapping.items():
            combo_box = getattr(self.ui, key)
            config_value = self.config
            for config_key in value:
                if config_key not in config_value:
                    raise KeyError(f"Key '{config_key}' not found in configuration")
                config_value = config_value[config_key]
            combo_box.setCurrentText(str(config_value))
    


    def read_UI_input_values(self):
        """
        Reads the input values from the UI elements and updates the corresponding parameters.
        """
            # LineEdits:
        for key, value in self.line_edit_mapping.items():
            line_edit = getattr(self.ui, key)
            parameter_name = value[0]
            unitfix = value[1]
            text = line_edit.text()
            if MyMainWindow.is_valid_float(text):
                self.parameters[parameter_name] = float(text) * unitfix
            else:
                line_edit.setStyleSheet("background-color: red;")
                print(f"Invalid input: {text}")

        # DoubleSpinBoxes:
        for key, value in self.double_spin_box_mapping.items():
            spin_box = getattr(self.ui, key)
            parameter_name = value[0]
            self.parameters[parameter_name] = spin_box.value()

        # CheckBoxes:
        for key, value in self.checkbox_mapping.items():
            checkbox = getattr(self.ui, key)
            parameter_name = value[0]
            self.parameters[parameter_name] = checkbox.isChecked()

        # ComboBoxes:
        for key, value in self.combo_box_mapping.items():
            combo_box = getattr(self.ui, key)
            parameter_name = value[0]
            self.parameters[parameter_name] = combo_box.currentText()



    def on_button_clicked(self):
        
        self.read_UI_input_values() # Update the parameters with the values from the line edits (failsafe in case the user doesn't click out of the line edit before clicking the button)
        
        burst_operational = BurstCriterion(self.parameters,self.config, "operational")
        print_dict(self.parameters)
        print_dict(burst_operational.parameters)
        burst_operational.run()
        #self.ui.lbl_UR_PressureContainment_operation.setText(f"<b>{burst_operational.utilisation:.3f}</b>")
        #self.ui.lbl_minWT_PressureContainment_operation.setText(f"{burst_operational.min_wt:.2f}")
        self.ui.lbl_UR_PressureContainment_operation.setText(f"<b>{burst_operational.utilisation_dnv:.3f}</b>")
        self.ui.lbl_minWT_PressureContainment_operation.setText(f"{burst_operational.min_wt_dnv:.2f}")
        
        burst_test = BurstCriterion(self.parameters,self.config, "system test")
        burst_test.run()
        #self.ui.lbl_UR_PressureContainment_test.setText(f"<b>{burst_test.utilisation:.3f}</b>")
        #self.ui.lbl_minWT_PressureContainment_test.setText(f"{burst_test.min_wt:.2f}")
        self.ui.lbl_UR_PressureContainment_test.setText(f"<b>{burst_test.utilisation_dnv:.3f}</b>")
        self.ui.lbl_minWT_PressureContainment_test.setText(f"{burst_test.min_wt_dnv:.2f}")
        
        print("Burst Verification Completed")


        
    @classmethod
    def set_dark_ui_scheme(cls, app):
        # Apply dark mode stylesheet
        app.setStyle('Fusion')

        dark_mode_stylesheet = """
        /* Base background color for all widgets */
        QWidget {
            background-color: #333333;
            color: #FFFFFF;
        }

        /* Background color for input fields */
        QLineEdit {
            background-color: #555555;
        }
        
        QSpinBox {
            background-color: #555555; 
        }

        QDoubleSpinBox {
            background-color: #555555; 
        }

        /* Background color for buttons */
        QPushButton {
            background-color: #555555;
            border: none;
            padding: 5px 10px;
        }

        /* Background color for combobox */
        QComboBox {
            background-color: #555555;
            color: #FFFFFF;
            selection-background-color: #666666;
        }

        /* Background color for checkboxes */
        QCheckBox {
            color: #FFFFFF;
        }

        /* Background color for radio buttons */
        QRadioButton {
            color: #FFFFFF;
        }

        /* Background color for labels */
        QLabel {
            color: #FFFFFF;
        }

        /* Background color for scrollbars */
        QScrollBar {
            background-color: #555555;
        }

        /* Background color for tab widget */
        QTabWidget::pane {
            background-color: #555555;
        }

        /* Background color for tab bar */
        QTabBar::tab {
            background-color: #666666;
            color: #FFFFFF;
        }

        /* Background color for selected tab */
        QTabBar::tab:selected {
            background-color: #777777;
        }

        /* Background color for disabled widgets */
        QWidget[enabled="false"] {
            background-color: #444444;
            color: #888888;
        }
        
        /* Push Buttons */
        QPushButton {
            background-color: #555;
            color: #eee;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }

        """

        # Apply dark mode stylesheet
        app.setStyleSheet(dark_mode_stylesheet)
        # Set dark mode color palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(70,70,70))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)


def main():
    app = QtWidgets.QApplication(sys.argv)

    MyMainWindow.set_dark_ui_scheme(app)
    
    window = MyMainWindow()
    window.ui.pushButton.clicked.connect(window.on_button_clicked)  # Connect the button click event to a method in MyMainWindow
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()