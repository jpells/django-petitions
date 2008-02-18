"""
Convenience module for access of custom petitions application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

_ = lambda s: s

# The choices for state of a Petition/Signature
STATE_CHOICES = getattr(settings, 'STATE_CHOICES', (
    ('1', _('Draft')),
    ('2', _('Published')),
    ('3', _('Inactive')),
))

# The default state when a Petition/Signature is created
STATE_DEFAULT = getattr(settings, 'STATE_DEFAULT', 3)

# The state of a Published Petition/Signature
STATE_PUBLISHED = getattr(settings, 'STATE_PUBLISHED', 2)

# The choices of a Signature
PETITION_SIGNATURE_CHOICES = getattr(settings, 'PETITION_SIGNATURE_CHOICES', (
    ('Y', _('Yay')),
    ('N', _('Nay')),
))