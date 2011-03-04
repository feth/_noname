from os.path import expanduser

from django.db import models


class CompanyName(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    explanation = models.TextField()
    image = models.ImageField(
        blank=True,
        max_length=1024,
        upload_to=expanduser('~/noname/uploaded_images/')
    )
    free_brand = models.BooleanField('Brand is free')
    free_dotcom = models.BooleanField('.com is free')
    free_dotfr = models.BooleanField('.fr is free')
    free_dotnet = models.BooleanField('.net is free')


    def __unicode__(self):
        return self.name

    def _availability(self):
        yield 'brand (INPI)', self.free_brand
        yield '.com TLD', self.free_dotcom
        yield '.fr TLD', self.free_dotfr
        yield '.net TLD ', self.free_dotnet

    availability = property(fget=_availability)


class Voter(models.Model):
    optionnal_info = models.TextField()


class Vote(models.Model):
    VOTE_CHOICES = (
        (0, 'Dislike'),
        (1, 'Acceptable'),
        (2, 'Good'),
        )

    name = models.ForeignKey(CompanyName)
    voter = models.ForeignKey(Voter)
    date = models.DateTimeField('time of vote')
    value = models.IntegerField(choices=VOTE_CHOICES)
    additionnal_remarks = models.TextField()


