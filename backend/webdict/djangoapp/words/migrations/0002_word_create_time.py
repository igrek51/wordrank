from django.db import migrations, models
import webdict.djangoapp.words.time


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='create_time',
            field=models.DateTimeField(default=webdict.djangoapp.words.time.now),
        ),
    ]
