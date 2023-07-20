from django.contrib import admin
from .models import User, Client, Requisition, Deposit, Engagement

admin.site.register(Client)
admin.site.register(Requisition)
admin.site.register(Deposit)
admin.site.register(Engagement)
admin.site.register(User)