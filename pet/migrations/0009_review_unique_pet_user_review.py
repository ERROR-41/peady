# Generated by Django 5.1.5 on 2025-05-16 04:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0008_review_user_alter_review_date_alter_review_pet'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('pet', 'user'), name='unique_pet_user_review'),
        ),
    ]
