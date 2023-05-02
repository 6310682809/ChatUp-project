from django.urls import reverse
from django.test import Client, TestCase
from user.models import *
from .utils.search import *

# Create your tests here.

class SearchFriendTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="user1",
            email="user1@email.prj",
            password="password"
        )
        self.user2 = User.objects.create(
            username="user2",
            email="user2@email.prj",
            password="password"
        )
        self.user3 = User.objects.create(
            username="user3",
            email="user3@email.prj",
            password="password"
        )
        self.user1_info = UserInfo.objects.create(
            user_id=self.user1,
            chatup_id="user1_id",
            prefix_phone_number="+66",
            phone_number="489456468748",
        )
        self.user2_info = UserInfo.objects.create(
            user_id=self.user2,
            chatup_id="user2_id",
            prefix_phone_number="+89",
            phone_number="748944868",
        )
        self.user3_info = UserInfo.objects.create(
            user_id=self.user3,
            chatup_id="user3_id",
            prefix_phone_number="+98",
            phone_number="123456789",
        )
    def test_searchFriend_accessible(self):
        c = Client()
        response = c.get(reverse('searchFriend'))
        self.assertEqual(response.status_code, 200)
    def test_searchFriend_id_present(self):
        c = Client()
        response = c.get(reverse('searchFriend'), {'search':'user2_id'})
        self.assertQuerysetEqual(response.context['friends'], [self.user2_info,], ordered=False)
    def test_searchFriend_id_absent(self):
        c = Client()
        response = c.get(reverse('searchFriend'), {'search':'absentTest'})
        self.assertQuerysetEqual(response.context['friends'], UserInfo.objects.all(), ordered=False)
    def test_searchFriend_Phone_present(self):
        c = Client()
        response = c.get(reverse('searchFriend'), {'search':'+98 123456789'})
        self.assertQuerysetEqual(response.context['friends'], [self.user3_info,], ordered=False)
    def test_searchFriend_Phone_absent(self):
        c = Client()
        response = c.get(reverse('searchFriend'), {'search':'+1234 4678974'})
        self.assertQuerysetEqual(response.context['friends'], UserInfo.objects.all(), ordered=False)