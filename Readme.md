## Setting Up Redis

### Prerequisites

Ensure you have Redis installed on your system. If Redis is not installed, follow the below instructions.

### Installation

**Run the following commands in command line:**

```bash
sudo apt-get update
sudo apt-get install redis-server
```

### Starting Redis

**Start the Redis server with the following command:**

```bash
redis-server
```
Redis should start running on the default port 6379.

### Configuring Django Constance to Use Redis
Make sure the environment variables REDIS_HOST, REDIS_PORT, and REDIS_DB are set in your environment or .env file. For example, add the following to your .env file:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Setting Up Celery for Email Sending

### Configuration
We will be using redis as a broker for celery which we have already installed.
Set the CELERY_BROKER_URL in your .env file:
```bash
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
```
### Starting Redis

**Start the Redis server with the following command:**

```bash
redis-server
```
Redis should start running on the default port 6379.
### Starting Celery

Start Celery  by running the following command:

Run the following command in your project's root directory:

```bash
celery -A your_project_name worker --loglevel=info
```

Start Celery Beat  by running the following command:
```bash
celery -A your_project_name beat --loglevel=info
```

## Email Configuration

### Using a Gmail Account
To send emails using your Google account, you need to have 2-step verification enabled. If that is enabled follow these steps:

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords) and sign in with your Google account.
2. Enter a custom name for your app.
3. Google will generate a 16-character app password. Use this password in place of your usual Google account password in your app.

### Configuration
Set the following variables in your .env file and configure them according to your project.

```bash
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT='email port you want to use'
EMAIL_HOST_USER='your email@example.com'
EMAIL_HOST_PASSWORD='your app password'  # Use the 16-character app password here
```
