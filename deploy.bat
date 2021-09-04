@echo off
echo setup.py でのバージョンインクリメントは実施しましたか？
pause

rd /s /q dist

call venv\Scripts\activate.bat

venv\Scripts\python.exe setup.py sdist
venv\Scripts\python.exe setup.py bdist_wheel

echo テスト環境 testpypi にアップロードしてよろしいですか？
pause

twine upload --repository testpypi dist/*

echo 本番環境 pypi にアップロードしてよろしいですか？
pause

twine upload --repository pypi dist/*

pause