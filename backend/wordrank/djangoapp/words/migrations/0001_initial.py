# Generated by Django 3.2.6 on 2022-03-22 15:41

from django.db import migrations, models
import django.db.models.deletion
import wordrank.djangoapp.words.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('definition', models.CharField(max_length=255)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dictionary_id', to='words.dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='words.user')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_id', to='words.word')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.CharField(default=wordrank.djangoapp.words.models.new_uuid, max_length=36, primary_key=True, serialize=False)),
                ('reversed_dictionary', models.BooleanField()),
                ('last_use', models.DateTimeField(blank=True, null=True)),
                ('rank_value', models.DecimalField(decimal_places=3, default=0, max_digits=6)),
                ('tries_count', models.IntegerField(default=0)),
                ('user_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_word_id', to='words.userword')),
            ],
        ),
        migrations.AddField(
            model_name='dictionary',
            name='source_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_language_id', to='words.language'),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='target_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_language_id', to='words.language'),
        ),
    ]
