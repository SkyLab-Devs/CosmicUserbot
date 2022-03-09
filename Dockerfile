FROM ghcr.io/skylab-devs/cosmic:squashed
RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/SkyLab-Devs/ProjectFizilion -b demon /Fizilion
WORKDIR /Fizilion
CMD ["python3","-m","userbot"]
