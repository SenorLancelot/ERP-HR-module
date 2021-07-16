# Generated by Django 3.1.7 on 2021-07-16 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_auto_20210715_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavepolicies',
            name='id',
        ),
        migrations.RemoveField(
            model_name='leaves',
            name='id',
        ),
        migrations.RemoveField(
            model_name='leavesapplications',
            name='id',
        ),
        migrations.RemoveField(
            model_name='monthlyreports',
            name='id',
        ),
        migrations.AddField(
            model_name='leavepolicies',
            name='leavepolicy_id',
            field=models.CharField(default=2, max_length=50, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaves',
            name='leave_id',
            field=models.CharField(default=2, max_length=50, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leavesapplications',
            name='leaveapplication_id',
            field=models.CharField(default=2, max_length=50, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthlyreports',
            name='monthlyreport_id',
            field=models.CharField(default=2, max_length=50, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
