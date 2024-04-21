echo off

set arg1=%1
set arg2=%2
set arg3=%3

venv\Scripts\activate
python run.py %arg1% %arg2% %arg3%