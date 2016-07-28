FROM gliderlabs/alpine:3.4

RUN addgroup user
RUN adduser user -D -G user
RUN chown -R user:user /home/user/
RUN mkdir -p /home/user/flask-image-resize


WORKDIR /home/user/flask-image-resize
ADD ./ /home/user/flask-image-resize/

RUN apk add --update python=2.7.12-r0 openssl ca-certificates py-pip libffi-dev openssl-dev \
    && pip install --upgrade pip \
    && apk --update add --virtual build-dependencies python-dev build-base \
    && pip install -r /home/user/flask-image-resize/requirements.txt \ 
    && rm -rf /root/.cache/ \
	&& apk del build-dependencies

EXPOSE 8888
ENTRYPOINT gunicorn project.main:app -c project.gunicorn
