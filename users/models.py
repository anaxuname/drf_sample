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

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class PaymentMethod(models.IntegerChoices):
    cash = 1, "Cash"
    transfer_to_bank = 2, "Transfer"
    acquiring = 3, "Acquiring"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    date = models.DateField(verbose_name="Payment date", auto_now_add=True)
    paid_course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, verbose_name="Paid Course")
    paymant_amount = models.FloatField(verbose_name="Payment amount")
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices, default=PaymentMethod.acquiring, verbose_name="Payment method"
    )
