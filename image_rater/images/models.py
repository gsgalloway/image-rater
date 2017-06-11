from random import randint

from django.db import models
from django.db.models.aggregates import Count
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


# Custom model manager to support fetching random Images
class ImageManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


@python_2_unicode_compatible
class Image(TimeStampedModel):
    image = models.ImageField(_('image'), upload_to='images', blank=False, null=False)
    name = models.CharField(_('Image Name'), blank=True, max_length=255, unique=False)

    objects = ImageManager()

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.image.url


@python_2_unicode_compatible
class ImagePresentation(TimeStampedModel):
    class Meta:
        unique_together = ['viewer', 'sequence_number']

    STATE_UNSEEN = 'unseen'
    STATE_SEEN = 'seen'
    STATE_SEEN_AND_LIKED = 'seen_and_liked'
    STATE_SEEN_AND_DISLIKED = 'seen_and_disliked'
    STATE_SEEN_AND_QUIT = 'seen_and_quit'
    STATE_CHOICES = (
        (STATE_UNSEEN, _('Unseen')),
        (STATE_SEEN, _('Seen')),
        (STATE_SEEN_AND_LIKED, _('Seen and liked')),
        (STATE_SEEN_AND_DISLIKED, _('Seen and disliked')),
        (STATE_SEEN_AND_QUIT, _('Seen and user quit')),
    )

    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=False, null=False)
    sequence_number = models.SmallIntegerField(blank=False, null=False)
    viewer = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False)
    state = models.CharField(_('state'), max_length=255, choices=STATE_CHOICES, default=STATE_UNSEEN)

    def __str__(self):
        return 'User: {}, Image: {}, SeqNo: {}'.format(self.viewer, self.image, self.sequence_number)
