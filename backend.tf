terraform {
  backend "gcs" {
    bucket  = "billing-account-access-tfstate"
    prefix = "terraform/state"
  }
}