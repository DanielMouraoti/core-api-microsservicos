# 🚀 Core API - Microsserviços, Cache, IaC, CI/CD e Kubernetes na Nuvem

Este projeto evoluiu de uma Prova de Conceito (PoC) local para uma infraestrutura moderna, resiliente e altamente escalável, orquestrada via **Kubernetes** na nuvem pública (**Google Cloud Platform - GCP**). O ecossistema combina o desenvolvimento de microsserviços de alta performance com práticas avançadas de **IaC (Infraestrutura como Código)** e **CI/CD (Integração e Implantação Contínuas)**.

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

    %% Infraestrutura GCP
    subgraph "Google Cloud Platform - GCP (us-central1)"
        VPC[Rede VPC Privada <br> gke-vpc]
        
        subgraph "Cluster Kubernetes GKE (Autopilot)"
            subgraph "Pods da Aplicação"
                API_Pod1[Pod: API FastAPI <br> Replica 1]
                API_Pod2[Pod: API FastAPI <br> Replica 2]
            end
            
            %% Componentes em transição para o cluster
            subgraph "Serviços de Suporte (Local/PoC)"
                Redis[(Redis Cache)]
                Mongo[(MongoDB)]
                Rabbit[[RabbitMQ]]
            end
        end
    end

    %% Ferramentas de Provisionamento
    TF[Terraform <br> IaC Declarativo]

    %% Fluxo de Infraestrutura (IaC)
    TF -->|1. Provisiona VPC & Cluster GKE| VPC

    %% Fluxo de Código (CI)
    Dev -->|2. Git Push Code| GH
    GH -->|3. Dispara Trigger| GHA
    GHA -->|4. Build & Push Imagem| DH

    %% Fluxo de Implantação e Execução
    DH -->|5. Puxa Imagem da API| API_Pod1
    DH -->|6. Puxa Imagem da API| API_Pod2
    
    Cliente -->|7. Requisições REST| API_Pod1 & API_Pod2
    
    %% Conexões lógicas da API
    API_Pod1 & API_Pod2 -.->|Cache| Redis
    API_Pod1 & API_Pod2 -.->|Persistência| Mongo
    API_Pod1 & API_Pod2 -.->|Mensageria| Rabbit

    classDef cloud fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;
    classDef automation fill:#efebe9,stroke:#5d4037,stroke-width:2px;
    class TF automation;
    class VPC,API_Pod1,API_Pod2 cloud;
