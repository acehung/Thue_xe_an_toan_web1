@echo off
REM Test API Login & Register

echo.
echo ====== TEST API LOGIN ======
echo.

echo Username: testuser@example.com
echo Password: TestPass123
echo.

echo Sending POST request to /api/login/
echo.

curl -X POST http://127.0.0.1:8000/api/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser@example.com\",\"password\":\"TestPass123\"}" ^
  -v

echo.
echo.
echo ====== TEST REGISTER NEW USER ======
echo.

echo Sending POST request to /api/register/
echo.

curl -X POST http://127.0.0.1:8000/api/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"New User\",\"email\":\"newuser@example.com\",\"phone\":\"0912345678\",\"password\":\"NewPass123\",\"cccd\":\"123456789012\"}" ^
  -v

echo.
echo Done!
pause
