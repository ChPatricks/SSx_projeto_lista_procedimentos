#!/usr/bin/env bash

# Atualiza os pacotes
apt-get update

# Instala dependências
apt-get install -y curl gnupg apt-transport-https unixodbc-dev

# Adiciona o repositório do driver ODBC para SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualiza e instala o driver
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Se quiser usar o driver 17:
# ACCEPT_EULA=Y apt-get install -y msodbcsql17
