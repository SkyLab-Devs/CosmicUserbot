FROM ghcr.io/qubitdimension/fizilion:squashed
RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/FrosT2k5/ProjectFizilion -b demon /Fizilion
WORKDIR /Fizilion
RUN pip3 install duckduckgo_search
CMD ["python3","-m","userbot"]
