FROM python

EXPOSE 5002

RUN mkdir -p /home/yamconway

COPY ./requirements.txt /home/yamconway
RUN pip install -r /home/yamconway/requirements.txt

COPY ./yamconway /home/yamconway/yamconway
COPY ./run.py /home/yamconway
COPY ./run_REST_API.py /home/yamconway

CMD ["python3","/home/yamconway/run_REST_API.py"]
