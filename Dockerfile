FROM ubuntu:latest
# Installing dependencies and cleaning up
RUN apt-get update && \
        apt-get install -y python3 python3-pip postgresql-client libpq-dev libcurl4-openssl-dev libssl-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*
# Install pipenv
RUN pip3 install pipenv
# Setting the working directory
WORKDIR /app
# Install pipenv dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
# Copying our application into the container
COPY bin bin
COPY todo todo

# Running our application
ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["serve"]
