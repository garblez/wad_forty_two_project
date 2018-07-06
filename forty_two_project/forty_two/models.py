from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class Subject(models.Model):
    title = models.CharField(max_length=64, unique=True, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Subject"


class Solution(models.Model):
    #  The user who posted it.
    author = models.ForeignKey(User)

    #  Post timestamp
    post_time = models.DateTimeField()

    #  Short title to encapsulate the solution: also  slugged for use in the URL.
    title = models.CharField(max_length=256)

    slug_title = models.SlugField()  # For use in the URL.

    subject = models.ForeignKey(Subject, null=True)  # Refers to which category the solution pertains to: e.g., comp, alt, sci/physics,

    #  A brief explanation of how the solution was attained, what technologies were involved etc.
    cause = models.CharField(max_length=144)

    #  The main body of the solution: the steps involved, tips, outcomes.
    description = models.CharField(max_length=2048)

    tags = TaggableManager()    # Use django-taggit to add and remove simple tags (e.g., programming, calculus etc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Solution, self).save(*args, **kwargs)

    def __str__(self):
        return "[{0}\t{1}]\t{2}".format(
            self.post_time, self.author, self.title
        )

    class Meta:
        ordering = ('-post_time', )