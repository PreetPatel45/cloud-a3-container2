FROM python:3.9-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY app2.py .

CMD ["python", "app2.py"]