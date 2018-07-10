from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class Subject(models.Model):
    title = models.CharField(max_length=64, unique=True, primary_key=True)

    title_slug = models.SlugField(default=slugify(title))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Subjects"


class Solution(models.Model):
    #  The user who posted it. If the account is deleted, remove their posts too. (May change in future)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #  Post timestamp
    post_time = models.DateTimeField(null=True)

    #  Short title to encapsulate the solution: also  slugged for use in the URL.
    title = models.CharField(max_length=144)

    title_slug = models.SlugField()  # For use in the URL.

    # Refers to which category the solution pertains to: e.g., comp, alt, sci/physics,
    subject = models.ForeignKey(Subject, null=True)

    subject_choice = models.CharField(
        max_length=144, default="computing science"
    )

    #  A brief explanation of how the solution was attained, what technologies were involved etc.
    cause = models.CharField(max_length=256)

    #  The main body of the solution: the steps involved, tips, outcomes.
    description = models.CharField(max_length=2048)

    # Use django-taggit to add and remove simple tags (e.g., programming, calculus etc)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        self.author = User.objects.get(username='mak')
        super(Solution, self).save(*args, **kwargs)

    def __str__(self):
        return "\t".join([str(self.post_time), str(self.author), self.title])

    class Meta:
        ordering = ('post_time', )


class Comment(models.Model):
    solution = models.ForeignKey(Solution)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Delete a user's posts when their account is deleted.
    content = models.CharField(max_length=2049)
    post_time = models.DateTimeField()

    def __str__(self):
        return "\t".join([str(self.post_time), str(self.solution), str(self.author)])

    class Meta:
        verbose_name_plural = "comments"