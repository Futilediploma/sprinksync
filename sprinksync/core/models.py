from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('designer', 'Designer'),
        ('estimator', 'Estimator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

class Project(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)  # 👈 Add this line
    name = models.CharField(max_length=250)
    contractor = models.CharField(max_length=200)
    design_deadline = models.DateField()
    install_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    est_Labor_hours = models.DecimalField(max_digits=12, decimal_places=2)
    est_design_hours = models.DecimalField(max_digits=12, decimal_places=2)
    est_material_cost = models.DecimalField(max_digits=12, decimal_places=2)
    true_Labor_hours = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    true_design_hours = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    true_material_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name