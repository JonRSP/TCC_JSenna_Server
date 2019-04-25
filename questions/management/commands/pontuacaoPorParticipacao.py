from django.core.management.base import BaseCommand, CommandError
from data.models import Sensor, Reading
from datetime import datetime, timedelta
from questions.models import *

class Command(BaseCommand):
    help = 'Verifica a cada hora se houve envio de respostas psicologicas'

    def handle(self, *args, **options):
        now = datetime.now()
        lastHour = datetime.now() - timedelta(hours = 1)
        try:
            sensores = Sensor.objects.all()
            for sensor in sensores:
                if(float(sensor.score) > 2.5):
                    score = 0
                    try:

                        count = 0
                        questions = Questions.objects.filter(questionKind__description = 'Psicologica', sensorKind__sensors = sensor.id)
                        for question in questions:
                            count += 1
                            try:
                                answerDic = {}
                                answers = Answers.objects.filter(question__id__exact = question.id, moment__gte=lastHour,sensor__id__exact=sensor.id)
                                for answer in answers:
                                    if(str(answer.answer) in answerDic):
                                        answerDic[answer.answer] += 1
                                    else:
                                        answerDic.update({answer.answer:1})
                                score += self.score(answerDic)
                            except:
                                pass
                        score /= float(count)
                    except:
                        pass
                    if (float(score) >= 1 and (float(sensor.score) * 1.05) < 5):
                        if score < 1.9:
                            sensor.score *= 1.01
                            sensor.save()
                        elif score >= 1.9:
                            sensor.score = float(sensor.score) * 1.05
                            sensor.save()
        except:
            pass

    def score(self, dic):
        total = 0
        for element in dic:
            total += dic[element]
        for element in dic:
            dic[element] /= total
            if dic[element] > 0.9:
                return 2
                break
            elif dic[element] > 0.5:
                return 1
                break
