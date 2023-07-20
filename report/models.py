from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    # Add other client-related fields

class Requisition(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    officer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requisitions')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisions', null=True, blank=True)
    management_signed_off = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # Add other requisition-related fields

class Deposit(models.Model):
    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other deposit-related fields

class Engagement(models.Model):
    requisition = models.OneToOneField(Requisition, on_delete=models.CASCADE)
    remaining_payment = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other engagement-related fields

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username  # Display the username as the object representation
