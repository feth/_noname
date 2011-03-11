#coding:utf-8
from datetime import date
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
    free_brand = models.BooleanField(_('Brand is available'))
    free_dotcom = models.BooleanField(_('.com is available'))
    free_dotfr = models.BooleanField(_('.fr is available'))
    free_dotnet = models.BooleanField(_('.net is available'))

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

    def normscore(self):
        """
        Gets you
        * the normalized score for this company name
        * the value in percentage
        * the number of evaluations that it got
        """
        evaluations = self.evaluations.all()

        if not evaluations:
            return 0, 0, 0

        evaluations_nb = evaluations.count()

        total = sum(
            evaluation.value * evaluation.author.weight
            for evaluation in evaluations
            )

        mean = total / evaluations_nb

        #50 because it is 100/2
        #2 is the greatest value: for 'great'
        return mean, 50*mean, evaluations_nb


class Voter(models.Model):
    """
        The voter's model
    """
    optional_nickname = models.CharField(max_length=100, blank=True)
    optional_email = models.EmailField(max_length=100, blank=True)
    optional_info = models.TextField(blank=True)
    pages_seen = models.ManyToManyField(CompanyName, related_name="seen",
                                        blank=True)
    #redundant with evaluations but quite quicker
    pages_voted = models.ManyToManyField(CompanyName, related_name="voted",
                                         blank=True)
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        unicode_string = u"Voter %d" % self.id
        if self.optional_nickname:
            unicode_string += u", %s" % self.optional_nickname
        return unicode_string

    class Meta(object):
        verbose_name = _('voter')
        verbose_name_plural = _('voters')

    def get_evaluation(self, companyname):
        evaluations_tuple = self.evaluations.filter(subject=companyname)
        if evaluations_tuple:
            return evaluations_tuple[0]
        evaluation = Evaluation()
        evaluation.date_of_creation = date.today()
        evaluation.date_of_modification = date.today()
        evaluation.author = self
        evaluation.subject = companyname
        return evaluation


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
        default=0,
        blank=False)
    message = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(Voter, related_name="evaluations")
    subject = models.ForeignKey(CompanyName, related_name="evaluations")
    date_of_creation = models.DateTimeField()
    date_of_modification = models.DateTimeField()

    class Meta(object):
        verbose_name = _('evaluation')
        verbose_name_plural = _('evaluations')

