# maintainer info
FROM alpine:latest
LABEL maintainer="carrergt@gmail.com"

# config container
RUN apk add py3-pip py3-wheel py3-jwt
RUN pip3 install fastapi uvicorn mysql-connector-python python-multipart

# config project
WORKDIR /app
COPY ./ ./
CMD ["sh","./start_prod_server"]
EXPOSE 9003
