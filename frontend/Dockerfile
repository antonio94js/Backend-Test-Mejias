FROM node:10.16.3-buster

# File Author / Maintainer
LABEL maintainer="DealSyte Engineering Team"

# Setting enviroment variables
ENV appDir /usr/src/app

# Setting work directory
WORKDIR ${appDir}

# Create app directory and changing owner
RUN mkdir -p ${appDir} && chown -R node:node ${appDir}

# Updating dependecies and making sudo available
RUN apt-get update 

# Copy package.json inside app
COPY package.json ./

# Set the container user
USER node

# Install app dependencies
RUN yarn

#  Bundle source code
COPY --chown=node:node . ./

# Build the app
# RUN yarn build

EXPOSE 3000

CMD [ "yarn", "start" ]
