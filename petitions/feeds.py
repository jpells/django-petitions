from petitions.models import Petition
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings

class RssFeed(Feed):
    title = _("Petitions")
    link = "/petitions/" 
    description = _("Petitions")
    def items(self):
        return Petition.published_objects.all().order_by('-pub_date')[:5]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
