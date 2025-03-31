terraform {
  required_version = ">= 1.0"

  required_providers {
    signalfx = {
      source  = "splunk-terraform/signalfx"
      version = "~> 9.7.1"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35.1"
    }
  }
}