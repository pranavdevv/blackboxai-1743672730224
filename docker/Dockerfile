FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Set up restricted user
RUN useradd -m coder && \
    chmod 755 /home/coder

WORKDIR /code
USER coder

# Install timeout command
RUN apt-get update && \
    apt-get install -y --no-install-recommends coreutils && \
    rm -rf /var/lib/apt/lists/*

CMD ["python"]