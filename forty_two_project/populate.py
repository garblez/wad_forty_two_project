import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# Other import to be found in the main function before populate is called: the above is used to setup and
# connect to django.

def populate():
    u = create_super_user('mak', '', 'CrabbitPirate')

    user_aaron, result = User.objects.get_or_create(username='aaron', email='', password='pass')

    computing_sub = add_sub("computing science")

    print("#######  "+str(type(computing_sub)))

    #physics_sub = add_sub("physics")
    #maths_sub = add_sub("mathematics")

    computing_sol = add_sol(
        user_aaron,
        datetime.now(),
        "Just a title for this solution",
        computing_sub,
        "I needed a one-line function to reverse any string argument",
        "I simply created the following:\nreverse = lambda x: x[::-1]"
    )
    '''
    computing_sol.tags.add("programming", "python", "strings", "reverse", "lambda")

    for user in User.objects.all():
        print(user)

    for sol in Solution.objects.all():
        print(sol)
    '''



def add_sub(title):
    sub, result = Subject.objects.get_or_create(title=title)
    sub.save()
    return sub


def add_sol(user, post_time, title, subject, cause, description):
    a, result = Solution.objects.get_or_create(
        author=user,
        post_time=post_time,
        title=title,
        subject=subject,
        cause=cause,
        description=description
    )
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
