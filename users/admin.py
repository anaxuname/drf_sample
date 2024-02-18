from django.contrib import admin

from users.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "paid_course", "paid_lesson")
