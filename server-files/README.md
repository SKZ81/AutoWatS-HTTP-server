# Docker files for AutoWatS CGI server deployment

## Server installation

The server must be installed with `docker-compose` beforehand.

First, as root, create some directory to install the files, for instance:

```bash
# mkdir /var/www/autowats-cgi
# cd /var/www/autowats-cgi
```

Download the files needed to start the container (alternatively, `scp` them from your working copy...):

```bash
# wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/server-files/docker/Dockerfile?raw=true -O Dockerfile
# wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/server-files/docker/docker-compose.yml?raw=true -O docker-compose.yml
# wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/server-files/docker/nginx.conf?raw=true -O nginx.conf
```

## Manually start the service

```bash
docker-compose up -d --build
```

## Database volume path

It can be queried by `docker volume inspect aws-docker_autowats_db | jq -r .[].Mountpoint` (YMMV)

## Systemd unit

A systemd unit is available, download or scp it into `/etc/systemd/system/`.

For instance:

```bash
# cd /etc/systemd/system/
# wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/server-files/systemd/AutoWatS-cgi.service
# systemctl daemon-reload
# systemctl enable AutoWatS-cgi
# systemctl start AutoWatS-cgi
```

**NOTE:** If your installation path differs from `/var/www/autowats-cgi`, you **MUST** edit the service file, and adapt the `WorkingDirectory` variable in `[service]` section to match your installation.

## Updating

In order to force a rebuild of the container after pushing new commits into the repo, use:

```bash
$ docker-compose build --no-cache autowats-cgi-server
```

And restart it using `systectl` or `docker-compose up -d --no-deps autowats-cgi-server`.

## Exposing the server

The service assumes it runs in a secured environment with a front instance of nginx that manages a listening HTTPS port. It emulates sub-domains, and redirects the traffic to a sub-domain to a dedicated docker instance.
That's why the default configuration only accepts request from localhost.
It assumes the deployment environment provides a local proxy that forwards external requests.

The container can be exposed to the world directly, by removing the `127.0.0.1` in **both** `nginx.conf` AND `docker-compose.yml`.

You can also configure the listening port of the docker in `nginx.conf`.
