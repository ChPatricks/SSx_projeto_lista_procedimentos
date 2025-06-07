# Usar uma imagem Python leve como base
FROM python:3.11-slim

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https unixodbc-dev

# Instalar Microsoft ODBC Driver 18 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copiar o requirements.txt para a imagem e instalar as libs Python
COPY requirements.txt /requirements.txt
WORKDIR /SSx_projeto_lista_procedimentos
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para a imagem
COPY . /SSx_projeto_lista_procedimentos

# Comando para rodar a aplicação
CMD ["python", "app.py"]
