# Generated by Django 4.2.4 on 2023-08-10 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.IntegerField()),
                ('channel_limit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('usage', models.IntegerField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.channel')),
            ],
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.RemoveField(
            model_name='cookie',
            name='bot_id',
        ),
        migrations.AddField(
            model_name='bot',
            name='channels',
            field=models.ManyToManyField(related_name='bot_channels', to='dashboard.channel'),
        ),
        migrations.AddField(
            model_name='bot',
            name='cookies',
            field=models.ManyToManyField(related_name='bot_cookies', to='dashboard.cookie'),
        ),
    ]