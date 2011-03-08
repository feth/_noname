#coding:utf-8
from os.path import expanduser

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CompanyName(models.Model):
    """
        Model for the company name
    """
    name = models.CharField(max_length=200, primary_key=True)
    explanation = models.TextField()
    image = models.ImageField(
        blank=True,
        max_length=1024,
        upload_to=expanduser('~/noname/uploaded_images/')
    )
    free_brand = models.BooleanField(_('Brand is free'))
    free_dotcom = models.BooleanField(_('.com is free'))
    free_dotfr = models.BooleanField(_('.fr is free'))
    free_dotnet = models.BooleanField(_('.net is free'))

    def __unicode__(self):
        return self.name

    def _availability(self):
        yield _('brand (INPI))'), self.free_brand
        yield _('.com TLD'), self.free_dotcom
        yield _('.fr TLD'), self.free_dotfr
        yield _('.net TLD'), self.free_dotnet

    availability = property(fget=_availability)

    class Meta(object):
        verbose_name = _('company name')
        verbose_name_plural = _('company names')


class Voter(models.Model):
    """
        The voter's model
    """
    optional_nickname = models.CharField(max_length=100, blank=True)
    optional_email = models.EmailField(max_length=100, blank=True)
    optional_info = models.TextField(blank=True)
    pages_seen = models.ManyToManyField(CompanyName, related_name="seen")
    #redundant with evaluations but quite quicker
    pages_voted = models.ManyToManyField(CompanyName, related_name="voted")
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        return "I am a voter"

    class Meta(object):
        verbose_name = _('voter')
        verbose_name_plural = _('voters')


class Evaluation(models.Model):
    """
        Evaluation's model
    """
    VALUES = (
        (0, _('Prejudiciable')),
        (1, _('Valid')),
        (2, _('Great')),
    )
    value = models.IntegerField(
        _("What do you think this name would be to our company?"),
        choices=VALUES,
        default=-1)
    message = models.TextField(max_length=300)
    author = models.ForeignKey(Voter)
    subject = models.ForeignKey(CompanyName)
    eval_date = models.DateTimeField()

    class Meta(object):
        verbose_name = _('evaluation')
        verbose_name_plural = _('evaluations')
