from django.contrib import admin
from .models import SecurityIncident

# Opción simple:
# admin.site.register(SecurityIncident)

# Opción recomendada (para que la lista se vea mejor en la captura):
@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'detected_at')