# Generated by Django 4.2.4 on 2023-09-02 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_user_room_topic_room_host'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
