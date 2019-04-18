from django.core.management.base import BaseCommand, CommandError
from data.models import Sensor, Reading
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Verifica se houve algum envio durante a hora'

    def handle(self, *args, **options):
        now = datetime.now()
        lastHour = datetime.now() - timedelta(hours = 1)
        sensores = Sensor.objects.all()
        for sensor in sensores:
            if(sensor.score > 0):
                try:
                    x = Reading.objects.filter(sensor_id__exact=sensor.id, moment__gte=lastHour).latest('moment')
                except:
                    sensor.score /= 2
                    sensor.save()
