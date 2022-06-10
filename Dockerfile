FROM python:3.10
ENV PATH /usr/local/bin:$PATH
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY app /app
WORKDIR /app
CMD ["python", "clothes_man.py"]
