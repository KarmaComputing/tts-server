FROM ubuntu:20.04
USER root
WORKDIR /code
COPY ./ /code

#!/bin/bash
RUN apt update -y
RUN apt-get install sudo -y
# Get latest patches
RUN apt-get upgrade -y
# Install apache
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install -y apache2

# Install python venv and pip
RUN apt install python3.8-venv -y
RUN apt install python3-pip -y
RUN apt install curl
# Add non-root user
RUN adduser --disabled-password --gecos "" tts

# Install cmake
RUN curl -L -o cmake3.23.1.tar.gz -v https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1.tar.gz

RUN tar xvf cmake3.23.1.tar.gz
RUN apt install libssl-dev
RUN cd cmake-3.23.1/ \
    ./bootstrap \
    make \
    make install \
    cmake --version

# Build llvm v10
RUN cd
RUN curl -L -o llvm-10.0.1.tar.gz -v https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.1/llvm-project-10.0.1.tar.xz
RUN tar xvf llvm-10.0.1.tar.gz
RUN cd llvm-project-10.0.1/llvm/
RUN LLVM_SRC=$(pwd)
RUN cd
RUN mkdir buildllvm
RUN cd buildllvm \
    cmake -D CMAKE_BUILD_PARALLEL_LEVEL=16 -G "Unix Makefiles" -D CMAKE_BUILD_TYPE=Release $LLVM_SRC \
    cmake --build . --parallel 16 \
    cmake --build . --parallel 16 --target install

# Install TTS
RUN apt-get install libsndfile1 -y
RUN sudo -iu tts 

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install wheel
RUN pip install -r requirements.txt

# Test tts
RUN sudo -iu tts 
RUN tts --text "This is a test"
RUN sudo -iu root
ENTRYPOINT ["/code/run-server.sh"]
