# Generated by Django 2.0.1 on 2018-03-26 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='note_type',
            field=models.CharField(choices=[('NF', 'New Follower'), ('NC', 'New Comment'), ('NM', 'New Message'), ('NR', 'New Reply'), ('NU', 'New Upvote'), ('ND', 'New Downvote'), ('NM', 'New Milestone'), ('NM', 'New Post')], max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='object_type',
            field=models.CharField(choices=[('P', 'Post'), ('U', 'User'), ('T', 'Topic'), ('C', 'Comment'), ('M', 'Message')], max_length=100),
        ),
    ]
