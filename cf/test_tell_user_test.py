import unittest
import tell_user_taste


class UserTasteTestCase(unittest.TestCase):

    def test_tell_user_taste(self):
        # TODO: please specify a valid user id.
        user_id = ''
        t = tell_user_taste.tell_user_taste(user_id)
        self.assertTrue(t is not None)

if __name__ == '__main__':
    unittest.main()