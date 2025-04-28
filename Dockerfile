# 1) Pick a small Python base
FROM python:3.11-slim  
# Using a lightweight official Python 3.11 image to keep the container small and efficient

# 2) Set your working directory
WORKDIR /app  
# Setting the working directory inside the container to '/app'

# 3) Copy & install Python deps
COPY requirements.txt .  
# Copying only requirements.txt first to leverage Docker layer caching
RUN pip install --upgrade pip \  
# Upgrading pip to the latest version
&& pip install -r requirements.txt  
# Installing all Python dependencies listed in requirements.txt

# 4) Copy your code
COPY . .  
# Copying all application files from the local directory to the container's '/app' directory

# 5) Expose and run
EXPOSE 80  
# Informing Docker that the container will listen on port 80 at runtime
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]  
# Command to start the FastAPI app using Uvicorn, binding to all interfaces on port 80
