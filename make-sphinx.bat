@echo off

call venv\Scripts\activate.bat

call make.bat html

cd build/html
git add -A
git commit -m "feat: build sphinx docs"
git push

pause