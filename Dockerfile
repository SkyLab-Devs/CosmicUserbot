FROM ghcr.io/skylab-devs/cosmic:squashed
RUN dnf install -y aria2
RUN pip3 install aria2p
RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/SkyLab-Devs/ProjectFizilion -b demon /Fizilion
WORKDIR /Fizilion
CMD ["python3","-m","userbot"]
