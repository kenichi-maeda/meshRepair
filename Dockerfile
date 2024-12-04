# Base image: pymesh/pymesh
FROM pymesh/pymesh:latest

# Install dependencies required to build Python from source
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev && \
    apt-get clean

# Download, build, and install Python 3.9
RUN wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz && \
    tar xzf Python-3.9.9.tgz && \
    cd Python-3.9.9 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.9.9.tgz Python-3.9.9

# Set Python 3.9 as the default python3
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1

# Verify Python installation
RUN python3 --version
