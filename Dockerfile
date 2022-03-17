FROM ghcr.io/skylab-devs/cosmic:squashed
RUN dnf install -y aria2
RUN pip3 install aria2p
RUN mkdir /cosmos && chmod 777 /cosmos && git clone https://github.com/SkyLab-Devs/CosmicUserbot -b starfire /cosmos
WORKDIR /cosmos
CMD ["python3","-m","userbot"]
