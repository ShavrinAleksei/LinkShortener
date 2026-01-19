import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def create_alias():
    """Generate a random alias for short links."""
    while True:
        alias = uuid.uuid4().hex[:10]
        if not ShortLink.objects.filter(alias=alias).exists():
            return alias


class ShortLink(models.Model):
    url = models.URLField(max_length=2048, help_text="The original URL to shorten")
    alias = models.CharField(
        max_length=10,
        unique=True,
        default=create_alias,
        help_text="Short alias for the URL"
    )
    created_at = models.DateTimeField(default=timezone.now, help_text="When the short link was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the short link was last updated")
    clicks = models.PositiveIntegerField(default=0, help_text="Number of times the link was clicked")
    is_active = models.BooleanField(default=True, help_text="Whether the link is active")
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the link expires (optional)"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Short Link"
        verbose_name_plural = "Short Links"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('link_shortener:redirect', kwargs={'link_alias': self.alias})
    
    def __str__(self):
        return f"{self.alias} -> {self.url}"
    
    def clean(self):
        """Validate the model fields."""
        super().clean()
        if self.expires_at and self.expires_at < timezone.now():
            raise ValidationError("Expiration date cannot be in the past.")
    
    def is_expired(self):
        """Check if the link has expired."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at
    
    def increment_clicks(self):
        """Increment the click counter."""
        self.clicks += 1
        self.save(update_fields=['clicks', 'updated_at'])
