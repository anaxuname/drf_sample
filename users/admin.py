from django.contrib import admin
from materials.models import Subscription

from users.models import Payment, User


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "paid_course")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "phone_number", "city")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "course")
