IF "%~1" == "" (set thisPython=python) ELSE (set thisPython="%~1")
%thisPython% -m pip install virtualenv
%thisPython% -m virtualenv ares-env
.\ares-env\Scripts\python.exe -m pip install -r requirements.txt