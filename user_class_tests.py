
import pytest
import sqlite3
from User import User
conn = sqlite3.connect(':memory:')
c = conn.cursor()

acc=(2, 'fn', 'ln', 'user', 'pass', 'Librarian ', None, None, 'True', None)
@pytest.mark.parametrize("fn,ln,acc", ['t','u', acc])
class Test_User_class:

    def test_user(self, f, l, account):
        newUser = User(f, l, account)
        assert newUser.f_name == f
        assert newUser.l_name == l
        assert newUser.account==account