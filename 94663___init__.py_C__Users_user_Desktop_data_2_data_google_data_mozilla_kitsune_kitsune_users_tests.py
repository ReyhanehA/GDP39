from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType

import factory

from kitsune.sumo.tests import FuzzyUnicode, LocalizingClient, TestCase
from kitsune.users.models import Profile, Setting


class TestCaseBase(TestCase):
    """Base TestCase for the users app test cases."""

    client_class = LocalizingClient


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText()
    email = factory.LazyAttribute(lambda u: '{}@example.com'.format(u.username))
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

    # We pass in 'user' to link the generated Profile to our just-generated User.
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory('kitsune.users.tests.ProfileFactory', 'user')

    @factory.post_generation
    def groups(user, created, extracted, **kwargs):
        groups = extracted or []
        for group in groups:
            user.groups.add(group)


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    name = FuzzyUnicode()
    bio = FuzzyUnicode()
    website = 'http://support.example.com'
    timezone = None
    country = 'US'
    city = 'Portland'
    locale = 'en-US'
    user = factory.SubFactory(UserFactory, profile=None)


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.fuzzy.FuzzyText()


def add_permission(user, model, permission_codename):
    """Add a permission to a user.

    Creates the permission if it doesn't exist.

    """
    content_type = ContentType.objects.get_for_model(model)
    permission, created = Permission.objects.get_or_create(
        codename=permission_codename,
        content_type=content_type,
        defaults={'name': permission_codename})
    user.user_permissions.add(permission)


class SettingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Setting

    name = factory.fuzzy.FuzzyText()
    value = factory.fuzzy.FuzzyText()