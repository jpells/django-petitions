from django.contrib.auth.models import User
from django.db import models
from petitions import settings
from tagging.fields import TagField
from published_manager.managers import PublishedManager
from django.utils.translation import ugettext as _

class Petition(models.Model):
    """
    A petition 
    """
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(prepopulate_from=('title',), unique=True, verbose_name=_("Slug Field"))
    user = models.ForeignKey(User, verbose_name=_("User"))
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Published"))
    description = models.TextField(verbose_name=_("Description"))
    state = models.CharField(max_length=1, choices=settings.STATE_CHOICES, default=settings.STATE_DEFAULT, verbose_name=_("State of object"))
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))
    tags = TagField(help_text=_("Enter key terms seperated with a space that you want to associate with this Petition"), verbose_name=_("Tags"))
    objects = models.Manager()
    published_objects = PublishedManager()

    def get_absolute_url(self):
        return "/petitions/%s/" % self.slug

    def __str__(self):
        return _(self.title)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Petition")
        verbose_name_plural = _("Petitions")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('title', 'user')
        ordering = ['pub_date']
        search_fields = ['title', 'description']
        fields = (
            (None, {
                'fields': ('title', 'description', 'user', 'ip_address')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('state', 'slug', 'pub_date')
            }),
        )

class Signature(models.Model):
    """
    A signature 
    """
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Published"))
    mod_date = models.DateTimeField(auto_now=True, verbose_name=_("Date Modified"))
    user = models.ForeignKey(User, verbose_name=_("User"))
    petition = models.ForeignKey(Petition, verbose_name=_("Petition"))
    vote = models.CharField(max_length=1, choices=settings.PETITION_SIGNATURE_CHOICES, verbose_name=_("Vote"))
    comment = models.TextField(verbose_name=_("Comment"))
    state = models.CharField(max_length=1, choices=settings.STATE_CHOICES, default=settings.STATE_DEFAULT, verbose_name=_("State of object"))
    ip_address = models.IPAddressField(verbose_name=_("Author's IP Address"))
    objects = models.Manager()
    published_objects = PublishedManager()

    def get_absolute_url(self):
        return "/petitions/%s/#signature_%d" % (self.petition.slug, self.id)

    def __str__(self):
        return _(self.vote + " " + self.comment)

    class Meta:
        unique_together = (("user", "petition"),)
        ordering = ['pub_date']
        get_latest_by = "pub_date"
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")

    class Admin:
        date_hierarchy = 'pub_date'
        list_display = ('petition', 'vote')
        ordering = ['pub_date']
        search_fields = ['comment']
        fields = (
            (None, {
                'fields': ('petition', 'vote', 'comment', 'user', 'ip_address')
            }),
            (_('Advanced settings'), {
                'classes': 'collapse',
                'fields' : ('state', 'pub_date', 'mod_date')
            }),
        )
