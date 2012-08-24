@echo off
REM Il faut enregistrer sans BOM UTF-8

echo Conversion du fichier UI....
C:\Python27\Lib\site-packages\PyQt4\uic\pyuic.py interpolation.ui -o interpolation_ui.py
echo Fait !
pause