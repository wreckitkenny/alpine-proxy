FROM python:3.12.9-alpine
LABEL authors="wiky"
WORKDIR /app
COPY . .
RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install fastapi[standard]
RUN pip install -r requirements.txt
ENTRYPOINT ["fastapi", "run"]