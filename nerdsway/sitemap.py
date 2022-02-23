from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from blog.models import Blog

class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['home:index', 'home:about', 'home:subscribe', 'home:unsubscribe', 'home:contact', 'home:rss_feed', 'home:faqs', 'home:privacy_policy', 'home:terms']
    
    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Blog.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at