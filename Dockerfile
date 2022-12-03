ARG tag
FROM gitlab/gitlab-runner-helper:${tag}
RUN addgroup -g 1000 -S nonroot && \
    adduser -u 1000 -S nonroot -G nonroot
WORKDIR /home/Qbot
USER 1000:1000