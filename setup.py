from cx_Freeze import setup, Executable

setup(name="Vesim's Object Tracking and Detection Software", description="Object tracking and detection.", executables=[Executable("opencv.py")])
