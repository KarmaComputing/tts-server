apt update
# Get latest patches
apt-get upgrade

# Install apache
apt install -y apache2
a2enmod proxy_uwsgi
systemctl restart apache2

# Install python venv and pip
apt install python3.8-venv
apt install python3-pip

# Add non-root user
adduser tts

# Install cmake
curl -L -o cmake3.23.1.tar.gz -v https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1.tar.gz

tar xvf cmake3.23.1.tar.gz
apt install libssl-dev
cd cmake-3.23.1/
./bootstrap
make
make install
cmake --version

# Build llvm v10
cd
curl -L -o llvm-10.0.1.tar.gz -v https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.1/llvm-project-10.0.1.tar.xz
tar xvf llvm-10.0.1.tar.gz
cd llvm-project-10.0.1/llvm/
LLVM_SRC=$(pwd)
cd
mkdir buildllvm
cd buildllvm

cmake -D CMAKE_BUILD_PARALLEL_LEVEL=16 -G "Unix Makefiles" -D CMAKE_BUILD_TYPE=Release $LLVM_SRC
cmake --build . --parallel 16
cmake --build . --parallel 16 --target install

# Install TTS
sudo apt-get install libsndfile1
sudo -iu tts

python3 -m venv venv
. venv/bin/activate
pip install wheel
pip install -r requirements.txt

# Test tts
sudo -iu tts
tts --text "This is a test"
