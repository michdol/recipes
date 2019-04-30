from django.db import migrations, models
from django.utils import timezone
import django.db.models.deletion
from scrapers.constants import SCRAPER_NAME_TASTY


def insert_scraper(apps, schema_editor):
    SourceWebsite = apps.get_model('recipes', 'SourceWebsite')
    source = SourceWebsite.objects.create(name='Tasty', url='https://tasty.co')
    Scraper = apps.get_model('scrapers', 'Scraper')
    ScraperLog = apps.get_model('scrapers', 'ScraperLog')
    scraper = Scraper.objects.create(name=SCRAPER_NAME_TASTY, source_id=source.id)
    yesterday = timezone.now() - timezone.timedelta(days=1)
    ScraperLog.objects.create(scraper=scraper, started=yesterday, finished=yesterday)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scrapers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_scraper)
    ]
