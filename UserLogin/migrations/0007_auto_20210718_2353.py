# Generated by Django 2.2.24 on 2021-07-18 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0006_auto_20210718_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='hearing',
            field=models.IntegerField(choices=[(0, ''), (1, '可'), (2, '応相談')], default=0, verbose_name='聴覚障碍対応'),
        ),
        migrations.AddField(
            model_name='shop',
            name='price_basic',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='基本料金'),
        ),
        migrations.AddField(
            model_name='shop',
            name='visually',
            field=models.IntegerField(choices=[(0, ''), (1, '可'), (2, '応相談')], default=0, verbose_name='視覚障碍対応'),
        ),
        migrations.AddField(
            model_name='shop',
            name='wheelchair',
            field=models.IntegerField(choices=[(0, ''), (1, '可'), (2, '応相談')], default=0, verbose_name='車イス対応'),
        ),
    ]