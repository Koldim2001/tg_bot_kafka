# Use the official Python image as base
FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt-get install -y libusb-1.0-0

# Set working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory into the container
COPY . .

# Command to run your Python script
CMD ["python", "bot.py"]