from itertools import cycle

from base.db.router import in_read_only_database
from dispatch.models import City as AnyDbModel
from django.conf import settings
from mock import patch


@patch('db.router._cycle_and_skew', return_value=cycle(settings.READONLY_DBS))
def test_in_read_only_database_ctx_mgr_should_cycle_through_database_list(mocked_db_ro_cycle):
    with in_read_only_database():
        db_cycle_1 = AnyDbModel.objects.db

    with in_read_only_database():
        db_cycle_2 = AnyDbModel.objects.db

    assert db_cycle_1 != db_cycle_2
    assert db_cycle_1 in settings.READONLY_DBS
    assert db_cycle_2 in settings.READONLY_DBS


@patch('db.router._cycle_and_skew', return_value=cycle(settings.READONLY_DBS))
def test_in_read_only_database_decorator_should_cycle_through_database_list(mocked_db_ro_cycle):

    @in_read_only_database()
    def decorated_func():
        db_cycle = AnyDbModel.objects.db
        return db_cycle

    db_cycle_1 = decorated_func()
    db_cycle_2 = decorated_func()
    assert db_cycle_1 != db_cycle_2
    assert db_cycle_1 in settings.READONLY_DBS
    assert db_cycle_2 in settings.READONLY_DBS
