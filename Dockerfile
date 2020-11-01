from python:3.9

run mkdir /app/

copy requirements.txt /app/

run python -m venv /app/venv/

run /app/venv/bin/pip install -r /app/requirements.txt

copy src src

workdir /src/

cmd /app/venv/bin/uvicorn --host 0.0.0.0 main:app