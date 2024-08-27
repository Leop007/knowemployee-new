# gunicorn.conf.py
# Non logging stuff
### Create directory and files in it and give it permission of user that is running the app as well, add log files to logrotatae ###
bind = "127.0.0.1:8005"
workers = 3
# Access log - records incoming HTTP requests
accesslog = "gunicorn/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "gunicorn/gunicorn.error.log"
# Whether to send Django output to the error log 
capture_output = True
# How verbose the Gunicorn error logs should be 
loglevel = "debug"