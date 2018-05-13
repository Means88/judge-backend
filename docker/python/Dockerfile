FROM python:2.7-alpine

COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

RUN adduser -s /bin/sh -D judge

CMD ["/bin/sh", "/entrypoint.sh"]

