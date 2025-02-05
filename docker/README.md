# Docker files for AutoWatS CGI server deployment

## Download 
To use them, dowload the files in this directory and run `docker-compose`.

```bash
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/Dockerfile?raw=true -O Dockerfile
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/docker-compose.yml?raw=true -O docker-compose.yml
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/nginx.conf?raw=true -O nginx.conf
```

## Build and start
```bash
docker-compose build
docker-compose up -d
```

Note that it will create a volume...

It can be queried by `docker volume inspect aws-docker_autowats_db | jq -r .[].Mountpoint` (YMMV)

## Exposing the server

The default configuration only accepts request from localhost.
It assumes the deployment environment provides a local proxy that forwards external requests.

The container can be exposed to the world directly, by removing the `127.0.0.1` in **both** `nginx.conf` AND `docker-compose.yml`.
