FROM python:3.7.5-slim-buster

# File Author / Maintainer
LABEL maintainer="Antonio Mejias"

# Setting enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV appDir /usr/src/app

# Setting work directory
WORKDIR ${appDir}

# Add user
 RUN addgroup --system django && adduser --system --no-create-home --group django

# Create app directory and changing owner
RUN mkdir -p ${appDir} && chown -R django:django ${appDir}

# Add an alias to the python manage.py command inside the container
RUN echo 'alias dj="python manage.py"' >> ~/.bashrc
## Update and Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean
  

# RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

## Add and Install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

## Add entrypoint.sh
# COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
# RUN chmod +x /usr/src/app/entrypoint.sh

## switch to non-root user
USER django

## Add app
COPY --chown=django:django . ./

EXPOSE 8028

## Run server
CMD python manage.py run -h 0.0.0.0