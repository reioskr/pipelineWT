pip freeze > requirements.txt
pyinstaller --clean --onefile --name PipelineWallThickness --windowed --noconsole --icon=resources\icons\app.ico --version-file=version.txt main.py

pause