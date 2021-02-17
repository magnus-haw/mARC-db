from django.conf import settings
import mARC.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
import django
django.setup()
from data.models import *
from stats.models import *
from stats.views import *
import numpy as np

app = Apparatus.objects.all().last()
updateRunUsage(app)
