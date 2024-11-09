from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Category

@receiver(user_logged_in)
def attach_default_categories(sender, user, request, **kwargs):
    default_categories = ['Food', 'Travel', 'Bills', 'Shopping', 'Groceries', 'Rent', 'Utilities', 'Health & Fitness', 'Education', 'Loans & Debts', 'Clothing', 'Emergency', 'Other']  # Example categories
    existing_categories = Category.objects.filter(name__in=default_categories)

    # Add default categories if they don't exist for this user
    if not existing_categories.exists():
        for category_name in default_categories:
            Category.objects.create(name=category_name)
