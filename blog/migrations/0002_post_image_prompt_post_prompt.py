#0627 신규
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_prompt',
            field=models.CharField(default='Not created by AI', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='prompt',
            field=models.CharField(default='Not created by AI', max_length=200),
        ),
    ]