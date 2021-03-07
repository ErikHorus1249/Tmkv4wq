FROM alpine:latest

RUN apk add --update tftp-hpa syslinux && \
    cp -r /usr/share/syslinux /tftpboot && \
    find /tftpboot -type f -exec chmod 0444 {} +

EXPOSE 69/udp

ENTRYPOINT ["in.tftpd"]
CMD ["--foreground", "--verbose", "--secure", "/tftpboot"]
