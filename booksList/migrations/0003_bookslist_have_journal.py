# Generated by Django 5.0.4 on 2024-12-06 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksList', '0002_alter_bookslist_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslist',
            name='have_journal',
            field=models.BooleanField(default=False),
        ),
    ]
