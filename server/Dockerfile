FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install wheel setuptools pip --upgrade
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
