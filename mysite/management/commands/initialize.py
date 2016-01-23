# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from mysite.models import User, Pic, Question, Valid, Candidate, Var, Log, Exl, Text
import string,random


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        #设定超时60秒 进行最终评判
        Pic.objects.all().delete()
        User.objects.all().delete()
        Valid.objects.all().delete()
        Question.objects.all().delete()
        Var.objects.all().delete()
        Candidate.objects.all().delete()
        Exl.objects.all().delete()
        Log.objects.all().delete()
        Text.objects.all().delete()
        Var(name = "authkey", val = "10000").save()
        Var(name = "bind", val = "0").save()
        Var(name = "seed", val = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))).save()
        Text(id = 0, content = "").save()
        Text(id = 1, content = "").save()
        Text(id = 2, content = "").save()