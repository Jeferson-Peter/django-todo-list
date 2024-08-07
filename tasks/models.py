from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('Pessoal', 'Pessoal'),
        ('Trabalho', 'Trabalho'),
        ('Outro', 'Outro'),
    ]

    PRIORITY_CHOICES = [
        ('Alta', 'Alta'),
        ('Média', 'Média'),
        ('Baixa', 'Baixa'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Outro')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Média')
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content


