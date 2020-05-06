# ##
# # Build Stage
# ##
# FROM node:10.16.3-buster as build-stage

# # Setting enviroment variables
# ENV appDir /usr/src/app

# # Setting work directory
# WORKDIR ${appDir}

# # Create app directory and changing owner
# RUN mkdir -p ${appDir}

# # Copy package.json inside app
# COPY frontend/yarn.lock ./

# # Install app dependencies
# RUN yarn global add node-gyp
# RUN yarn

# #  Bundle source code
# COPY --chown=node:node frontend/ ./

# # Compile the app
# RUN yarn build

##
# Python stage
##
FROM nikolaik/python-nodejs:python3.7-nodejs10

# File Author / Maintainer
LABEL maintainer="Antonio Mejias"

# Setting enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV appDir /usr/src/app
ENV frontendDir /usr/src/app/frontend

WORKDIR ${appDir}


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

# Install psql
RUN apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*


## Add and Install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

## Add app
COPY . ./

# Setting work directory
WORKDIR ${frontendDir}

RUN yarn
RUN yarn build
  
WORKDIR ${appDir}

RUN chmod +x ./entrypoint.sh

EXPOSE 8028

ENTRYPOINT [ "./entrypoint.sh" ]

CMD python manage.py run -h 0.0.0.0