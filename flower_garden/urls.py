from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from flower_garden import settings

from django.contrib.sitemaps.views import sitemap
from mainapp.sitemaps import StaticViewSitemap, ProductsSitemap, ArticleSitemap, ReviewsSitemap, FlowersSitemap, \
    PackSitemap, DecorationSitemap

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('mainapp.urls', namespace='mainapp')),

    path('accounts/', include('authapp.urls', namespace='authapp')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
