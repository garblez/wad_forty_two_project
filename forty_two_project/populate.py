import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forty_two_project.settings')

import django
django.setup()

from django.db.utils import IntegrityError
from datetime import datetime
from django.contrib.auth.models import User
from forty_two.models import Solution, Subject
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager


def populate():
    u = create_super_user('mak', '', 'CrabbitPirate')

    user_aaron, result = User.objects.get_or_create(username='aaron', email='', password='pass')
    user_brian, result = User.objects.get_or_create(username='brian', email='', password='word')
    user_claire, result = User.objects.get_or_create(username="cwilson", email='', password="3.14159826535")

    computing_sub = add_sub("computing science")
    physics_sub = add_sub("physics")
    maths_sub = add_sub("mathematics")


    computing_sol = add_sol(
        user_aaron,
        datetime.now(),
        "One line functions",
        computing_sub,
        "I needed a one-line function to reverse any string argument",
        "I simply created the following:\nreverse = lambda x: x[::-1]"
    )

    computing_sol1 = add_sol(
        user_claire,
        datetime.now(),
        "Database Migrations",
        computing_sub,
        "I couldn't migrate my database.",
        """I removed all __pycache__ directories and migrations directories from my project, makemigrations and migrated for the project (manage.py migrate project_name) and then for my app."""
    )

    physics_sol = add_sol(
        user_brian,
        datetime.now(),
        "Matlab help",
        physics_sub,
        "I needed some way to document what I was doing inside a matlab script without it being read by matlab",
        "Matlab allows you to comment using %. The comment starts where % is and ends at the end of the line."
    )

    computing_sol.tags.add("programming", "python", "strings", "reverse", "scripting")
    physics_sol.tags.add("matlab", "comments", "explanation", "inline explanation", "programming")



def add_sub(title):
    sub, result = Subject.objects.get_or_create(title=title)
    sub.save()
    return sub


def add_sol(user, post_time, title, subject, cause, description):
    a, result = Solution.objects.get_or_create(
        author=user,
        title=title,
        subject=subject,
        cause=cause,
        description=description
    )
    a.post_time = post_time
    a.save()  # Slugs the title and stores it in the slug_title field.
    return a


def create_super_user(username, email, password):
    try:
        u = User.objects.create_superuser(username=username, email=email, password=password)
        return u
    except IntegrityError:
        pass



if __name__ == "__main__":
    print("Starting population script....")

    populate()
    print("..complete!")
