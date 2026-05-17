# 🚀 Core API - Microsserviços, Cache, IaC e CI/CD na Nuvem

Este projeto evoluiu de uma Prova de Conceito (PoC) local para uma arquitetura conteinerizada robusta e automatizada, implantada na nuvem pública (**Microsoft Azure**). O ecossistema combina desenvolvimento de microsserviços de alta performance com práticas modernas de **IaC (Infraestrutura como Código)** e **CI/CD (Integração e Implantação Contínuas)**.

---

## 🏗️ Diagrama de Arquitetura e Fluxo DevOps

```mermaid
graph TD
    %% Nós de Usuário e Dev
    Dev((Desenvolvedor))
    Cliente((Usuário / Cliente HTTP))

    %% Esteira de CI/CD
    subgraph "Esteira de Automação (CI/CD)"
        GH[GitHub Repositorio]
        GHA[GitHub Actions]
        DH[(Docker Hub Registry)]
    end

    %% Infraestrutura Azure
    subgraph "Nuvem Microsoft Azure (Canadá)"
        VM[Máquina Virtual Ubuntu <br> vm-core-api]
        FW[Network Security Group <br> Firewall: Portas 22, 8000]
        
        subgraph "Ambiente Docker Orchestrating"
            API[API FastAPI <br> Porta 8000]
            Worker[Worker Assíncrono]
            Redis[(Redis Cache)]
            Mongo[(MongoDB)]
            Rabbit[[RabbitMQ]]
        end
    end

    %% Ferramentas de Provisionamento
    TF[Terraform <br> Provisionamento]
    AN[Ansible <br> Configuração]

    %% Fluxo de Infraestrutura (IaC)
    TF -->|1. Cria Infra/Network| VM
    AN -->|2. Configura VM & Instala Docker| VM

    %% Fluxo de Código (CI)
    Dev -->|3. Git Push Code| GH
    GH -->|4. Dispara Trigger| GHA
    GHA -->|5. Build & Push Imagem| DH

    %% Fluxo de Execução
    Cliente -->|6. Requisições REST| FW
    FW --> API
    API -->|Cache| Redis
    API -->|Persistência| Mongo
    API -->|Mensageria| Rabbit
    Rabbit --> Worker
    Worker --> Mongo

    classDef infra fill:#f5f5f5,stroke:#333,stroke-width:1px;
    classDef cloud fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef automation fill:#efebe9,stroke:#5d4037,stroke-width:2px;
    class TF,AN automation;
    class VM cloud;
