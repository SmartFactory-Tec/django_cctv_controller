# IP Security Camera Management Backend with Django

This Django backend application is designed to manage IP security cameras, facial recognition and handle API calls, particularly for processing Real-Time Streaming Protocol (RTSP) streams.

## Getting Started

### Setting up the Virtual Environment

To ensure a clean and isolated environment, create and activate a virtual environment using the following commands:

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### Installing Project Dependencies

Install the necessary project dependencies by running the command:

```bash
pip install -r requirements.txt
```

### Setting Up Redis via WSL

Redis is not officially supported on Windows, but you can install it through the Windows Subsystem for Linux (WSL). Here are the steps to get Redis running on WSL:

1. **Enable WSL2**

    Microsoft provides detailed instructions for installing WSL. You can follow this guide [here](https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview) and take note of the default Linux distribution it installs. This guide assumes the default distribution to be Ubuntu.

2. **Install Redis on WSL**

   Once you're running Ubuntu on Windows, follow the steps below to install recent stable versions of Redis from the official `packages.redis.io` APT repository:

   ```bash
   curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

   echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

   sudo apt-get update
   sudo apt-get install redis
   ```

3. **Start the Redis Server**

   Start the Redis server using the following command:

   ```bash
   sudo service redis-server start
   ```

4. **Connect to Redis**

    You can test that your Redis server is running by connecting with the Redis CLI:

    ```bash
    redis-cli 
    127.0.0.1:6379> ping
    PONG
    ```

### Make Django migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running the Development Server

Redis is required for the server to run properly. After installing the dependencies, you can start the development server using the command:

```bash
python manage.py runserver
```