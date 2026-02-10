from django.db import models

class SecurityIncident(models.Model):
    # Definimos las opciones para la severidad
    class Severity(models.TextChoices):
        LOW = 'LOW', 'Baja'
        MEDIUM = 'MEDIUM', 'Media'
        HIGH = 'HIGH', 'Alta'

    title = models.CharField(max_length=200)
    description = models.TextField()
    
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.MEDIUM,
    )
    
    detected_at = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"