# Generated by Django 4.0.5 on 2024-02-19 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_note', '0002_alter_note_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NoteUpdateHistory',
        ),
    ]
