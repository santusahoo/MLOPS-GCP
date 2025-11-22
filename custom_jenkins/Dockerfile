# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root to install dependencies
USER root

# Install Docker (repo via keyring; no apt-key; auto-detect arch/codename)
RUN set -eux; \
    apt-get update -y; \
    apt-get install -y ca-certificates curl gnupg lsb-release; \
    install -m 0755 -d /etc/apt/keyrings; \
    curl -fsSL https://download.docker.com/linux/debian/gpg \
      | gpg --dearmor -o /etc/apt/keyrings/docker.gpg; \
    chmod a+r /etc/apt/keyrings/docker.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
      > /etc/apt/sources.list.d/docker.list; \
    apt-get update -y; \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# If you really want DinD local storage (usually not needed for docker-out-of-docker)
# RUN mkdir -p /var/lib/docker
# VOLUME /var/lib/docker

# Back to jenkins user
USER jenkins
