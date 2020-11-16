from django.core.management.base import BaseCommand

import subprocess
import os


class Command(BaseCommand):
    help = 'Run migrate all db'

    def handle(self, *args, **options):
        migrate_sh_file = os.path.abspath(os.path.dirname(__file__)) + '/migrate_all.sh'
        print(migrate_sh_file)
        subprocess.call(['sh', migrate_sh_file])
