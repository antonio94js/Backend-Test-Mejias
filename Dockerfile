FROM python:3.7.5-buster

# File Author / Maintainer
LABEL maintainer="Antonio Mejias"

# Setting enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV appDir /usr/src/app

# Setting work directory
WORKDIR ${appDir}

#  Add user
#  RUN addgroup --system django && adduser --system --no-create-home --group django

# Create app directory and changing owner
RUN mkdir -p ${appDir}
# RUN mkdir -p ${appDir} && chown -R django:django ${appDir}

# Add an alias to the python manage.py command inside the container
RUN echo 'alias dj="python manage.py"' >> ~/.bashrc

## Update and Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean
  

## Add and Install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


## switch to non-root user
# USER django

## Add app
COPY . ./

RUN chmod +x ./entrypoint.sh

EXPOSE 8028

ENTRYPOINT [ "./entrypoint.sh" ]

CMD python manage.py run -h 0.0.0.0