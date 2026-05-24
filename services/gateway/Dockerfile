FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

RUN apt update
RUN apt install build-essential -y

COPY . /usr/src/app

RUN python setup.py build_ext --inplace

ENTRYPOINT ["python", "main.py"]