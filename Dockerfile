# 1) Pick a small Python base
FROM python:3.11-slim

# 2) Set your working directory
WORKDIR /app

# 3) Copy & install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 4) Copy your code
COPY . .

# 5) Expose and run
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
