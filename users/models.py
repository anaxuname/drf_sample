from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=50, verbose_name="Phone_number")
    city = models.CharField(max_length=50, default="Moscow", verbose_name="City")
    avatar = models.ImageField(upload_to="users", blank=True, null=True, verbose_name="Avater")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class OblateMethod(models.IntegerChoices):
    cash = 1, "Cash"
    transfer_to_bank = 2, "Transfer"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    date = models.DateField(verbose_name="Payment date")
    paid_course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, verbose_name="Paid Course")
    paid_lesson = models.ForeignKey("materials.Lesson", on_delete=models.CASCADE, verbose_name="Paid Lesson")
    paymant_amount = models.FloatField(verbose_name="Payment amount")
    oblate_method = models.IntegerField(
        choices=OblateMethod.choices, default=OblateMethod.cash, verbose_name="Oblate method"
    )
