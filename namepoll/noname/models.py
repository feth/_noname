#coding:utf-8
from datetime import date
from os.path import expanduser

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import UUIDField


UP_DIR = expanduser('~/noname/uploaded_images/')


class CompanyName(models.Model):
    """
        Model for the company name
    """
    name = models.CharField(max_length=200, primary_key=True)
    explanation = models.TextField()
    image = models.ImageField(blank=True, max_length=1024, upload_to=UP_DIR)
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

        total = sum(evaluation.value * evaluation.author.weight
            for evaluation in evaluations)

        mean = total / evaluations_nb

        #50 because it is 100/2
        #2 is the greatest value: for 'great'
        return mean, 50 * mean, evaluations_nb


class Voter(models.Model):
    """
        The voter's model
    """
    uuid = UUIDField()
    optional_nickname = models.CharField(max_length=100, blank=True)
    optional_email = models.EmailField(max_length=100, blank=True)
    optional_info = models.TextField(blank=True)
    pages_seen = models.ManyToManyField(CompanyName, related_name="seen",
                                        blank=True)
    weight = models.IntegerField(default=1)

    def __unicode__(self):
        unicode_string = u"Voter %d" % self.id
        if not self.optional_nickname:
            return unicode_string
        return u"%s, %s" % (unicode_string, self.optional_nickname)

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

    def _companies_voted(self):
        return tuple(evaluation.subject
            for evaluation in self.evaluations.all())

    companies_voted = property(fget=_companies_voted)


class Evaluation(models.Model):
    """
        Evaluation's model
    """
    VALUES = (
        (1, _('Prejudiciable')),
        (2, _('Valid')),
        (3, _('Great')),
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
