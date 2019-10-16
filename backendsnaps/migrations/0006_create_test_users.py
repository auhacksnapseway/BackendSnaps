from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_test_users(apps, schema_editor):
    User = apps.get_model("backendsnaps", "User")

    u, _ = User.objects.get_or_create(username="Spectator")
    u.password = make_password("secret")
    u.save()

    User.objects.get_or_create(username="test")


class Migration(migrations.Migration):

    dependencies = [("backendsnaps", "0005_auto_20190406_2141")]

    operations = [migrations.RunPython(create_test_users)]
