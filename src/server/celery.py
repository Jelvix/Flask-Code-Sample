from server.utils.celery_app_provider import get_celery_app_with_db

celery = get_celery_app_with_db()
