# Use official Python 3.13 minimal Debian-based image
FROM python:3.13-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install necessary packages: Nginx, FastCGI, Git, SQLite
RUN apt update && apt install -y \
    nginx fcgiwrap spawn-fcgi sqlite3 git \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /tmp

# Clone your GitHub repo
RUN git clone https://github.com/SKZ81/AutoWatS-HTTP-server.git /tmp/autowats
# Copy website files
RUN mkdir -p /var/www
RUN cp -r /tmp/autowats/html /var/www/
RUN cp -r /tmp/autowats/images /var/www/
RUN cp -r /tmp/autowats/cgi-bin /var/www/
RUN cp -r /tmp/autowats/db /var/www/

# Ensure correct permissions for CGI scripts
RUN chmod +x /var/www/cgi-bin/*.py

# Create directories for CGI scripts and static content
RUN mkdir -p /var/www/cgi-bin /var/www/html

# Set correct permissions
RUN chown -R www-data:www-data /var/www/cgi-bin

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Initialize SQLite database
RUN mkdir -p /var/www/db && \
    [ -f /var/www/db/database.db ] || sqlite3 /var/www/db/database.db < /var/www/db/database.sql

# Give ownership to web user
RUN chown -R www-data:www-data /var/www/

# Cleanup temp git repo
RUN rm -rf /tmp/autowats

# Expose only port 1486
EXPOSE 1486

# Start fcgiwrap with correct permissions
RUN mkdir -p /run/fcgiwrap && chown www-data:www-data /run/fcgiwrap
CMD spawn-fcgi -s /run/fcgiwrap.socket -M 666 -u www-data -g www-data /usr/sbin/fcgiwrap && \
    nginx -g "daemon off;"

