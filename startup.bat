@echo off
echo ==============================
echo      AT Command Testing
echo ==============================
set /p main_port=Please Enter the main phone port: 
echo.
set /p ref_port=Please Enter the reference phone port: 
echo.
set /p at_cmd_set=Please Enter the test set: 
echo.
echo AT Command testing startup...
python at_command_runner.py --main_port %main_port% --ref_port %ref_port% --at_cmd_set %at_cmd_set%
pause