import os
from PIL import Image
import base64

def convert_image_to_icon():
    """
    Converts an image to an icon file and saves it in different sizes.
    Also converts the icon file to a base64 string and writes it to a Python script as PyInstaller does
    not to consider the external files for taskbar/window icon.
    """
    # Define the directory where the image is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the paths
    path = os.path.join(script_dir, '..', 'resources', 'icons')

    import_file = os.path.join(path, 'fullsize.jpg')
    export_file = os.path.join(path, 'app.ico')
    export_base64 = os.path.join(path, '64px.ico')
    icon_base64_file = os.path.join(path, 'icon_base64.py')

    # Open the image file
    img = Image.open(import_file)

    # Save the image as an icon file in different sizes
    img.save(export_file, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])

    img.save(export_base64, format='ICO', sizes=[(128,128)]) # title bar / taskbar icon


    # Read the icon file and convert it to base64
    with open(export_base64, 'rb') as icon_file:
        icon_data = icon_file.read()
        icon_base64 = base64.b64encode(icon_data)

    # Write the base64 string to a Python script
    with open(icon_base64_file, 'w') as python_file:
        python_file.write('icon_base64 = """{}"""'.format(icon_base64.decode('utf-8')))

# Call the function to convert the image to an icon
convert_image_to_icon()
