import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


# p5 - Question model testing
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    # end test()

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    # end test()

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    # end test()
# end class()


# p5 - view testing helper
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
# end cq()


# p5 - view testing
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    # end no_q()

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question1 = create_question(question_text="Past question.", days=-30)
        question1.choice_set.create(choice_text="choice1")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    # end past_q()

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    # end future_q()

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        past_question.choice_set.create(choice_text="choice1")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    # end future_past()

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question1 = create_question(question_text="Past question 1.", days=-30)
        past_question2 = create_question(question_text="Past question 2.", days=-5)
        past_question1.choice_set.create(choice_text="choice1")
        past_question2.choice_set.create(choice_text="choice1")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
    # end two_past()

    def test_no_choices(self):
        """
        questions without choices shouldn't be displayed
        """
        create_question(question_text="no choices", days=-30)
        question2 = create_question(question_text="has choices", days=-30)
        question2.choice_set.create(choice_text='choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: has choices>']
        )
    # end tnc()
# end class()


# p5 - Detail view testing
class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found
        """
        future_question = create_question("Future Question", 5)
        future_question.choice_set.create(choice_text="choice1")
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    # end future_q()

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question('Past Question', -5)
        past_question.choice_set.create(choice_text="choice1")
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    # end past()

    def test_no_choice(self):
        """
        question without choice view should not exist
        """
        question_no_choice = create_question('question without choice', -30)
        qnc_url = reverse('polls:detail', args=(question_no_choice.id,))
        response = self.client.get(qnc_url)
        self.assertEquals(response.status_code, 404)
    # end tnc()
# end class


# p5 - Results view testing
class QuestionResultsViewTest(TestCase):
    def test_no_question(self):
        """
        invalid question id should return 404 error
        """
        invalid_url = reverse('polls:results', args=(1,))
        response = self.client.get(invalid_url)
        self.assertEquals(response.status_code, 404)
    # end tnq()

    def test_future_question(self):
        """
        future question view should return a 404 error
        """
        future_question = create_question('future question', 30)
        future_question.choice_set.create(choice_text="choice1")
        fq_url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(fq_url)
        self.assertEquals(response.status_code, 404)
    # end test_fq()

    def test_past_question(self):
        """
        results view should only exist for questions with pub_date in the past
        """
        past_question = create_question('past question', -30)
        past_question.choice_set.create(choice_text="choice1")
        pq_url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(pq_url)
        self.assertContains(response, 'past question')
    # end past_q()

    def test_question_but_no_choice(self):
        """
        results view should only exist for questions with choices
        """
        question1 = create_question("question", -10)
        # question1.choice_set.create(choice_text="choice1")
        q1_url = reverse('polls:results', args=(question1.id,))
        response = self.client.get(q1_url)
        self.assertEquals(response.status_code, 404)
    # end tqbnc()
# end class
