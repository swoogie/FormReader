from pathlib import Path


def getLoggerConfig():
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    if not logs_dir.exists():
        logs_dir.mkdir()

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(logs_dir / 'app.log'),
                'maxBytes': 10485760,
                'backupCount': 10,
                'formatter': 'detailed'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['file', 'console']
        }
    }
