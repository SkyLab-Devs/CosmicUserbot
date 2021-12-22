FROM ghcr.io/qubitdimensions/fizilion:squashed
RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/FrosT2k5/ProjectFizilion -b demon /Fizilion
WORKDIR /Fizilion
CMD ["python3","-m","userbot"]
