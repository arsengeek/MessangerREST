# Generated by Django 5.0.6 on 2024-07-16 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messangerREST', '0008_remove_message_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessanger',
            name='room',
            field=models.ManyToManyField(related_name='room', to='messangerREST.room'),
        ),
    ]
