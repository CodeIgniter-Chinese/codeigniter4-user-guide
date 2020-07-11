FROM python:3-alpine

LABEL maintainer="hex@codeigniter.org.cn"

COPY ./requirements.txt /

WORKDIR /ci

VOLUME /ci

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache make \
    && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt \
    && echo "cd /ci && make html" > /make.sh

CMD [ "sh", "/make.sh" ]
