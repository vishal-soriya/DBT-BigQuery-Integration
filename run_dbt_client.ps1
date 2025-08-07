# DBT Multi-Client Runner PowerShell Script
# Usage: .\run_dbt_client.ps1 <client> <environment> <command> [additional_args]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("client_a", "client_b")]
    [string]$Client,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "prod")]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$Command,
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AdditionalArgs
)

function Show-Usage {
    Write-Host "Usage: .\run_dbt_client.ps1 <client> <environment> <command> [additional_args]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Clients:"
    Write-Host "  client_a  - Uses DBT_VISHAL_DATASET"
    Write-Host "  client_b  - Uses DBT_client_b_DATASET"
    Write-Host ""
    Write-Host "Environments:"
    Write-Host "  dev   - Development environment" 
    Write-Host "  prod  - Production environment"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  run     - Run models"
    Write-Host "  test    - Run tests"
    Write-Host "  seed    - Load seed data"
    Write-Host "  build   - Run models and tests"
    Write-Host "  debug   - Test connection"
    Write-Host "  docs    - Generate and serve docs"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_dbt_client.ps1 client_a dev run"
    Write-Host "  .\run_dbt_client.ps1 client_b prod test"
    Write-Host "  .\run_dbt_client.ps1 client_a dev seed"
}

# Set target based on client and environment
$Target = "${Client}_${Environment}"

# Set environment variable for client ID
$env:DBT_CLIENT_ID = $Client

Write-Host "Running DBT for:" -ForegroundColor Green
Write-Host "  Client: $Client" -ForegroundColor Yellow
Write-Host "  Environment: $Environment" -ForegroundColor Yellow
Write-Host "  Target: $Target" -ForegroundColor Yellow
Write-Host "  Command: dbt $Command" -ForegroundColor Yellow
Write-Host ""

try {
    if ($Command -eq "docs") {
        Write-Host "Generating and serving documentation..." -ForegroundColor Green
        dbt docs generate --target $Target $AdditionalArgs
        Write-Host "Starting docs server..." -ForegroundColor Green
        dbt docs serve --target $Target $AdditionalArgs
    } else {
        # Run the DBT command with the specified target
        $CommandString = "dbt $Command --target $Target $($AdditionalArgs -join ' ')"
        Write-Host "Executing: $CommandString" -ForegroundColor Green
        dbt $Command --target $Target $AdditionalArgs
    }
    
    Write-Host "✅ DBT command completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ DBT command failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
