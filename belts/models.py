from django.db import models
from django.conf import settings
from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords_html
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from autoslug import AutoSlugField


class Student(models.Model):
    """ A Student

    A fairly basic wrapper around the Django User model that holds all our
    dojo-specific informaiton.

    """
    user = models.ForeignKey(User)
    joined = models.DateTimeField(null=True, blank=True, default=datetime.now())

    @property
    def passed_test_count(self):
        """ Return the number of tests self has passed. """
        return self.testattempt_set.count()

    def __unicode__(self):
        if self.user.first_name or self.user.last_name:
            return ' '.join(self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    @property
    def passed_tests(self):
        tests = self.testattempt_set.filter(passed=True).values('test').distinct()
        return Test.objects.filter(id__in=tests)


class Dojo(models.Model):
    """ A Dojo

    Organizes Students into logical groups, so that schools or organizations can
    create private Disciplines and still share them with other Students.

    A Dojo also allows for smaller groups to share TestAttempts with other users
    in the Dojo without opening it up to the whole internet.

    """
    title = models.CharField(max_length=100)
    slug = AutoSlugField(_('Slug'), populate_from='title')
    owners = models.ManyToManyField(User)
    private = models.BooleanField(_('Private'), default=True)
    created_by = models.ForeignKey(Student)
    created = models.DateTimeField(null=True, blank=True, default=datetime.now(), editable=False)

    def __unicode__(self):
        return self.title


class Discipline(models.Model):
    """ A discipline

    Keeps track of a collection of Tests and culminates in a Student
    achieving the sempai status

    Disciplines are the primary interface to the application for a Student. They
    choose a Discipline and are presented with a series of Tests to rise in Rank.

    Disciplines enforce whether Students are allowed to jump Ranks or whether they
    have to take Tests in the order specified by the Tests.

    """
    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(_('Slug'), populate_from='title')
    description = HTMLField(_('Description'), blank=True, null=True)
    private = models.BooleanField(_('Private'), default=True)
    test_in_order = models.BooleanField(_('Test in Order'), default=True)
    dojo = models.ForeignKey(Dojo, blank=True, null=True)
    created_by = models.ForeignKey(Student)
    created = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('dojo-discipline-detail', kwargs={'slug': self.slug})

    def tests(self, student=None):
        """ Return a dict of tests a Student is allowed to take:

        example return values:

        In both cases a user has not passed Test1 yet.

        if test_in order true: { Test1: True, Test2: False, Test3: False }

        if test_in_order false: { Test1: True, Test2: True, Test3: True }


        """
        tests = {}
        if self.test_in_order:
            if student:
                attempts_at_this_discipline = student.testattempt_set.filter(test__discipline=self).order_by('test__rank_awarded__order')
                for attempt in attempts_at_this_discipline:
                    if attempt.passed:
                        tests[attempt.test] = True
                    else:
                        tests[attempt.test] = False
            else:
                for test in self.test_set.all():
                    tests[test] = True
        else:
            for test in self.test_set.all():
                tests[test] = True
        return tests

    class Meta:
        ordering = ['-created']


class Rank(models.Model):
    """
    A Rank

    Used inside of a Discipline and are associated with badges. As students
    complete Tests in a Discipline they earn ranks in the order specified here,
    with 1 being the lowest and any number of other ranks.

    By default, the dojo app comes with a fixture setting a up a simplified Kyu-style:

    1 - White
    2 - Orange
    3 - Blue
    4 - Purple
    5 - Brown
    6 - Black

    But any number can be created.

    Additionally, Ranks are not tied to a specific discpline, but are specified on
    a Test level, so Tests determine what Rank should be given on completion. The
    Discipline model is then required to enforce Students rising ranks in order.
    This also allows Ranks to be given out in any order (if a Discipline allows,
    Students could "jump" to the Brown belt).

    TODO: Hook up Mozilla's OpenBadges here, probably using django-obi

    """
    title = models.CharField(_('Rank'), max_length=100)
    slug = AutoSlugField(_('Slug'), populate_from='title')
    order = models.IntegerField(_('Order'), max_length=2)
    created = models.DateTimeField(null=True, blank=True, default=datetime.now(), editable=False)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ['order']


class Test(models.Model):
    """ A Test

    How a Student climbs Ranks in a Discipline. A Test presents the Student with
    a set of TestQuestions and then auto-grades it on submission using the
    associated TestAnswer.
    """
    discipline = models.ForeignKey(Discipline)
    rank_awarded = models.ForeignKey(Rank,
                                     help_text='Awarded to a student on successful completion of the test.')
    slug = models.SlugField(_('Slug'), editable=False)
    pass_percentage = models.IntegerField(_('Pass Percentage'), blank=True, null=True,
                                          help_text='Percent correct required to pass the text. Leave blank to use\
                                                     default.')
    created = models.DateTimeField(null=True, blank=True, default=datetime.now(), editable=False)

    @property
    def total_questions(self):
        return self.testquestion_set.count()

    def __unicode__(self):
        return u'%s test for %s' % (self.rank_awarded, self.discipline)

    def get_absolute_url(self):
        return reverse('dojo-test-detail', kwargs={'discipline_slug': self.discipline.slug, 'slug': self.rank_awarded.slug})

    def save(self, *args, **kwargs):
        self.slug = self.rank_awarded.slug
        super(Test, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Test")
        ordering = ["rank_awarded__order"]


class TestAnswer(models.Model):
    """ A TestAnswer

    A string representing an answer to a TestQuestion. The correct answer
    is indicated as part of the TestQuestion. All this knows is what
    order to present the TestAnswer in.

    If no order is given, it defaults to 1 and presents the Answer in a random order.

    """
    answer = models.TextField(_('Answer'))
    order = models.IntegerField(_('Order'), default=1)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __unicode__(self):
        return u'%s' % truncatewords_html(self.answer, 15)

    @property
    def question_count(self):
        """ Counts the number of questions related to self. """
        return self.question_set.count()


class TestQuestion(models.Model):
    """ A TestQuestion

    Represents a question as part of a Test.

    """
    test = models.ForeignKey(Test)
    question = models.TextField(_('Question'))
    answers = models.ManyToManyField(TestAnswer)
    correct_answer = models.ForeignKey(TestAnswer, related_name="correct_answer")

    class Meta:
        verbose_name = _('Test Question')
        verbose_name = _('Test Questions')

    def __unicode__(self):
        return u'%s [%s]' % (truncatewords_html(self.question, 15), self.test)


class TestAttempt(models.Model):
    """ A TestAttempt

    Records an attempt made to pass a test.

    """
    student = models.ForeignKey(Student)
    test = models.ForeignKey(Test)
    correct_answers = models.ManyToManyField(TestQuestion, blank=True, null=True)
    passed = models.BooleanField(default=False)
    created = models.DateTimeField(null=True, blank=True, default=datetime.now(), editable=False)

    def save(self, *args, **kwargs):
        req = getattr(settings, 'DOJO_TEST_PASS_PERCENTAGE', 80)
        if self.test.pass_percentage:
            req = self.test.pass_percentage
        if self.percentage_correct >= req:
            self.passed = True
        super(TestAttempt, self).save(*args, **kwargs)

    @property
    def correct_answer_count(self):
        return self.correct_answers.count()

    @property
    def total_questions(self):
        return self.test.total_questions

    @property
    def percentage_correct(self):
        """ Return computed percentage of correct answers vs. the total questions in the test. """
        return round((float(self.correct_answer_count) / float(self.total_questions) * 100), 0)

    def __unicode__(self):
        return u'Attempt at %s' % (self.test)

    def get_absolute_url(self):
        return reverse('dojo-test-attempts', kwargs={'discipline_slug': self.test.discipline.slug, 'test_slug': self.test.slug, 'pk': self.pk})

    class Meta:
        verbose_name = _('Test Attempt')
        verbose_name_plural = _('Test Attempts')
        ordering = ["test", "test__rank_awarded"]
