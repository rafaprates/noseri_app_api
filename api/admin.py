from django.contrib import admin
from api.models import Load, Kwh, BillingInfo, Tax, UserLoadAssociation

# Register your models here.
# Os modelos aqui registrados aparecerão em /admin

admin.site.register(Load)
admin.site.register(Kwh)
admin.site.register(UserLoadAssociation)
admin.site.register(BillingInfo)
admin.site.register(Tax)


