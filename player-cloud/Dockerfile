# Use the official Terraform image
FROM hashicorp/terraform:latest

# Set working directory
WORKDIR /terraform

RUN apk update && \
    apk add --no-cache \
    bash \
    curl \
    && rm -rf /var/cache/apk/*

COPY providers.tf .
RUN terraform init -input=false
RUN rm providers.tf

COPY entrypoint.apply.sh /terraform/entrypoint.apply.sh
COPY entrypoint.destroy.sh /terraform/entrypoint.destroy.sh
COPY main.tf /terraform/main.tf
COPY vars.tf /terraform/vars.tf

#ENTRYPOINT ["/terraform/entrypoint.apply.sh"]