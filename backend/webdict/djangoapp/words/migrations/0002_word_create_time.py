from django.db import migrations, models
import wordrank.djangoapp.words.time


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='create_time',
            field=models.DateTimeField(default=wordrank.djangoapp.words.time.now),
        ),
    ]
