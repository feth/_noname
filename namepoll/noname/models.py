from django.db import models

class CompanyName(models.Model):
    name = models.CharField(max_length=200)
    explanation = models.TextField()
    image = models.ImageField(
        blank=True,
        max_length=1024,
        upload_to='/home/fethdjango/uploaded_images/'
        )

    def __unicode__(self):
        return self.name


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


