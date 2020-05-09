FROM xeffyr/termux:latest

RUN pkg update -y

COPY docker-static-dnd-hosts.txt /tmp
RUN cat /tmp/docker-static-dnd-hosts.txt >> /system/etc/static-dns-hosts.txt && \
    bash /system/bin/update-static-dns

RUN curl -LO https://its-pointless.github.io/setup-pointless-repo.sh && \
    bash setup-pointless-repo.sh && \
    rm setup-pointless-repo.sh && \
    pkg update -y

RUN pkg install -y python git nano scipy numpy

RUN pip install ipython

RUN pip install youtube-dl

RUN mkdir turmyx
WORKDIR turmyx

COPY . .
RUN pip install .
