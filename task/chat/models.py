
# Create your models here.
from chat.managers import ThreadManager
from django.db import models
from django.contrib.auth.models import User

class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField('auth.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'

class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'



class Chatroom(models.Model):
    superuser=models.ForeignKey(User, on_delete=models.CASCADE , related_name="superuser")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

def get_or_create_personal_thread(superuser, user):
    threads = Chatroom.objects.get(superuser=superuser, user=user)
    if threads:
        return threads.id
    else:
        threads=Chatroom.objects.create(superuser=superuser, user=user)
    return threads.id