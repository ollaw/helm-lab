FROM public.ecr.aws/prima/python:3.10.2

COPY requirements.txt /

RUN pip3 install --no-cache-dir -r /requirements.txt

COPY . /flask
WORKDIR /flask

ENTRYPOINT ["./bin/entrypoint.sh"]