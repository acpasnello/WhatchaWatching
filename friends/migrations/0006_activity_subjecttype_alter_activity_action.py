# Generated by Django 4.1.3 on 2023-01-23 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0005_alter_activity_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='subjecttype',
            field=models.CharField(choices=[('M', 'Movie'), ('S', 'Show')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='action',
            field=models.CharField(choices=[('rated', 'Rated'), ('reviewed', 'Reviewed'), ('added', 'Add to List'), ('watched', 'Watched'), ('created', 'Create new list')], max_length=30),
        ),
    ]
