@ECHO OFF

REM The script install python if no suitable version is found
REM It then install a click and flask in a virtual environnement

SET _TMPOutput=TMPOutput.txt
SET _TMPOutput2=TMPOutput2.txt
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

::check if the path to python is in an environnement variable
FOR /F "tokens=* USEBACKQ" %%F IN (`where python`) DO (
    ECHO %%F >> %_TMPOutput%
)
IF NOT EXIST %_TMPOutput% goto FullSearch


::the output is cleared of erronous path
FOR /F "tokens=* USEBACKQ" %%F IN (`findstr Python %_TMPOutput%`) DO (
    ECHO %%F >> %_TMPOutput2%   
)
IF NOT EXIST %_TMPOutput2% goto FullSearch

::if a correct version of python was found
::we skip the part where we install python
SET _ContainPath=%_TMPOutput2%
CALL :PyVersionVerification
IF %_found%==true goto InstallDependancy


:FullSearch
ECHO python not found in environnement path
::If python not found, we check in the entire repository of the user
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

FOR /F "tokens=* USEBACKQ" %%F IN (`where /R C:\Users\%username% python`) DO (
    ECHO %%F >> %_TMPOutput%
)
IF NOT EXIST %_TMPOutput% goto InstallPython

::the output is cleared of erronous path
FOR /F "tokens=* USEBACKQ" %%F IN (`findstr Python %_TMPOutput%`) DO (
    ECHO %%F >> %_TMPOutput2%   
)
IF NOT EXIST %_TMPOutput2% goto InstallPython
DEL %_TMPOutput%


::the output is cleared of the virtual environnement path
for /F "tokens=* USEBACKQ" %%F in (`findstr /vi \venv\Scripts %_TMPOutput2%`) do (
    ECHO %%F >> %_TMPOutput%
)

::if a correct version of python was found
::we skip the part where we install python
SET _ContainPath=%_TMPOutput%
CALL :PyVersionVerification
IF %_found%==true goto InstallDependancy

:InstallPython
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

ECHO Installing python
::return the OS version and if it's 32 or 64 bits from the systeminfo command
SETLOCAL ENABLEDELAYEDEXPANSION
SET _count=1
FOR /F "tokens=* USEBACKQ" %%F IN (`systeminfo`) DO (
    SET _var=%%F
    IF !_count!==3 SET _Versiontmp=!_var!
    IF !_count!==14 SET _Systypetmp=!_var!
    SET /a _count=!_count!+1
    
)


:::~28,2

ENDLOCAL & SET _Version=%_Versiontmp:~44,3%& SET _Systype=%_Systypetmp:~45,2%
ECHO %_Version%
ECHO %_Systype%


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

::download python -> the file download depends on the link
::_dnld is the application and the arguments used to download
set "_dnld=bitsadmin /transfer PythonDownloading /download /priority normal"
%_dnld% %_link% %cd%\pythonInstall.exe
::auto install python -> still display a progress bar
pythonInstall.exe /passive InstallAllUsers=0
DEL pythonInstall.exe

SET _PythonPath =C:\Users\%username%\AppData\Local\Programs\Python
cd %_PythonPath%

::return the last created directory
for /F %%i in ('dir /ad/od/b') do set LAST=%%i
SET _PythonPath =C:\Users\%username%\AppData\Local\Programs\Python\%LAST%




:InstallDependancy
IF EXIST %_TMPOutput% DEL %_TMPOutput%
IF EXIST %_TMPOutput2% DEL %_TMPOutput2%

ECHO Installing dependancy

::trim the path to python in order to contain only the repository
SET _current=a
:loop
SET _current=%_PythonPath:~-1%%_current%
SET _PythonPath=%_PythonPath:~0,-1%
SET _extracted=%_current:~0,10%
IF "%_extracted%" NEQ "python.exe" goto loop

:: create a virtual environnement in a new folder
:: and install flask and click
mkdir ProjectEnvironnement
%_PythonPath%python -m venv %~dp0\ProjectEnvironnement
%~dp0\ProjectEnvironnement\Scripts\python.exe -m pip install --upgrade pip
%~dp0\ProjectEnvironnement\Scripts\pip.exe install click
%~dp0\ProjectEnvironnement\Scripts\pip.exe install flask

goto EOF

:PyVersionVerification
::check the version for each python version
::where its path is in the file _ContainPath
SETLOCAL ENABLEDELAYEDEXPANSION

SET _found=false

FOR /F "tokens=* USEBACKQ" %%F IN (%_ContainPath%) DO (
    SET "_LPythonPath=%%F"
    !_LPythonPath! --version>TEMPFILE
    for /F "tokens=*" %%H in (TEMPFILE) do (
        SET "_PythonInfo=%%H"
        SET "_version=!_PythonInfo:~7,3!"
        IF !_version!==3.8 SET _found=true
        IF !_version!==3.9 SET _found=true
        IF !_found!==true goto breakloop
    )   
)
:breakloop

DEL TEMPFILE
ENDLOCAL & SET _PythonPath=%_LPythonPath%& SET _Found=%_found%
EXIT /B 0


:EOF
:: return where we executed the script
cd %~dp0
ECHO "Installation complete"
PAUSE
EXIT 0

:InstallPythonFaillure
ECHO "OS not handled by the installer, please install python manually"
EXIT 1

