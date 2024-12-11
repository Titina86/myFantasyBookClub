# Generated by Django 5.0.4 on 2024-12-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksList', '0003_bookslist_have_journal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookslist',
            name='read_status',
            field=models.CharField(choices=[('Wish List', 'Wish List'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Wish List', max_length=15),
        ),
    ]