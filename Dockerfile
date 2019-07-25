FROM python:3-onbuild

COPY . /blackbox
WORKDIR /blackbox

RUN pip3 install -r requirements.txt

CMD ["python", "./bin/run"]