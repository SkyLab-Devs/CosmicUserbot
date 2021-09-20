FROM ghcr.io/elytra8/fedora-docker:main

RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/FrosT2k5/ProjectFizilion -b demon /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

CMD ["python3","-m","userbot"]
