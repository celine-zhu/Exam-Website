@ECHO OFF
SET _TMPOutput=TMPOutput.txt
SET _TMPOutput2=TMPOutput2.txt
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

FOR /F "tokens=* USEBACKQ" %%F IN (`where python`) DO (
    ECHO %%F >> %_TMPOutput%
)

IF NOT EXIST %_TMPOutput% goto FullSearch

FOR /F "tokens=* USEBACKQ" %%F IN (`findstr Python %_TMPOutput%`) DO (
    ECHO %%F >> %_TMPOutput2%   
)

IF NOT EXIST %_TMPOutput2% goto FullSearch

::check if a python version is already in the path
FOR /F "tokens=* USEBACKQ" %%F IN (%_TMPOutput2%) DO (
    SET _PythonPath=%%F
    %_PythonPath% --version > %_TMPOutput%
    for /f "tokens=*" %%s in (%_TMPOutput%) do (
        SET _PythonInfo=%%s
        IF %_PythonInfo:~7,3%==3.8 goto InstallDependancy
        IF %_PythonInfo:~7,3%==3.9 goto InstallDependancy
    )   
)

:FullSearch
ECHO python not found in environnement path
::If not found, we check in the entire repository of the user
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%
FOR /F "tokens=* USEBACKQ" %%F IN (`where /R C:\Users\%username% python`) DO (
    ECHO %%F >> %_TMPOutput%
)

IF NOT EXIST %_TMPOutput% goto InstallPython

FOR /F "tokens=* USEBACKQ" %%F IN (`findstr Python %_TMPOutput%`) DO (
    ECHO %%F >> %_TMPOutput2%   
)

IF NOT EXIST %_TMPOutput2% goto InstallPython

DEL %_TMPOutput%

for /F "tokens=* USEBACKQ" %%F in (`findstr /vi \venv\Scripts %_TMPOutput2%`) do (
    ECHO %%F >> %_TMPOutput%
)


for /F "tokens=*" %%F in (%_TMPOutput%) do (
    SET _PythonPath=%%F
    %_PythonPath% --version > %_TMPOutput2%
    for /f "tokens=*" %%G in (%_TMPOutput2%) do (
        SET _PythonInfo=%%G
        IF %_PythonInfo:~7,3%==3.8 goto InstallDependancy
        IF %_PythonInfo:~7,3%==3.9 goto InstallDependancy
    )     
)

:InstallPython
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

ECHO Installing python
::return the OS version and if it's 32 or 64 bits from the systeminfo command
SETLOCAL ENABLEDELAYEDEXPANSION
SET _count=1
FOR /F "tokens=* USEBACKQ" %%F IN (`systeminfo`) DO (
    SET _var!_count!=%%F
    SET /a _count=!_count!+1
)
ENDLOCAL & SET _Version=%_var3:~27,3%& SET _Systype=%_var14:~28,2% 

ECHO %_Version% --- %_Systype%

::check windows Vista
IF %_Version%==6.0 goto DownloadPythonOld
::check windows 7
IF %_Version%==6.1 goto DownloadPythonOld
::check windows 8
IF %_Version%==6.2 goto DownloadPythonNew
IF %_Version%==6.3 goto DownloadPythonNew
::check windows 10
IF %_Version%==10. goto DownloadPythonNew 
goto InstallPythonFaillure


::for windows 7 and Vista
:DownloadPythonOld
IF %_Systype%==32 SET _link=https://www.python.org/ftp/python/3.8.9/python-3.8.9.exe
IF %_Systype%==64 SET _link=https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe
goto InstallPython


::for windows 8 or newer
:DownloadPythonNew
IF %_Systype%==32 SET _link=https://www.python.org/ftp/python/3.9.4/python-3.9.4.exe
IF %_Systype%==64 SET _link=https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe
goto InstallPython


:InstallPython
set "_dnld=bitsadmin /transfer PythonDownloading /download /priority normal"
%_dnld% %_link% %cd%\pythonInstall.exe
pythonInstall.exe /passive InstallAllUsers=0
::DEL pythonInstall.exe
SET _PythonPath =C:\Users\%username%\AppData\Local\Programs\Python
cd %_PythonPath%
for /f %%i in ('dir /ad/od/b') do set LAST=%%i
SET _PythonPath =C:\Users\%username%\AppData\Local\Programs\Python\%LAST%




:InstallDependancy
SET str=%_PythonPath%
for /l %%a in (1,1,31) do if "!str:~-1!"==" " set str=!str:~0,-1!

SET _PythonPathDirectory=%str:~0,-10%
DEL %_TMPOutput%
DEL %_TMPOutput2%

ECHO %_PythonPathDirectory% > PythonPath

goto EOF



python -m venv %~dp0\ProjectEnvironnement
%~dp0\ProjectEnvironnement\Scripts\activate
python -m pip install --upgrade pip
pip install click
pip install flask

goto EOF

:InstallPythonFaillure
ECHO "OS not handled by the installer, please install python manually"
::EXIT 1


:EOF
cd %~dp0
PAUSE
::EXIT 0