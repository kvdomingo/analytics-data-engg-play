terraform {
  required_version = "~>1"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>6"
    }
  }

  backend "gcs" {
    prefix = "ae-de-play/tfstate"
    bucket = "my-projects-306716-terraform-backend"
  }
}
