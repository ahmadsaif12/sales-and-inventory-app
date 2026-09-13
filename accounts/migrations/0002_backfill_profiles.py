from django.db import migrations


def create_missing_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("accounts", "Profile")
    for user in User.objects.filter(profile__isnull=True):
        Profile.objects.create(user=user)


def remove_orphan_profiles(apps, schema_editor):
    Profile = apps.get_model("accounts", "Profile")
    Profile.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles, remove_orphan_profiles),
    ]