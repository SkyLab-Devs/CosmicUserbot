# inherit prebuilt image
FROM ghcr.io/elytra8/fedora-docker:main

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

# clone repo
RUN git clone https://github.com/FrosT2k5/ProjectFizilion -b demon /Fizilion
#RUN git clone https://github.com/Senpai-sama-afk/ProjectFizilion -b dragon /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

#
# install required pypi modules
# If you want to install new packages, you can do it here
# example: pip install colorama
# note that this is just temporary and you installing package in docker image is proper way
#
RUN pip install --use-deprecated=legacy-resolver --use-feature 2020-resolver -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
