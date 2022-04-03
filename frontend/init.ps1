if (-not (Test-Path node_modules/electron/dist)) {
    Expand-Archive -Path prebuilt/electron/electron-v11.5.0-win32-x64.zip -DestinationPath node_modules/electron/dist
    # echo 'electron.exe' | Out-File node_modules/electron/path.txt
    Copy-Item -Path prebuilt/electron/path.txt -Destination node_modules/electron/path.txt -Force
}

if (-not (Test-Path node_modules/seamap)) {
    Copy-Item -Path prebuilt/node_modules/seamap -Destination node_modules/seamap -Recurse -Force
}
