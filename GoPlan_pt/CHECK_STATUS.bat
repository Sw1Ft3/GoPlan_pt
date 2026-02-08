@echo off
chcp 65001 >nul
echo ================================================
echo Проверка статуса миграций Django
echo ================================================
echo.

echo Проверка доступных миграций...
python.exe manage.py showmigrations schedules
if %errorlevel% neq 0 (
    echo.
    echo Попытка с py...
    py manage.py showmigrations schedules
)
echo.
echo ================================================
echo Если видите [ ] перед миграциями - они не применены
echo Если видите [X] - они применены
echo ================================================
echo.
pause
