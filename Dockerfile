FROM ghcr.io/skylab-devs/cosmic:squashed
RUN mkdir /cosmos && chmod 777 /cosmos && git clone https://github.com/SkyLab-Devs/CosmicUserbot -b starfire /cosmos
WORKDIR /cosmos
CMD ["bash","bot.sh"]
