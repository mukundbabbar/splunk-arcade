#!/bin/bash

set -euxo pipefail

echo "secret_suffix = \"${TF_VAR_player_name}\"" > backend.hcl

terraform init -reconfigure -input=false -backend-config=backend.hcl
terraform apply -auto-approve