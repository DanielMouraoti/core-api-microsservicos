terraform {

  required_providers {

    google = {

      source  = "hashicorp/google"

      version = "~> 5.0"

    }

  }

}


provider "google" {

  project = "silken-centaur-478314-v6" # Insira o seu Project ID do GCP aqui

  region  = "us-central1"          # Região estável e com ótimo custo-benefício

}


# Criando a rede VPC para o cluster

resource "google_compute_network" "vpc_network" {

  name                    = "gke-vpc"

  auto_create_subnetworks = true

}


# Criando o Cluster Kubernetes (GKE Autopilot)

resource "google_container_cluster" "gke_cluster" {

  name     = "gke-core-api"

  location = "us-central1"


  # Ativando o modo Autopilot para máxima produtividade e menor custo

  enable_autopilot = true

  network          = google_compute_network.vpc_network.name


  ip_allocation_policy {

    # Configuração necessária para redes nativas de VPC do GKE

  }


  deletion_protection = false # Permite destruir o laboratório facilmente depois

}


# Output para facilitar o acesso ao cluster depois

output "kubernetes_cluster_name" {

  value = google_container_cluster.gke_cluster.name

}
