$json = '{"username":"testuser@example.com","password":"TestPass123"}'
Write-Host "Testing login endpoint..."
Write-Host "URL: http://127.0.0.1:8000/api/login/"
Write-Host "JSON: $json"
Write-Host ""

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/login/" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $json `
        -ErrorAction Stop
    
    Write-Host "SUCCESS! Response:"
    Write-Host $response.Content
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host "Status: $($_.Exception.Response.StatusCode)"
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $content = $reader.ReadToEnd()
        Write-Host "Content: $content"
    }
}
