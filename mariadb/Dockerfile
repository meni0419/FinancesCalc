FROM mariadb:latest

# Устанавливаем mysql-client, не удаляя важные файлы MariaDB
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt/lists/*