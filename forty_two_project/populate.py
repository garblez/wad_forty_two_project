import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# Other import to be found in the main function before populate is called: the above is used to setup and
# connect to django.

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
        "Just a title for this solution",
        computing_sub,
        "I needed a one-line function to reverse any string argument",
        "I simply created the following:\nreverse = lambda x: x[::-1]"
    )

    physics_sol = add_sol(
        user_brian,
        datetime.now(),
        "Yet another title for another solution",
        physics_sub,
        "I needed some way to document what I was doing inside a matlab script without it being read by matlab",
        "Matlab allows you to comment using %. The comment starts where % is and ends at the end of the line."
    )

    maths_sol = add_sol(
        user_claire,
        datetime.now(),
        "Proper and Formal Title Befitting of a Mathematician Writing in the Wrong Register",
        maths_sub,
        "Came across a latex parsing error when trying to write the curl of F using the nabla cross product.",
        "Just use \\noit{curl}F."
    )

    computing_sol.tags.add("programming", "python", "strings", "reverse", "scripting")
    physics_sol.tags.add("matlab", "comments", "explanation", "inline explanation", "programming")
    maths_sol.tags.add("calculus 3", "curl", "vector fields", "partial derivatives", "latex", "typesetting", "nabla",
                       "format error")

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
    from django.db.utils import IntegrityError
    from datetime import datetime
    from django.template.defaultfilters import slugify
    from django.contrib.auth.models import User
    from forty_two.models import Solution, Subject
    from taggit.managers import TaggableManager

    populate()
    print("..complete!")
