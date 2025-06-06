# Generated by Django 5.2.1 on 2025-06-01 01:12

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import users.models.user
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Nombre')),
                ('paternal_surname', models.CharField(blank=True, max_length=150, null=True, verbose_name='Apellido Paterno')),
                ('maternal_surname', models.CharField(blank=True, max_length=150, null=True, verbose_name='Apellido Materno')),
                ('phone', models.CharField(blank=True, max_length=150, null=True, verbose_name='Teléfono')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Biografía')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('avatar_image', models.ImageField(blank=True, default='usuarios/avatars/default.png', upload_to=users.models.user.avatar_upload_to, verbose_name='Avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=50, unique=True, verbose_name='Rol')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='roles', to='auth.group', verbose_name='Grupo')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'rol',
            },
        ),
        migrations.CreateModel(
            name='UserPrivacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_is_public', models.BooleanField(default=False, verbose_name='Email público')),
                ('phone_is_public', models.BooleanField(default=False, verbose_name='Teléfono público')),
                ('bio_is_public', models.BooleanField(default=True, verbose_name='Biografía pública')),
                ('username_or_name', models.CharField(choices=[('username', 'Nombre de usuario'), ('name', 'Nombre completo')], default='username', max_length=8, verbose_name='Nombre público')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='privacy', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Configuración de Privacidad del Usuario',
                'verbose_name_plural': 'Configuraciones de Privacidad de Usuarios',
                'db_table': 'user_privacy',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('github', 'GitHub'), ('linkedin', 'LinkedIn'), ('twitter', 'Twitter'), ('instagram', 'Instagram')], default='facebook', max_length=30, verbose_name='Plataforma')),
                ('link', models.URLField(verbose_name='Enlace')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Red Social',
                'verbose_name_plural': 'Redes Sociales',
                'db_table': 'social_media',
                'unique_together': {('user', 'platform')},
            },
        ),
        migrations.CreateModel(
            name='UserRol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_roles', to='users.rol', verbose_name='Rol')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Rol de Usuario',
                'verbose_name_plural': 'Roles de Usuario',
                'db_table': 'user_rol',
                'unique_together': {('user', 'rol')},
            },
        ),
    ]
