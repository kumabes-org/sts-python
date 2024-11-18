FROM python:3.10.0-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && export PYTHONPATH=${PWD}

EXPOSE 5000

CMD [ "python", "src/main.py" ]