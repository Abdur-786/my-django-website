import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('energy_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='energyusage',
            name='user_ID',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='energy_usages',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='energygoal',
            name='user_ID',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='energy_goals',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
