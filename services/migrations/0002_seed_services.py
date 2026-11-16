from django.db import migrations


def seed_services(apps, schema_editor):
    ServiceType = apps.get_model('services', 'ServiceType')
    for name in ('Consultation', 'Installation'):
        ServiceType.objects.get_or_create(service_name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services, migrations.RunPython.noop),
    ]
