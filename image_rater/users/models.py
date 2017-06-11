from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from image_rater.images.models import Image, ImagePresentation


@python_2_unicode_compatible
class User(AbstractUser):
    ## Model field choices ##
    SEX_MALE = 'm'
    SEX_FEMALE = 'f'
    SEX_CHOICES = (
        (SEX_MALE, _('male')),
        (SEX_FEMALE, _('female')),
    )

    RACE_WHITE = 'white'
    RACE_BLACK = 'black'
    RACE_NATIVE_AMERICAN = 'native_american'
    RACE_ASIAN = 'asian'
    RACE_PACIFIC_ISLAND = 'pacific_island'
    RACE_CHOICES = (
        (RACE_WHITE, _('White')),
        (RACE_BLACK, _('Black')),
        (RACE_NATIVE_AMERICAN, _('American Indian/Alaska Native')),
        (RACE_ASIAN, _('Asian')),
        (RACE_PACIFIC_ISLAND, _('Native Hawaiian/Other Pacific Islander')),
    )

    ## Model fields ##
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    age = models.PositiveIntegerField(blank=False)
    sex = models.CharField(_('Sex'), blank=False, choices=SEX_CHOICES, max_length=1)
    race = models.CharField(_('Race'), blank=False, choices=RACE_CHOICES, max_length=50)
    religion = models.CharField(_('Religion'), blank=False, max_length=255)
    political_orientation = models.CharField(_('Political Orientation'), blank=False, max_length=255)
    zip_code = models.PositiveIntegerField(blank=False)
    years_of_education_completed = models.PositiveIntegerField(blank=False)

    ## Model methods ##
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def presented_images(self):
        return self.imagepresentation_set.all()

    @property
    def liked_images(self):
        return self.presented_images.filter(state=ImagePresentation.STATE_SEEN_AND_LIKED)

    @property
    def disliked_images(self):
        return self.presented_images.filter(state=ImagePresentation.STATE_SEEN_AND_DISLIKED)

    @property
    def num_presented_images(self):
        return self.presented_images.count()

    def get_next_image(self):
        selected_image = Image.objects.random()  # TODO: don't use random
        sequence_number = self.num_presented_images + 1
        ImagePresentation.objects.create(image=selected_image, sequence_number=sequence_number, viewer=self)
        return selected_image
