FROM python:3

#install psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install psycopg2>=2.7.1
RUN apt-get autoremove -y gcc
#install all packages needed
RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r app/requirements.txt
#we copy in our new directory the files we are going to run.
COPY ./postgre.py /app/postgre.py
COPY ./tripadvisor.py /app/tripadvisor.py
ENTRYPOINT ["python" , "/app/tripadvisor.py"]