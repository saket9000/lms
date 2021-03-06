# Generated by Django 2.1.7 on 2019-03-02 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_auto_20190301_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='passwordreset',
            name='userprofile',
        ),
        migrations.DeleteModel(
            name='PasswordReset',
        ),
    ]
