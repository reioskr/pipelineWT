# Create python file from UI Designer
import os


# Define the directory where the image is locateds
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths
path = os.path.join(script_dir, '..', 'ui_files')   

ui_import_path = os.path.join(path, 'ui_mainwindow.ui')
py_export_path = os.path.join(path, 'ui_mainwindow.py')

print(f"UI import path: {os.path.abspath(ui_import_path)}")
print(f"PY export path: {os.path.abspath(py_export_path)}")

os.system(f"pyuic5 -o {py_export_path} {ui_import_path}")


