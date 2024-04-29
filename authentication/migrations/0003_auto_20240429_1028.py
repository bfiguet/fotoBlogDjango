# Generated by Django 5.0.4 on 2024-04-29 10:28
from django.core.management.sql import emit_post_migrate_signal

from django.db import migrations

def create_groups(apps, schema_migration):
	emit_post_migrate_signal(verbosity=1, interactive=False, db='default')
	
	User = apps.get_model('authentication', 'User')
	Group = apps.get_model('auth', 'Group')
	Permission = apps.get_model('auth', 'Permission')

	add_photo = Permission.objects.get(codename='add_photo')
	change_photo = Permission.objects.get(codename='change_photo')
	delete_photo = Permission.objects.get(codename='delete_photo')
	view_photo = Permission.objects.get(codename='view_photo')

	creator_permissions = [
		add_photo,
		change_photo,
		delete_photo,
		view_photo,
	]

	creators = Group(name='creators')
	creators.save()

	creators.permissions.set(creator_permissions)

	subscribers = Group(name='subscribers')
	subscribers.save()
	subscribers.permissions.add(view_photo)

	for user in User.objects.all():
		if user.role == 'CREATOR':
			creators.user_set.add(user)
		if user.role == 'SUBSCRIBER':
			subscribers.user_set.add(user)

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_profile_photo_alter_user_role'),
    ]

    operations = [
		migrations.RunPython(create_groups)
    ]