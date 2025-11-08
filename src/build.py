import PyInstaller.__main__
import os
import shutil

APP_NAME = "py-phonk"
ICON_PATH = "icon.ico" if os.path.exists("icon.ico") else None

params = [
    "main.py", 
    "--name", APP_NAME,    
    "--onefile",           
    "--windowed",          
    "--noconsole",         
    "--clean",
    "--icon", ICON_PATH if ICON_PATH else "NONE",
    "--distpath", "dist"   
]

PyInstaller.__main__.run(params)
print(f"\n{APP_NAME} package in dist")
