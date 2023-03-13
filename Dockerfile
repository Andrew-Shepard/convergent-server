# Dockerfile
FROM python:3.8.15-bullseye

ARG IMAGE_NAME="convergent"
ARG VER_PYTHON=""
ARG VER_PIP=""
# TODO: Fix s6 exec permissions to get rid of root
USER root
WORKDIR /app

# Dependencies
COPY requirements.txt /app/
COPY utility/install_packages.sh /tmp
COPY utility/db_init.sh /tmp

RUN  chmod +x /tmp/install_packages.sh
RUN  /tmp/install_packages.sh

RUN pip3 install \
    --disable-pip-version-check \
--no-cache-dir \
    --no-deps \
    --require-hashes \
    --requirement requirements.txt

# S6 setup
ENV S6_OVERLAY_VERSION=3.1.2.1
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# Behavior 2 = crash
ENV SRC_DEF_DIR=/etc/s6-overlay/s6-rc.d \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2

ADD . /app

RUN set -o nounset -o errexit -o xtrace -o verbose \
    \
    && addgroup --system convergent \
    && adduser --disabled-password --system --home /app --shell /sbin/nologin --ingroup convergent convergent \
    && mkdir ${SRC_DEF_DIR}/convergent \
    && touch ${SRC_DEF_DIR}/user/contents.d/convergent \ 
    && cp utility/s6-type ${SRC_DEF_DIR}/convergent/type \
    && cp utility/convergent-run.sh ${SRC_DEF_DIR}/convergent/run \
    && cp utility/convergent-finish.sh ${SRC_DEF_DIR}/convergent/finish


EXPOSE 8000


ENTRYPOINT ["/init"]

ARG GIT_COMMIT=""
ARG GIT_COMMIT_DATE=""
ARG BUILD_DATE=""

ENV IMAGE_NAME="$IMAGE_NAME" \
    VER_PYTHON="$VER_PYTHON" \
    VER_PIP="$VER_PIP" \
    GIT_COMMIT="$GIT_COMMIT" \
    GIT_COMMIT_DATE="$GIT_COMMIT_DATE"