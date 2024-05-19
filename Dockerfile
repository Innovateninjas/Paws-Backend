# python image
FROM python:3

# set the current working directory inside the container
WORKDIR /app

# copy the file into container
COPY . .

# Install dependancies
RUN pip install -r requirements.txt


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

