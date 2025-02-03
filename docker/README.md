# Docker files for AutoWatS CGI server deployment

To use them, dowload the files in this directory and run `docker-compose`.

```bash
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/Dockerfile?raw=true -O Dockerfile
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/docker-compose.yml?raw=true -O docker-compose.yml
wget https://github.com/SKZ81/AutoWatS-HTTP-server/blob/main/docker/nginx.conf?raw=true -O nginx.conf
docker-compose build
docker-compose up -d
```

