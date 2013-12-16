import os.path

from django.core.files.storage import FileSystemStorage
from django.conf import settings


read_storage = FileSystemStorage(location=settings.SCHEDULER_READ_DIR)
