$IsWindows = [System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform("Windows")

# $airflowUrl = "https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml"

# if ($IsWindows) {
#     $outputFile = "$PSScriptRoot\docker-compose.yaml"   # Windows Path
# } else {
#     $outputFile = "$PSScriptRoot/docker-compose.yaml"   # Linux/Mac Path
# }

# Write-Host "Detected OS: $(Get-ComputerInfo | Select-Object -ExpandProperty OsName)"

# Write-Host "Downloading Apache Airflow docker-compose file..."
# Invoke-WebRequest -Uri $airflowUrl -OutFile $outputFile

if ($IsWindows) {
    $outputFile = "$PSScriptRoot\docker-compose.yaml"
    $envFile = "$PSScriptRoot\.env"
    $folders = @("dags", "logs", "plugins", "config")
} else {
    $outputFile = "$PSScriptRoot/docker-compose.yaml"
    $envFile = "$PSScriptRoot/.env"
    $folders = @("dags", "logs", "plugins", "config")
}

Write-Host "Creating Airflow directories..."
foreach ($folder in $folders) {
    $folderPath = Join-Path -Path $PSScriptRoot -ChildPath $folder
    if (!(Test-Path $folderPath)) {
        New-Item -Path $folderPath -ItemType Directory | Out-Null
    }
}
Write-Host "✅ Directories created: dags, logs, plugins, config"

Write-Host "Generating .env file..."
if ($IsWindows) {
    Set-Content -Path $envFile -Value "AIRFLOW_UID=50000"
    Write-Host "⚠️ Windows detected! Set AIRFLOW_UID=50000 (Change if needed)"
} else {
    $airflowUid = $(id -u)
    Set-Content -Path $envFile -Value "AIRFLOW_UID=$airflowUid"
    Write-Host "✅ .env file created with AIRFLOW_UID=$airflowUid"
}

Write-Host "Starting Apache Airflow with Docker Compose..."
docker-compose up airflow-init #REVIEW - this creates an airflow-init container. Why?
docker-compose up -d #REVIEW - why?