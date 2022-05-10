resource "aws_s3_bucket" "app_public_files" {
  bucket        = "${local.prefix}-bruvio-files"
  acl           = "public-read"
  force_destroy = true
}
