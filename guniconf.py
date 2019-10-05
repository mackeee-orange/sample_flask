"""
For Production only
"""

import multiprocessing
import os

# Server Socket
bind = 'unix:{}/tmp/sockets/ghidorah_gunicorn.sock'.format(os.getcwd())
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2
debug = False
spew = False

# Logging
logfile = '/var/www/ghidorah/log/production.log'
loglevel = 'info'
logconfig = None

# Process Name
proc_name = 'ghidorah_production'