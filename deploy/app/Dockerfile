FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libsm6 \
    libxext6 \
    libxrender-dev

# Install python packages
RUN pip3 install --upgrade pip
RUN pip3 install numpy \
    scipy \
    scikit-learn \
    pandas
    
# Set working directory
WORKDIR /var/www/app

# Copy source code
COPY . .

# Run the app
CMD ["python3", "main.py"]