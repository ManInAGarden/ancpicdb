rem batch to build the distributable version for ms-windows
echo off
call conda activate ancpicdb
echo writing external libst to cache fur use in about pexdb ...
python create_dependcydb.py
echo ... done
pyinstaller -w --noconfirm --name AncPicDb ^
    --hidden-import "sklearn.utils._typedefs" ^
    --add-data ./AncPicDbWINDIST.conf;. ^
    --add-data ./seeds;./seeds ^
    --add-data ./ressources;./ressources ^
    --icon ./ressources/application.ico ^
    AncPicDbMain.py
call conda deactivate
pause
