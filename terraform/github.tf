resource "github_repository" "backend_url" {
  name                 = "${var.name}-backend-url"
  visibility           = "public"
  auto_init            = true
  vulnerability_alerts = false

  pages {
    source {
      branch = "main"
      path   = "/"
    }
  }
}

resource "github_repository_file" "backend_url" {
  repository          = github_repository.backend_url.name
  branch              = "main"
  file                = "index.html"
  content             = "https://${azurerm_container_app.this.ingress[0].fqdn}/"
  commit_message      = "write backend url"
  commit_author       = "Terraform User"
  commit_email        = "terraform[bot]@bot.github.com"
  overwrite_on_create = true
}