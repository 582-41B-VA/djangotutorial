from django.test import TestCase, Client
from .models import Question
from django.utils import timezone
import datetime
from django.urls import reverse


class DetailViewTests(TestCase):
    def test_question_id_doesnt_exist(self):
        """
        Should return a 404 response if the id doesn't match a question
        in the database.
        """
        client = Client()
        response = client.get(reverse("polls:detail", args=(1,)))
        self.assertEqual(response.status_code, 404)


class QuestionModelTests(TestCase):
    def test_recently_published_with_future_question(self):
        """Should return false when the question hasn't yet been published."""
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=tomorrow)
        self.assertIs(future_question.was_published_recently(), False)

    def test_recently_published_with_today_question(self):
        """Should return true when the question was published today."""
        today = timezone.now()
        question = Question(pub_date=today)
        self.assertIs(question.was_published_recently(), True)

    def test_recently_published_with_yesterday_question(self):
        """Should return true when the question was published yesterday."""
        yesterday = timezone.now()
        question = Question(pub_date=yesterday)
        self.assertIs(question.was_published_recently(), True)
