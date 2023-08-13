@echo off
cd %~dp0

docker login
docker-compose up

pause