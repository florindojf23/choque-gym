from django.db import models
from custom.models import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your models here.

class Member(models.Model):
    nu_id = models.CharField(max_length=20,unique=True,null=True)
    naran = models.CharField(max_length=200,null=True)
    sexo = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')],max_length=10,null=True,blank=True)
    naturalidade = models.CharField(max_length=200,null=True,blank=True)
    data_moris = models.DateField(null=True)
    join_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    enderesu = models.CharField(max_length=200,null=True,blank=True)
    municipio = models.ForeignKey(Municipality, on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(choices=[('Solteiru/a','Solteiru/a'),('Marridu/a','Marridu/a')],max_length=10,null=True,blank=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    fotografia = models.ImageField(upload_to='images/',null=True, blank=True)
    documentos = models.FileField(upload_to='CV/', null=True, blank=True)

    def __str__(self):
        return self.naran

    def get_age(self):
        import datetime
        age = datetime.date.today().year-self.data_moris.year
        return age

    def get_duration_in_months(self):
        if self.end_date:
            delta = relativedelta(self.end_date, self.join_date)
            return delta.years * 12 + delta.months
        else:
            return None

class GymClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.CharField(max_length=150)
    payment_per_month = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)

    def get_schedule(self):
        return f"{self.days_of_week} {self.start_time} - {self.end_time}"

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.naran} enrolled in {self.gym_class.name}"

    def get_total_payment(self):
        duration_in_months = self.member.get_duration_in_months()
        if duration_in_months is not None:
            return duration_in_months * self.gym_class.payment_per_month
        else:
            return None
