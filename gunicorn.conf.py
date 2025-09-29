# Gunicorn configuration file
bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
timeout = 300  # 5 minutes for long-running requests
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
reload = True