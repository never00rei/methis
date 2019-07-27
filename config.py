import yaml
from os import getenv as getenv

HTTP_PORT = getenv('HTTP_PORT', 5000)
HTTP_ADDR = getenv('HTTP_ADDR', '0.0.0.0')
DEBUG = getenv('DEBUG', True)
THREADS_PER_PAGE = getenv('THREADS_PER_PAGE', 4)
CSRF_ENABLED = getenv('CSRF_ENABLED', True)
CSRF_SESSION_KEY = getenv('CSRF_SESSION_KEY','SECRET')

with open('data.yml','r') as f:
    DATA_SOURCE = yaml.load(f)