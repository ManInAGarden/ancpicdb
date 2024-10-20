rem batch to build the distributable version for ms-windows
echo off
call conda activate ancpicdb
echo writing external libs to cache for use in about ancpicdb ...
python create_dependcydb.py
echo ... done
pyinstaller -w --noconfirm --name AncPicDb ^
    --add-data ./AncPicDbWindows.conf:. ^
    --add-data ./seeds:./seeds ^
    --add-data ./ressources:./ressources ^
    --icon ./ressources/application.ico ^
    AncPicDbMain.py
call conda deactivate
pause
