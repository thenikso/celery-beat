import os
import json
from datetime import timedelta

CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_SERIALIZER = os.environ.get('CELERY_TASK_SERIALIZER', 'json')

# Secrets setup
SECRETS_DIR = os.environ.get('SECRETS_DIR', '/secrets')
SECRETS = {}
if os.path.isdir(SECRETS_DIR):
    SECRETS_FILES = [f for f in os.listdir(SECRETS_DIR) if os.path.isfile(os.path.join(SECRETS_DIR, f))]
    for f in SECRETS_FILES:
        try:
            with open(os.path.join(SECRETS_DIR, f), 'r') as secret_file:
                secret_name = f.upper().replace('-','_')
                SECRETS[secret_name] = secret_file.read().strip()
        except:
            pass

BROKER_URL = SECRETS.get('CELERY_BROKER_URL', os.environ.get('CELERY_BROKER_URL', 'amqp://guest@rabbit'))

def s_k(k): return 'schedule' if k == 'timedelta' else k
def s_v(k, v): return timedelta(**v) if k == 'timedelta' else v
def s_parse(o): return {s_k(k): s_v(k, v) for k, v in o.items()}

CELERYBEAT_SCHEDULE = {t: s_parse(o) for t, o in json.loads(os.environ.get('CELERYBEAT_SCHEDULE', '{}')).items()}