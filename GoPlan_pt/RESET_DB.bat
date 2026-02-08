@echo off
chcp 65001 >nul
echo ================================================
echo СБРОС И ПЕРЕСОЗДАНИЕ БАЗЫ ДАННЫХ
echo ================================================
echo.
echo ВНИМАНИЕ: Это удалит все данные в базе данных!
echo.
set /p confirm="Вы уверены? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Отменено.
    pause
    exit /b
)
echo.
echo Удаление старой базы данных...
if exist db.sqlite3 del db.sqlite3
echo.
echo Применение миграций...
python.exe manage.py migrate
if %errorlevel% neq 0 (
    echo.
    echo Попытка с py...
    py manage.py migrate
)
echo.
echo ================================================
echo База данных пересоздана!
echo ================================================
pause
