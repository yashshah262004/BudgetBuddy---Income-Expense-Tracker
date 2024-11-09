from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Source

@receiver(user_logged_in)
def attach_default_sources(sender, user, request, **kwargs):
    default_sources = ['Salary', 'Freelancing', 'Investments', 'Gifts', 'Business', 'Bonuses', 'Stock Trading', 'Side Jobs', 'Other']  # Example default sources
    existing_sources = Source.objects.filter(name__in=default_sources)

    # Add default sources if they don't exist
    if not existing_sources.exists():
        for source_name in default_sources:
            Source.objects.create(name=source_name)
