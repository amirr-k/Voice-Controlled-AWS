FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    awscli \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY audio_service.cpp .
COPY CMakeLists.txt .


RUN mkdir build && cd build && \
    cmake .. && \
    make

EXPOSE 8080
CMD ["./build/audio_service"]