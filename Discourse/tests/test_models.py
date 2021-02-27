from django.test import TestCase
from Discourse.models import RamblerSub, RamblerPost, RamblerComment
from django.contrib.auth import get_user_model

# Create your tests here.
class SubModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        for i in range(3):
            User.objects.create_user(username=f'name{i}', password=f'pass{i}')

        self.sub_1 = RamblerSub(user=User.objects.get(username="name1"), name="sub_1", description="none")
        self.sub_2 = RamblerSub(user=User.objects.get(username="name2"), name="sub_2", description="none")

    def test_sub_str(self):
        self.assertEqual(self.sub_1.name, str(self.sub_1))
        self.assertEqual(self.sub_2.name, str(self.sub_2))


class PostModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        for i in range(3):
            User.objects.create_user(username=f'name{i}', password=f'pass{i}')
            RamblerSub.objects.create(
                user=User.objects.get(username=f'name{i}'),
                name=f'sub{i}',
                description=f'description{i}')

        self
