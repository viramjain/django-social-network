# Generated by Django 2.2.3 on 2020-03-20 14:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(null=True, upload_to='{image\\')),
                ('subject', models.CharField(max_length=200)),
                ('msg', models.TextField(blank=True, null=True)),
                ('cr_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('single', 'single'), ('married', 'married'), ('widow', 'widow'), ('seprated', 'seprated'), ('commited', 'commited')], default='single', max_length=20)),
                ('age', models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(18)])),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^0?[5-9]{1}\\d{9}$')])),
                ('description', models.TextField(blank=True, null=True)),
                ('pic', models.ImageField(null=True, upload_to='image\\')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default='male', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField()),
                ('cr_date', models.DateTimeField(auto_now_add=True)),
                ('flag', models.CharField(blank=True, choices=[('racist', 'racist'), ('abbusing', 'abbusing')], max_length=20, null=True)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.MyProfile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.MyPost')),
            ],
        ),
        migrations.CreateModel(
            name='MyPostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cr_date', models.DateTimeField(auto_now_add=True)),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.MyProfile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.MyPost')),
            ],
        ),
        migrations.AddField(
            model_name='mypost',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.MyProfile'),
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myprofile', to='social.MyProfile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='social.MyProfile')),
            ],
        ),
    ]
