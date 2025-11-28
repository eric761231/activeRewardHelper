<#
Push the current project to GitHub, ensuring sensitive files are untracked.

Usage:
  .\scripts\push_to_github.ps1 -RemoteUrl "https://github.com/eric761231/activeRewardHelper.git"

Notes:
- This script will NOT send credentials; Git will prompt for authentication if needed.
- If you prefer, authenticate with `gh auth login` (GitHub CLI) or use an HTTPS PAT.
#>
param(
    [string]$RemoteUrl = "https://github.com/eric761231/activeRewardHelper.git",
    [switch]$Force
)

Set-Location -Path "$PSScriptRoot\.."

Write-Host "Working directory: $(Get-Location)"

try {
    # init repo if needed
    $isRepo = $false
    try { git rev-parse --is-inside-work-tree > $null 2>&1; $isRepo = $LASTEXITCODE -eq 0 } catch { $isRepo = $false }
    if (-not $isRepo) {
        Write-Host "Initializing git repository..."
        git init
    } else {
        Write-Host "Git repository detected"
    }

    # Ensure .gitignore contains sensitive patterns (append if missing)
    $gi = Get-Content .gitignore -ErrorAction SilentlyContinue
    $needUpdate = $false
    $patterns = @('config/keys/*.json', 'config/mysql_config.json', 'config/cloud_csv_config.json', 'credentials.json')
    foreach ($p in $patterns) {
        if ($gi -notcontains $p) { $needUpdate = $true }
    }
    if ($needUpdate) {
        Write-Host "Updating .gitignore with sensitive patterns"
        Add-Content -Path .gitignore -Value "`n# ignore sensitive keys and config`nconfig/keys/*.json`nconfig/mysql_config.json`nconfig/cloud_csv_config.json`ncredentials.json"
    }

    # Remove tracked sensitive files (keep local copy)
    Write-Host "Removing tracked sensitive files from git index (keeps local files)..."
    git rm --cached -r config/keys 2>$null
    git rm --cached config/mysql_config.json 2>$null
    git rm --cached config/cloud_csv_config.json 2>$null
    git rm --cached credentials.json 2>$null

    # Stage and commit
    Write-Host "Staging files..."
    git add .

    # Commit if there are changes
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Host "No changes to commit"
    } else {
        git commit -m "Prepare repo for GitHub: add README, _redirects, protect credentials"
    }

    # Set remote
    Write-Host "Configuring remote: $RemoteUrl"
    try { git remote remove origin 2>$null } catch {}
    git remote add origin $RemoteUrl

    # Push
    Write-Host "Pushing to remote (may prompt for credentials)..."
    git branch -M main
    git push -u origin main

    Write-Host "Push complete. Visit: $RemoteUrl"
}
catch {
    Write-Error "An error occurred: $_"
    Write-Host "If push failed due to authentication, try: `n 1) gh auth login`n 2) or set a Personal Access Token and use it when prompted.`nYou can also run: gh repo create eric761231/activeRewardHelper --source=. --remote=origin --push"
}
