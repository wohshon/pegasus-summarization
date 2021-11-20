FROM ubuntu:18.04
# Upgrade installed packages
RUN apt update && apt upgrade -y && apt clean
RUN apt-get install -y libhdf5-dev pkg-config
# install python 3.7.10 (or newer)
RUN apt update && \
    apt install --no-install-recommends -y build-essential curl software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.7 python3.7-dev python3.7-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*
# Register the version in alternatives (and set higher priority to 3.7)
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --force-reinstall && \
    rm get-pip.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
# RUN pip3 install --upgrade pip
RUN pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip3 install --upgrade  -r requirements.txt
COPY . /app
CMD [ "python3", "./app.py" ]
