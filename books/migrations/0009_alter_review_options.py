# Generated by Django 4.0.10 on 2024-05-14 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_review_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'permissions': [('can_add_review', 'Can add reviews nolimit')]},
        ),
    ]