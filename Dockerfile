FROM python:3-alpine

MAINTAINER Hex "hex@codeigniter.org.cn"

WORKDIR /ci

VOLUME /ci

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache make \
    && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple "sphinx==2.4.4" "sphinxcontrib-phpdomain==0.7.0" "jieba==0.42.1" \
    && echo "cd /ci/cilexer && python setup.py install > /dev/null 2>&1 && cd /ci && make html" > /make.sh

CMD [ "sh", "/make.sh" ]
