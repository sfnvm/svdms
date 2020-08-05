from django.db import models
from django.conf import settings


class Agency(models.Model):
    class Meta:
        db_table = 'agency'

    # auto field
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=False,
        related_name="%(class)s_created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Tài khoản chủ sỡ hữu đại lý // Chú ý role khi gán user
    user_related = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_owned_by"
    )

    code = models.CharField(max_length=32, unique=True, blank=True)
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)

    # Constants priority levels
    EMERGENCY = 'EM'        # RP: < 1 hour
    URGENT = 'UR'           # RP: 24 hours
    STANDARD = 'ST'         # RP: 7 days
    NORMAL = 'NO'           # RP: Agreed date
    PRIORITY_CHOICES = (
        (EMERGENCY, 'Emergency'),
        (URGENT, 'Urgent'),
        (STANDARD, 'Standard'),
        (NORMAL, 'Normal')
    )
    priority_level = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        default=NORMAL
    )

    # permission required
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
        related_name="%(class)s_removed_by"
    )

    def __str__(self):
        return self.code
