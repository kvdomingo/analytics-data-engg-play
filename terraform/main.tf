resource "google_storage_bucket" "default" {
  name                        = "kvdstudio-ae-de-play"
  location                    = "asia-east1"
  force_destroy               = true
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  hierarchical_namespace {
    enabled = true
  }

  soft_delete_policy {
    retention_duration_seconds = 0
  }
}
