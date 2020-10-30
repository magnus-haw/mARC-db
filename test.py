from django.conf import settings
import mARC.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from data.models import *

import numpy as np

dgs = DiagnosticSeries.objects.all()
for dg in dgs:
    r = dg.run
    if len(dg.time.time) != len(dg.values):
        print(r.name, dg.name)