"""
Patch database setup for fixture generation so it runs South migrations.

"""
from fixture_generator.management.commands import generate_fixture
from south.management.commands import patch_for_test_db_setup


class Command(generate_fixture.Command):
    def handle(self, *args, **kwargs):
        patch_for_test_db_setup()
        super(Command, self).handle(*args, **kwargs)
