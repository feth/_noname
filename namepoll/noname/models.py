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
    optional_nickname = models.CharField(max_length=100)
    optional_email = models.EmailField(max_length=100)
    optional_info = models.TextField()
    pages_seen = models.ManyToManyField(CompanyName, related_name="seen")
    #redundant with evaluations but quite quicker
    pages_voted = models.ManyToManyField(CompanyName, related_name="voted")

    def __unicode__(self):
        return "I am a voter"


class Evaluation(models.Model):
    VALUES = (
        (0, 'Prejudiciable'),
        (1, 'Valid'),
        (2, 'Great'),
    )
    value = models.IntegerField(
        "What do you think this name would be to our company?",
        choices=VALUES,
        default=-1)
    message = models.TextField(max_length=300)
    author = models.ForeignKey(Voter)
    subject = models.ForeignKey(CompanyName)
    eval_date = models.DateTimeField()

