import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from backend.models import Meme


class Command(BaseCommand):
    help = 'Добавить мемы в датасет'

    def handle(self, *args, **options):
        file = os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'data.csv')
        with open(file) as f_obj:
            arr = []
            reader = csv.DictReader(f_obj, delimiter=';')
            for line in reader:
                arr += [ Meme(photo=line["photo"], author=line["author"], important=True if line["important"] == '1' else False) ]
        Meme.objects.bulk_create(arr)
        print("Мемы успешно добавлены!")