# to run this script
# .\install-dependencies.ps1

# install-dependencies.ps1

# Change to the directory where the requirements.txt is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# Install yt-dlp using winget
# winget install yt-dlp.yt-dlp    # uncomment if you want .exe of yt-dlp

# Install FFmpeg using winget
winget install Gyan.FFmpeg