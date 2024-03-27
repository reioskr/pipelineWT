# Create python file from UI Designer
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
ui_file_path = os.path.join(script_dir, 'ui_files', 'ui_mainwindow_new.ui')
os.system(f"pyuic5 -o {os.path.join(script_dir, 'ui_mainwindow.py')} {ui_file_path}")


