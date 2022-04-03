$dest = $env:USERPROFILE + '\AppData\Local\electron-builder\Cache\wincodesign\wincodesign-2.6.0'
$src = 'prebuilt\wincodesign\wincodesign-2.6.0'
if (-not (Test-Path $dest)) {
    Copy-Item -Path $src -Destination $dest -Recurse -Force
}

$dest = $env:USERPROFILE + '\AppData\Local\electron-builder\Cache\nsis\nsis-3.0.4.1'
$src = 'prebuilt\nsis\nsis-3.0.4.1'
if (-not (Test-Path $dest)) {
    Copy-Item -Path $src -Destination $dest -Recurse -Force
}

$dest = $env:USERPROFILE + '\AppData\Local\electron-builder\Cache\nsis\nsis-resources-3.4.1'
$src = 'prebuilt\nsis\nsis-resources-3.4.1'
if (-not (Test-Path $dest)) {
    Copy-Item -Path $src -Destination $dest -Recurse -Force
}

$destDir = $env:USERPROFILE + '\AppData\Local\electron\cache\'
$dest = $destDir + 'electron-v11.5.0-win32-x64.zip'
$src = 'prebuilt\electron\electron-v11.5.0-win32-x64.zip'
if (!(Test-Path $dest)) {
    New-Item -ItemType Directory -Force -Path $destDir
    Copy-Item -Path $src -Destination $dest -Force
}

npm run build:elec:std
