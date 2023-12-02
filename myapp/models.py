from django.db import models

class Mchango(models.Model):
    mchango_name = models.CharField(max_length=100)
    beneficiary_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    unique_link = models.CharField(max_length=100, unique=True)  # Unique link for each mchango

    def __str__(self):
        return self.mchango_name


class Contribution(models.Model):
    mchango = models.ForeignKey(Mchango, on_delete=models.CASCADE)
    contributor_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contributed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor_name} - {self.mchango}"

