from django.contrib.sitemaps import Sitemap

from mainapp.models import Article


class KbankSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Article.objects.all()
