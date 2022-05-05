FROM ghcr.io/skylab-devs/cosmic:squashed
RUN mkdir /cosmos && chmod 777 /cosmos && git clone https://github.com/SkyLab-Devs/CosmicUserbot -b starfire /cosmos
RUN dnf -y install pv jq
WORKDIR /cosmos
CMD ["python3","-m","userbot"]
