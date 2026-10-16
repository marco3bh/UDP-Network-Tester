
@echo off
setlocal EnableExtensions
title MBH DDOS UDP FLOOD
color 0F
cd /d "%~dp0"

:menu
cls
echo.
echo  __  __  ____   _   _
echo ^|  \/  ^|^| __ ^) ^|^| ^| ^| ^|
echo ^| ^|\/^| ^|^|  _ \ ^|^| ^|_^| ^|
echo ^| ^|  ^| ^|^| ^|_^) ^|^|  _  ^|
echo ^|_^|  ^|_^|^|____/ ^|^|_^| ^|_^|
echo.
echo  ==========================================
echo             MBH DDOS UDP FLOOD
echo  ==========================================
echo.
echo             LOCAL NETWORK LAB
echo.
echo    [1] UDP FLOOD 
echo    [2] UDP POWER 
echo    [3] UDP MIX    
echo    [4] EXIT
echo.
echo  ==========================================
echo.
set "mode="
set /p "choice=  MBH / SELECT MODE: "

if "%choice%"=="4" exit /b
if "%choice%"=="1" set "mode=UDP-Flood"
if "%choice%"=="2" set "mode=UDP-Power"
if "%choice%"=="3" set "mode=UDP-Mix"

if not defined mode goto menu

echo.
echo  ------------------------------------------
echo              TEST CONFIGURATION
echo  ------------------------------------------
echo.
set "host="
set "port="
set "duration="
set "pps="

set /p "host=  TARGET IP [000.0.0.0]: "
if not defined host set "host=127.0.0.1"

set /p "port=  TARGET PORT [....]: "
if not defined port set "port=8080"

set /p "duration=  DURATION [... SEC]: "
if not defined duration set "duration=5"

set /p "pps=  PACKETS/SECOND [...]: "
if not defined pps set "pps=100"

python udp_tester.py "%host%" "%port%" "%mode%" --duration "%duration%" --pps "%pps%"

echo.
echo  ==========================================
echo                 TEST FINISHED
echo  ==========================================
echo.
pause
goto menu
