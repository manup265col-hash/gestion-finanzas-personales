from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_passwordresetcode_pendingsignup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(max_length=8),
        ),
    ]

