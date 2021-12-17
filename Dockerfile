FROM ghcr.io/qubitdimension/fizilion:latest
RUN git clone https://github.com/FrosT2k5/ProjectFizilion -b demon /Fizilion
CMD ["python3","-m","userbot"]
