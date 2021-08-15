from django.contrib import admin
from.models import Thread, Message, Chatroom
# Register your models here.
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(Chatroom)