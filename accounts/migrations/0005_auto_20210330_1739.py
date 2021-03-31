# Generated by Django 3.1.7 on 2021-03-30 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]