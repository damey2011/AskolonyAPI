# Generated by Django 2.0.1 on 2018-05-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(default='http://', max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='college',
            field=models.CharField(blank=True, default='NA', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_link',
            field=models.URLField(blank=True, default='http://facebook.com', max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lives',
            field=models.CharField(blank=True, default='NA', max_length=400),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter_link',
            field=models.URLField(blank=True, default='http://twitter.com', max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='works',
            field=models.CharField(blank=True, default='NA', max_length=200),
        ),
    ]
