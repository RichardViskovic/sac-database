FROM php:8.2-apache

# Copy index.php and the project files into the web server directory
COPY . /var/www/html/

# Ensure the data directory exists and has write permissions for Apache
RUN mkdir -p /var/www/html/data && chown -R www-data:www-data /var/www/html/data

# Expose port 80 (Apache default, Render will automatically detect this and route public HTTPS traffic to it)
EXPOSE 80
