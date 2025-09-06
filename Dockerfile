# use the official docker image
FROM python:3.12-bullseye

# set a directory for the app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for mysqlclient
# RUN apt-get update \
#     && apt-get install -y default-libmysqlclient-dev libmariadb-dev gcc pkg-config \
#     && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY ./requirements.txt .

# improve docker cache efficiency
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh


# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# expose port
EXPOSE 8000

# run the application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
