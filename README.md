# 🚀 Core API - Microsserviços, Cache e Mensageria

Este projeto é uma Prova de Conceito (PoC) de uma arquitetura de microsserviços moderna, focada em alta performance, desacoplamento e processamento assíncrono. Todo o ecossistema é orquestrado via **Docker** e **Docker Compose**.

## 🏗️ Diagrama de Arquitetura

```mermaid
graph TD
    Cliente((Usuário / Cliente HTTP))

    subgraph "Aplicação Conteinerizada (Docker)"
        API[API FastAPI <br> Porta 8000]
        Worker[Worker Assíncrono <br> Background]
    end

    subgraph "Infraestrutura de Dados (Docker)"
        Redis[(Redis <br> Cache Rápido)]
        Mongo[(MongoDB <br> Persistência)]
        Rabbit[[RabbitMQ <br> Mensageria]]
    end

    Cliente -->|1. Requisições REST| API
    API -->|2. Busca/Salva Cache| Redis
    API -->|3. Lê/Grava Dados| Mongo
    API -->|4. Publica Evento| Rabbit
    
    Rabbit -->|5. Consome Mensagem| Worker
    Worker -->|6. Registra Status| Mongo
    
    classDef infra fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef app fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    class Redis,Mongo,Rabbit infra;
    class API,Worker app;
