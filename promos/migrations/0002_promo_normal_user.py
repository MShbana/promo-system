# Generated by Django 3.1.7 on 2021-03-31 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_date_joined'),
        ('promos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='normal_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.normaluser'),
            preserve_default=False,
        ),
    ]