from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from mainapp.models import Products, Article, Reviews, Flowers, Pack, Decoration


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['index', 'catalog', 'blog', 'designer']

    def location(self, item):
        return reverse('mainapp:' + item)


class ProductsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Products.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        return reverse('mainapp:catalog')


class ArticleSitemap(Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('mainapp:blog')


class ReviewsSitemap(Sitemap):
    priority = 0.4
    changefreq = 'monthly'

    def items(self):
        return Reviews.objects.filter(is_active='published')

    def location(self, obj):
        return reverse('mainapp:index')

    def lastmod(self, obj):
        return obj.created_at


class FlowersSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Flowers.objects.all()

    def location(self, obj):
        return reverse('mainapp:designer')


class PackSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Pack.objects.all()

    def location(self, obj):
        return reverse('mainapp:designer')


class DecorationSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Decoration.objects.all()

    def location(self, obj):
        return reverse('mainapp:designer')
