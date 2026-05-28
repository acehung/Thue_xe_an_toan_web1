@echo off
setlocal
cd /d e:\autorent_backend

echo Testing login API...
echo.

curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d "{\"username\":\"testuser@example.com\",\"password\":\"TestPass123\"}"

echo.
echo.
echo Done!
pause
