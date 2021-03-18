FROM python:3.8.5

WORKDIR /code
COPY . .

RUN pip install -r requirements.txt
EXPOSE 5000

ENV FLASK_APP=/code/Flask_REST/
CMD ["flask", "run", "--host=0.0.0.0"]
