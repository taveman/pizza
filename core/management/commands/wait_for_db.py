import time
import sys

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Waiting for database to go live
    """
    def handle(self, *args, **options):
        pg_conn = None
        while not pg_conn:
            try:
                pg_conn = connections['default']
            except OperationalError:
                time.sleep(1)
        sys.stdout.write('Database is UP\n')
