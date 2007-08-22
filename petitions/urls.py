from django.conf.urls.defaults import *
from petitions.models import Petition, Signature
from petitions.feeds import RssFeed, AtomFeed
from django.conf import settings
    
feeds = { 
    'rss': RssFeed,
    'atom': AtomFeed,
}

petition_dict = {
    'model': Petition,
    'base_url': '/petitions/',
}

signature_dict = {
    'model': Signature,
    'base_url': '/petitions/signatures/',
}

urlpatterns = patterns('',
    (r'^rss/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'rss'}),
    (r'^atom/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url': 'atom'}),
)
        
urlpatterns += patterns('sorted_paginated_authored_archived_list_view.views',
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'sorted_paginated_authored_archived_list', petition_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'sorted_paginated_authored_archived_list', petition_dict),
    (r'^(?P<year>\d{4})/$', 'sorted_paginated_authored_archived_list',  petition_dict),
    (r'^$', 'sorted_paginated_authored_archived_list', petition_dict),
    (r'^signatures/$', 'sorted_paginated_authored_archived_list', signature_dict),
    # if signatures were really archived there would be more urls here
)

urlpatterns += patterns('django.views.generic.create_update',
    (r'^create/$', 'create_object', dict(model=Petition, login_required=True, extra_context={'STATE_DEFAULT': settings.STATE_DEFAULT})),
)

urlpatterns += patterns('petitions.views',
    (r'^(?P<slug>[-\w]+)/$', 'petition_detail', dict(queryset=Petition.published_objects.all(), date_field='pub_date', slug_field='slug')),
)
