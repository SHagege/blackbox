FROM python:3

COPY . /blackbox
WORKDIR /blackbox

RUN pip3 install -r requirements.txt

CMD ["python", "./bin/run", "--ip", "0.0.0.0"]