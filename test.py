from django.conf import settings
import mARC.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from data.models import *

import numpy as np

t = np.arange(0,5,.1)
ts = TimeSeries.objects.all()[0]