from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.datetime_safe import datetime


from taggit.managers import TaggableManager


class Subject(models.Model):
    title = models.CharField(max_length=64, unique=True)

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
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    #  Post timestamp
    post_time = models.DateTimeField(null=True)

    #  Short title to encapsulate the solution: also  slugged for use in the URL.
    title = models.CharField(max_length=40, unique=True)

    title_slug = models.SlugField()  # For use in the URL.

    # Refers to which category the solution pertains to: e.g., comp, alt, sci/physics,
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)

    subject_choice = models.CharField(
        max_length=64, default="computing science"
    )

    #  A brief explanation of how the solution was attained, what technologies were involved etc.
    cause = models.CharField(max_length=80)

    #  The main body of the solution: the steps involved, tips, outcomes.
    description = models.CharField(max_length=512)

    # Use django-taggit to add and remove simple tags (e.g., programming, calculus etc)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        super(Solution, self).save(*args, **kwargs)

    def __str__(self):
        return "\t".join([str(self.post_time), str(self.author), self.title])

    class Meta:
        ordering = ('post_time', )


class Comment(models.Model):
    parent_solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Delete a user's posts when their account is deleted.

    content = models.CharField(max_length=256, null=False)

    post_time = models.DateTimeField(default=datetime.now())

    # Each user gets one vote of either of the following (which will be tracked in the context of the solution comments)
    upvoters = models.ManyToManyField(User, related_name='comment_upvoters')  # The users who have 'liked' the comment
    downvoters = models.ManyToManyField(User, related_name='comment_downvoters')  # The users who have 'disliked' the comment

    # The greater the vote polarity, the better received the comment is and the further up in the comment section it appears
    def get_vote_polarity(self):
        return len(self.upvoters) - len(self.downvoters)

    # Only add a user as an upvoter if they haven't already voted
    def add_upvoter(self, voter):
        if voter not in self.upvoters and voter not in self.downvoters:
            self.upvoters.add(voter)
            self.save()

    # Only remove a user as an upvoter if they were an upvoter.
    def del_upvoter(self, voter):
        if voter in self.upvoters:
            self.upvoters.remove(voter)
            self.save()

    def add_downvoter(self, voter):
        if voter not in self.upvoters and voter not in self.downvoters:
            self.downvoters.add(voter)
            self.save()

    def del_downvoter(self, voter):
        if voter in self.downvoters:
            self.downvoters.remove(voter)
            self.save()

    def __str__(self):
        return "\t".join([str(self.post_time), str(self.parent_solution), str(self.author)])

    class Meta:
        verbose_name_plural = "comments"


def user_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]  # Get the correct file extension for the uploaded file
    # Store the uploaded file in media/profile/<username-slug>/<filename>
    return "profile/{0}/{1}".format(slugify(instance.user.username), filename)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(max_length=256, blank=True)

    photo = models.ImageField(blank=True, upload_to=user_directory_path)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

