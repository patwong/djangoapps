import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')

    def was_published_recently(self):
        # returns True if the question was published within the last 24h
        # rhs: subtracts one day from the the current UTC time
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # end wpr()

    def __str__(self):
        return self.question_text
    # end str()
# end class


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    # end str()
# end Choice()

