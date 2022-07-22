FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt update

RUN apt install -y ffmpeg libsm6 libxext6 wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh


WORKDIR /python-docker


COPY environment.yml environment.yml
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "flask-streaming", "/bin/bash", "-c"]

COPY . .

EXPOSE 5000

CMD ["conda", "run", "--no-capture-output", "-n", "flask-streaming", "python3", "-m", "app"]

#USER root
#SHELL ["/bin/bash", "-c"]
#RUN . /root/.bashrc \
#    && /root/miniconda3/bin/conda init bash \
#    && /root/miniconda3/bin/conda env create -f environment.yml \
#    && /root/miniconda3/bin/conda activate flask-streaming
#CMD ["python3", "-m", "flask"]