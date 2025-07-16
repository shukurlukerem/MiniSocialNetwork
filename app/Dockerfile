# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install fastapi uvicorn
# RUN pip install  -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
