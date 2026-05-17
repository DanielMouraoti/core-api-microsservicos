# Usa uma versão oficial e leve do Python
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia a lista de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua API e Worker para dentro do container
COPY . .

# Não colocamos o comando final (CMD) aqui porque vamos usar 
# esta mesma imagem base para rodar a API e o Worker separadamente.
