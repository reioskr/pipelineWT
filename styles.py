# styles.py


dark = """
/* Dark Skin Style */
QMainWindow {
    background-color: #333333; /* Dark Gray */
}

QWidget#centralwidget {
    background-color: #333333; /* Dark Gray */
}

QLineEdit {
    background-color: #555555; /* Dark Gray */
    border: 1px solid #555555; /* Gray */
    color: #ffffff; /* White */
    border-radius: 4px;
}

QLineEdit:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QLineEdit:focus {
    border-color: #007bff; /* Blue */
}

/* Dark Skin Heading Style */
QLabel {
    color: #ffffff; /* White */
	font: 9pt "Segoe UI";
}

QDoubleSpinBox {
    background-color: #555555; /* Dark Gray */
    border: 1px solid #555555; /* Gray */
    color: #ffffff; /* White */
    border-radius: 4px;
}

QDoubleSpinBox:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QDoubleSpinBox:focus {
    border-color: #007bff; /* Blue */
}

QComboBox {
    background-color: #555555; /* Dark Gray */
    border: 1px solid #555555; /* Gray */
    color: #ffffff; /* White */
    border-radius: 4px;
}

QComboBox:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QComboBox:focus {
    border-color: #007bff; /* Blue */
}

QComboBox::drop-down {
    border: none;
    background-color: transparent;
}

QPushButton {
    background-color: #555555; /* Dark Gray */
    border: 2px solid #ffffff; /* White */
    color: #ffffff; /* White */
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    margin: 4px 2px;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #ffffff; /* White */
    color: #555555; /* Dark Gray */
}

QPushButton:pressed {
    background-color: #555555; /* Dark Gray */
    color: #ffffff; /* White */
}


QCheckBox {
    background-color: #333333;
    color: #ffffff; /* White */
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #555555;
}

QCheckBox::indicator:checked {
    color: #ffffff; /* White */
}

QFrame.Line {
    background-color: #555555; /* Dark Gray */
    height: 2px;
    margin: 10px 0;
}

QGroupBox {
    border: 1px solid #555555; /* Dark Gray border */
    border-radius: 6px;
    margin-top: 10px;
    background-color: #333333; /* Dark background */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 5px;
	font: 75 12pt "Segoe UI";
    color: #ffffff; /* White */
}

QStatusBar {
    background-color: #333333; /* Dark Gray */
    color: #ffffff; /* White */
}

QMenuBar {
    background-color: #333333; /* Dark Gray */
}

QMenuBar::item {
    background-color: transparent;
    color: #ffffff; /* White */
}

QMenuBar::item:selected {
    background-color: #555555; /* Medium Gray */
}

QToolBar {
    background-color: #333333; /* Dark Gray */
    color: #ffffff; /* White */
    border: none; /* Remove border */
}
"""


light = """
/* Light Skin Style */
QMainWindow {
    background-color: #f0f0f0; /* Very Light Gray */
}

QWidget#centralwidget {
    background-color: #f0f0f0; /* Very Light Gray */
}

QLineEdit {
    background-color: #e0e0e0; /* Light Gray */
    border: 1px solid #cccccc; /* Light Gray */
    color: #000000; /* Black */
    border-radius: 4px;
}

QLineEdit:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QLineEdit:focus {
    border-color: #007bff; /* Blue */
}

QLabel {
    color: #000000; /* Black */
	font: 9pt "Segoe UI";
}

QDoubleSpinBox {
    background-color: #e0e0e0; /* Very Light Gray */
    border: 1px solid #cccccc; /* Light Gray */
    color: #000000; /* Black */
    border-radius: 4px;
}

QDoubleSpinBox:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QDoubleSpinBox:focus {
    border-color: #007bff; /* Blue */
}

QComboBox {
    background-color: #e0e0e0; /* Very Light Gray */
    border: 1px solid #cccccc; /* Light Gray */
    color: #000000; /* Black */
    border-radius: 4px;
}

QComboBox:hover {
    border-color: #aaaaaa; /* Medium Gray */
}

QComboBox:focus {
    border-color: #cccccc; /* Blue */
}

QComboBox::drop-down {
    border: none;
    background-color: transparent;
}

QPushButton {
    background-color: #f0f0f0; /* Very Light Gray */
    border: 2px solid #555555; /* Dark Gray */
    color: #000000; /* Black */
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    margin: 4px 2px;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #555555; /* Dark Gray */
    color: #f0f0f0; /* Very Light Gray */
}

QPushButton:pressed {
    background-color: #f0f0f0; /* Very Light Gray */
    color: #555555; /* Dark Gray */
}


QCheckBox {
    background-color: #f0f0f0;
    color: #000000; /* White */
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #e0e0e0;
}

QCheckBox::indicator:checked {
    color: #ffffff; /* White */
}
QFrame.Line {
    background-color: #cccccc; /* Light Gray */
    height: 2px;
    margin: 10px 0;
}

QGroupBox {
    border: 1px solid #cccccc; /* Light Gray border */
    border-radius: 6px;
    margin-top: 10px;
    background-color: #f0f0f0; /* Very Light Gray */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 5px;
	font: 75 12pt "Segoe UI";
    color: #333333; /* Dark Gray */
}

QStatusBar {
    background-color: #f0f0f0; /* Light Gray */
    color: #333333; /* Dark Gray */
}

QMenuBar {
    background-color: #f0f0f0; /* Light Gray */
}

QMenuBar::item {
    background-color: transparent;
    color: #333333; /* Dark Gray */
}

QMenuBar::item:selected {
    background-color: #cccccc; /* Light Gray */
}

QToolBar {
    background-color: #f0f0f0; /* Light Gray */
    color: #333333; /* Dark Gray */
    border: none; /* Remove border */
}
"""