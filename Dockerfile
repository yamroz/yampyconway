FROM python

RUN pip install asciimatics
RUN mkdir -p /home/app/src

COPY ./src /home/app/src

CMD ["python3","/home/app/src/run.py"]
