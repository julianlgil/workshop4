FROM python:3.11.2

WORKDIR /app
COPY . /app
RUN make install-pipenv &&  \
    make deps

HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:$APP_PORT/health || exit 1

EXPOSE $APP_PORT
CMD ["make", "start"]
