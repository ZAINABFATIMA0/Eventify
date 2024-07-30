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
Ensure that your Django project is configured to use Redis by setting the following in your settings.py:

```bash
CONSTANCE_REDIS_CONNECTION = {
    'host': config('REDIS_HOST', default='localhost'),
    'port': config('REDIS_PORT', default=6379, cast=int),
    'db': config('REDIS_DB', default=0, cast=int),
}
CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
```

Make sure the environment variables REDIS_HOST, REDIS_PORT, and REDIS_DB are set in your environment or .env file. For example, add the following to your .env file:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Setting Up Celery for Email Sending

### Prerequisites
Ensure you have Celery installed on your system. If Celery is not installed, follow the below instructions.

### Insallation

Configure Celery in settings.py:
**Run the following commands in command line:**

```bash
pip install celery
```
### Configuration
We will be using redis as a broker for cwlwery which we have already installed and configured above.
Add the following Celery settings in your settings.py:
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

Start a Celery  by running the following command:

Run the following command in your project's root directory:

```bash
celery -A your_project_name worker --loglevel=info
```

## Email Configuration
