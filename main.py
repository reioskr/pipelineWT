import os
import sys
from styles import *

from PyQt5 import QtWidgets
from ui_mainwindow import Ui_MainWindow
from backend import * 

from PyQt5.QtGui import QDoubleValidator, QColor, QPalette, QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt#, QFile, QTextStream, QSize
from functools import partial
from PyQt5.QtWidgets import QMessageBox, QFileDialog


import locale
import configparser


'''
minWT is incorrect when have ID selected. (does not give UR 1.00 when input the minWT). Investigate.
'''

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.load_settings()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parameters = parameters
        self.config = config
        
        self.get_locale_info()
        self.setupUI_graphics()
        self.init_ui_dict()
        self.save_original_button_status_tips()
        self.set_init_input_parameters()
        self.connect_ui_signals()

    def init_ui_dict(self):
        """
        Initializes a dictionary of line edit UI elements.
        Key: UI line edit object name
        Value:  (1) parameter name in local dictionary
                (2) unit conversion factor
                (3) QDoubleValidator object

        Returns:
            None
        """
        self.line_edit_mapping = {
            "le_P_design": ("P_design", Barg_to_MPa, QDoubleValidator(0, float('inf'), 10)),
            "le_P_min": ("P_min", Barg_to_MPa, QDoubleValidator(0, float('inf'), 10)),
            "le_P_test": ("P_test", Barg_to_MPa, QDoubleValidator(0, float('inf'), 10)),
            "le_ref_el_design_pressure": ("ref_el_design_pressure", 1, QDoubleValidator(-float('inf'), float('inf'), 10)),
            "le_ref_el_min_pressure": ("ref_el_min_pressure", 1, QDoubleValidator(-float('inf'), float('inf'), 10)),
            "le_ref_el_test_pressure": ("ref_el_test_pressure", 1, QDoubleValidator(-float('inf'), float('inf'), 10)),
            "le_D": ("D", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_t_cor": ("t_cor", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_t_fab": ("t_fab", 1, QDoubleValidator(0, float('inf'), 10)),
            # "le_t_bendthin": ("t_bendthin", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_alpha_fab": ("alpha_fab", 1, QDoubleValidator(0, 1, 10)),
            "le_alpha_gw": ("alpha_gw", 1, QDoubleValidator(0, 1, 10)),
            "le_fo": ("fo", percent_to_fraction, QDoubleValidator(0, 100, 10)),
            "le_SMYS": ("SMYS", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_SMTS": ("SMTS", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_fytemp": ("fytemp", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_futemp": ("futemp", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_E": ("E", GPa_to_Pa, QDoubleValidator(0, float('inf'), 10)),
            "le_nu": ("nu", 1, QDoubleValidator(0, 1, 10)),
            "le_rho_design": ("rho_design", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_rho_test": ("rho_test", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_rho_min": ("rho_min", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_rho_ext": ("rho_ext", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_water_depth": ("water_depth", 1, QDoubleValidator(0, float('inf'), 10)),
            "le_max_elevation": ("max_elevation", 1, QDoubleValidator(-float('inf'), float('inf'), 10)),
            "le_min_elevation": ("min_elevation", 1, QDoubleValidator(-float('inf'), float('inf'), 10))
        }
        
        self.double_spin_box_mapping = {
            "le_t": ("t", 1)
        }
        
        self.checkbox_mapping = {
            "cb_AddMaterialReq": ("AddMaterialReq",),
            "cb_PressureContainment_operational_enable_corrosion": ("Pressure containment", "operational", "enable_corrosion"),
            "cb_PressureContainment_operational_enable_derating": ("Pressure containment", "operational", "derating_enabled"),
            "cb_PressureContainment_systemtest_enable_corrosion": ("Pressure containment", "system test", "enable_corrosion"),
            "cb_PressureContainment_systemtest_enable_derating": ("Pressure containment", "system test", "derating_enabled")
            #"cb_Collapse_default_enable_corrosion": ("Collapse", "default", "enable_corrosion"),
            #"cb_Collapse_default_derating_enabled": ("Collapse", "default", "derating_enabled"),
            #"cb_PropagatingBuckling_default_enable_corrosion": ("Propagating buckling", "default", "enable_corrosion"),
            #"cb_PropagatingBuckling_default_derating_enabled": ("Propagating buckling", "default", "derating_enabled")
        }

        self.combo_box_mapping = {
            "cmb_ID_OD_selection": ["diameter_type"],
            "cmb_DNV_material_selection": ["DNV_material_selection"],
            
            "cmb_PressureContainment_operational_safety_class": ["Pressure containment", "operational", "safety_class"],
            "cmb_PressureContainment_systemtest_safety_class": ["Pressure containment", "system test", "safety_class"],
            #"cmb_Collapse_default_safety_class": ["Collapse", "default", "safety_class"],
            #"cmb_PropagatingBuckling_default_safety_class": ["Propagating buckling", "default", "safety_class"],
        }
    
    def get_locale_info(self):
        """
        Gets the locale information0 for the application.

        This method retrieves decimal separator convention from Windows locale setting to be used in the UI for the input.
        """
        locale.setlocale(locale.LC_ALL, '')
        self.decimal_point = locale.localeconv()['decimal_point']
    
    @classmethod
    def load_settings(cls):
        """
        Reads the settings from the settings.ini file.
        """
        cls.settings = configparser.ConfigParser()
        cls.settings.read('settings.ini')

    @classmethod
    def save_settings(cls):
        with open('settings.ini', 'w') as configfile:
            cls.settings.write(configfile)
        
    @staticmethod
    def is_valid_float(text):
        """
        Check if the text represents a valid floating-point number.
        """
        # Remove the first occurrence of '.' and leading '-' if present, then check if the remaining string is a digit
        cleaned_text = text.replace(',', '.').replace('.', '', 1).lstrip('-')
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

    def save_original_button_status_tips(self):
        """
        Updates the parameter value based on the input from the line edit.
        """
        self.original_pushButton_status_tip = self.ui.pushButton.statusTip()
        
    def update_parameter(self, line_edit, name, unit, text):
        if line_edit.hasAcceptableInput() and self.is_valid_float(text):
            line_edit.setStyleSheet("")  # Reset stylesheet to default if input is valid
            self.ui.pushButton.setDisabled(False)
            self.ui.pushButton.setStatusTip(self.original_pushButton_status_tip)
        else:
            line_edit.setStyleSheet("background-color: red;")  # Change background color to red if input is not valid
            self.ui.pushButton.setDisabled(True)
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
            validator = value[2]  # Get the validator from the dictionary
            line_edit.setValidator(validator) # Set the validator
    
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
            callback = partial(
                lambda combo_box, keys, index: 
                    self.config.update({keys[0]: combo_box.currentText()})
                    if len(keys) == 1 # If only one key is in dict, update the root level configuration
                    else self.config[keys[0]].update({keys[1]: combo_box.currentText()})
                    if len(keys) == 2 # If two keys are provided (nested dict), update the second level configuration
                    else self.config[keys[0]][keys[1]].update({keys[2]: combo_box.currentText()}),  # 3rd level nested dict
                combo_box, 
                value
            )
            combo_box.currentIndexChanged.connect(callback)        

        # Menu actions:
        self.ui.actionMenuOpen.triggered.connect(self.open_file_dialog)
        self.ui.actionMenuSave.triggered.connect(self.save_file_dialog)
        self.ui.actionMenuExit.triggered.connect(self.close)

        # Toolbar actions:
        self.ui.actionOpen.triggered.connect(self.open_file_dialog)
        self.ui.actionSave.triggered.connect(self.save_file_dialog)


        self.ui.actionThemeDark.triggered.connect(lambda: (MyMainWindow.set_settings('DEFAULT', 'Theme', 'dark'), self.update_ui_theme('dark')))
        self.ui.actionThemeLight.triggered.connect(lambda: (MyMainWindow.set_settings('DEFAULT', 'Theme', 'light'), self.update_ui_theme('light')))
        
        # To be implemented:
        # For DNV dropdown material selection combo box
        # self.ui.cmb_DNV_material_selection.currentIndexChanged.connect(lambda index: self.ACTION: self.ui.cmb_DNV_material_selection.currentText()}))
        
    def calculate_outer_diameter(self):
        if self.parameters["diameter_type"] == "OD [mm]":
            self.parameters["OD"] = self.parameters["D"]
        elif self.parameters["diameter_type"] == "ID [mm]":
            self.parameters["OD"] = self.parameters["D"] + 2 * self.parameters["t"]
        else:
            raise ValueError("Invalid diameter type")
        
        
    def check_OD_t_t_cor_t_fab_t_bendthin(self):
        OD = self.parameters["OD"]
        t = self.parameters["t"]
        t_bendthin_mm = self.parameters["t_bendthin"]
        t_fab_mm = self.parameters["t_fab"]
        t_cor_mm = self.parameters["t_cor"]
        
        if t < t_cor_mm + t_fab_mm + t_bendthin_mm:
            return self.show_warning("Calculated wall thickness is below zero.", "Please verify the input parameters:\n    • t\n    • t_cor\n    • t_fab")

        if OD < 2 * (t + t_fab_mm):
            return self.show_warning("Calculated ID is below zero.", "Please verify the input parameters:\n    • OD or ID\n    • t\n    • t_fab")        
        
        return True # Return True if checks are OK
                
    def show_warning(self, message, informative_text):
        """
        Display a warning message box with the given message and informative text.

        Args:
            message (str): The main message to be displayed in the warning box.
            informative_text (str): Additional text providing more information about the warning.

        Returns:
            bool: False indicating that the warning was shown.
        """
        print(message)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle("Warning")
        msg.setWindowIcon(self.windowIcon())  # Use the same icon as the main app
        msg.exec_()
        return False
         
    def set_init_input_parameters(self):
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
            parameter_value_str = str(parameter_value / unitfix)  # opposite unit conversion here

            # Replace the dot with a comma if windows locale is set to a comma
            if self.decimal_point == ',':
                parameter_value_str = parameter_value_str.replace('.', ',')

            line_edit.setText(parameter_value_str)
        
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
                self.parameters[parameter_name] = float(text.replace(',', '.')) * unitfix
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


    def on_button_clicked_general(self):
        """
        This method is called when any button is clicked. It performs the following actions:
        1. Updates the parameters with the values from the line edits.
        2. Calculates the outer diameter based on the selected input diameter type.
        3. Checks if the reduced wall thickness is above zero.

        Returns:
        bool: True if the reduced wall thickness is above zero, False otherwise.
        """
        self.read_UI_input_values() # Update the parameters with the values from the line edits (failsafe in case the user doesn't click out of the line edit before clicking the button)
        self.calculate_outer_diameter() # Calculate the outer diameter based on the selected diameter type
        return self.check_OD_t_t_cor_t_fab_t_bendthin() # Check if the reduced wall thickness is above zero
        

    def on_button_clicked_calculate_pressure_containment(self):
        
        if self.on_button_clicked_general(): # Proceed only if returns true
            burst_operational = BurstCriterion(self.parameters, self.config, "operational")
            self.update_ui(burst_operational, "operational")

            burst_test = BurstCriterion(self.parameters, self.config, "system test")
            self.update_ui(burst_test, "systemtest")
            print("Burst Verification Completed")

    def update_ui(self, burst, prefix):
        burst.run()
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_UR').setText(f"<b>{burst.Utility:.3f}</b>")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_minWT').setText(f"{burst.min_wt:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_fy').setText(f"{burst.fy:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_fu').setText(f"{burst.fu:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_t').setText(f"{burst.t_code:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_pb').setText(f"{burst.p_b:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_gammaM').setText(f"{burst.gamma_m:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_gammaSC').setText(f"{burst.gamma_sc:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_Pld').setText(f"{burst.Pld:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_Plx').setText(f"{burst.Pl_it:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_Pe').setText(f"{burst.Pe:.2f}")
        getattr(self.ui, f'lbl_PressureContainment_{prefix}_PlxPe').setText(f"{burst.Pl_it_Pe:.2f}")


    @classmethod
    def set_ui_scheme(cls, app):
        app.setStyle('Fusion')
        
        # Select the desired stylesheet        
        theme = cls.settings.get('DEFAULT', 'Theme', fallback='light')  # 'light' is the default theme
        cls.update_ui_theme(app, theme)
        
    @classmethod
    def set_settings(cls, section, option, value):
        cls.settings.set(section, option, value)
        cls.save_settings()

    def update_ui_theme(app, theme):
        """MyMainWindow.set_ui_scheme
        Updates the UI theme based on the selected theme from the UI.
        """
        
        if theme == 'dark':
            app.setStyleSheet(dark)
        else:
            app.setStyleSheet(light)
            
    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Case", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)
                self.parameters = data.get('parameters', {})
                self.config = data.get('config', {})
                print("Loaded: ", file_name)
                self.set_init_input_parameters()
                self.on_button_clicked_calculate_pressure_containment() # Rerun the calculations with imported input (alternatively could load the results from json)

                
    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Case", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                data = {'parameters': self.parameters, 'config': self.config}
                json.dump(data, f, indent=4, sort_keys=False) 
                print("Saved: ", file_name)                
                    
                    
        
def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MyMainWindow()

    window.ui.pushButton.clicked.connect(window.on_button_clicked_calculate_pressure_containment)  # Connect the button click event to a method in MyMainWindow
    MyMainWindow.set_ui_scheme(app)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


"""
def save_to_excel(data, file_path):
    with pd.ExcelWriter(file_path) as writer:
        df_factors = pd.DataFrame(data["factors"])
        df_factors.to_excel(writer, sheet_name="factors", index=False)
        
        df_config = pd.DataFrame(data["config"])
        df_config.to_excel(writer, sheet_name="config", index=False)
        
        df_parameters = pd.DataFrame(data["parameters"])
        df_parameters.to_excel(writer, sheet_name="parameters", index=False)

def read_from_excel(file_path):
    with pd.ExcelFile(file_path) as xls:
        data = {}
        data["factors"] = pd.read_excel(xls, sheet_name="factors").to_dict(orient='records')
        data["config"] = pd.read_excel(xls, sheet_name="config").to_dict(orient='records')
        data["parameters"] = pd.read_excel(xls, sheet_name="parameters").to_dict(orient='records')
        return data

# Example usage:
data = {
    "factors": factors,
    "config": config,
    "parameters": parameters
}

save_to_excel(data, 'data.xlsx')

data_from_excel = read_from_excel('data.xlsx')
factors_from_excel = data_from_excel["factors"]
config_from_excel = data_from_excel["config"]
parameters_from_excel = data_from_excel["parameters"]
"""