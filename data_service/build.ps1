New-Item -ItemType Directory -Force -Path ../release/compute_service
python compile.py
Remove-Item __pycache__ -Recurse
# 'python server.pyc' | Out-File ../release/compute_service/run.ps1
