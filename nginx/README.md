# STAGE 1 - Exposing a REST API for managing Docker containers

The [Docker Daemon](https://docs.docker.com/config/daemon/) is Docker's mechanism of managing containers in a host machine. It provides a [unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) to be interacted with in order to leverage the Docker Daemon with a REST API. We rarely use this socket directly because we are provided with a `docker` CLI client that uses this socket under the hood, offering the user a higher level and more friendly interface to managing containers.

In this experimentation we don't want that. We wanna go under the hood, but not too deep, just enough to provide a REST API over a TCP port. For this, we use a NGINX proxy that listen on PORT and forwards all incoming requests to the Docker Daemon provided unix socket.

The NGINX proxy will, of course, run in a Docker container, but the Docker Daemon unix socket is provided on the host machine's file system, by default in `/var/run/docker.sock`. So we have to provide this socket to the container running NGINX, and we do it by mounting a volume.

## Requirements
This is `dangerous`, but for our naïve example to work fine, your `/var/run/docker.sock` might need maximum permissions... What I did was `chmod 777 /var/run/docker.sock` ¯\_(ツ)_/¯

## How to run this stage
Run `docker-compose up`.

Now you'll have the Docker Daemon REST API exposed in your port 80 localhost. This means that if you run `curl localhost/containers/json` you will get a JSON response with the description of all running Docker containers.

At this stage you can already use this endoint to do **anything** the `docker` CLI is able to do, just have a look on the [Docker API Documentation](https://docs.docker.com/engine/api/v1.24/)