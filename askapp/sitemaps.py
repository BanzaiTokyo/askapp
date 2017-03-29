from django.contrib.sitemaps import Sitemap
from askapp.models import Thread, User
from django.template.defaultfilters import slugify


class ThreadSitemap(Sitemap):
    """
    This class generates sitemap subset for thread URLs
    https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/#sitemap-classes
    """

    # Check attributes and methods destination (except items) at https://www.sitemaps.org/protocol.html#urlsetdef
    changefreq = "never"

    priority = 0.5

    def items(self):
        return Thread.objects.filter(deleted=False).order_by('-created')

    def lastmod(self, obj):
        return obj.created

    def location(self, obj):
        return '/thread/{}/{}/'.format(obj.id, slugify(obj))


class ProfileSitemap(Sitemap):
    """
    This class generates sitemap subset for profile URLs
    """
    changefreq = "never"
    priority = 0.5

    def items(self):
        return User.objects.filter(is_active=True).order_by('-date_joined')

    def lastmod(self, obj):
        return obj.date_joined

    def location(self, obj):
        return '/profile/{}/{}/'.format(obj.id, slugify(obj))

# this is a dictionary of the site sitemaps. Since our sitemap includes dynamic content, it can be large enough and
# overboard the standard limit of 50,000 entries (https://www.sitemaps.org/protocol.html#index). Hence we split the
# sitemap into two lists: threads and profiles and create an index file.
# https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/#creating-a-sitemap-index
sitemap_dict = {
    'threads': ThreadSitemap,
    'profiles': ProfileSitemap,
}