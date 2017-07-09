@echo off
TIMEOUT /T 10
taskkill /F /T /IM "EthDcrMiner64.exe"
taskkill /F /T /IM "ZecMiner64.exe"
shutdown -r -t 0
