@echo off
echo setup.py �ł̃o�[�W�����C���N�������g�͎��{���܂������H
pause

rd /s /q dist

call venv\Scripts\activate.bat

venv\Scripts\python.exe setup.py sdist
venv\Scripts\python.exe setup.py bdist_wheel

echo �e�X�g�� testpypi �ɃA�b�v���[�h���Ă�낵���ł����H
pause

twine upload --repository testpypi dist/*

echo �{�Ԋ� pypi �ɃA�b�v���[�h���Ă�낵���ł����H
pause

twine upload --repository pypi dist/*

pause