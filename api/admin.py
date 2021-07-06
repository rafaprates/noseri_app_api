from django.contrib import admin
from .models import Load, Kwh, BillingInfo

# Register your models here.
# Os modelos aqui registrados aparecerão em /admin

admin.site.register(Load)
admin.site.register(Kwh)
admin.site.register(BillingInfo)


