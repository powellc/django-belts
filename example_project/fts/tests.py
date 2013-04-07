from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_dynamic_fixture import G

from dojo.models import Student, Dojo, Discipline, Rank, Test, TestQuestion, TestAnswer


class TestAStudent(WebTest):

    def setUp(self):
        self.student = G(Student, user__is_staff = True)
        #self.dojo = G(Dojo, owner = self.student, title="Test Dojo", slug="test-dojo")
        #self.discipline = G(Discipline, )

    def test_student_can_access_account_homepage(self):
        """
        Test a student can access the account homepage
        """
        res = self.app.get(reverse('account_homepage'), user = user)
        pdb.set_trace()
        self.assertTemplateUsed(res, 'accounts/account_homepage.html',
                'Activated account did not access account homepage correctly')
    def test_(self):
        """ A student can login and create a new dojo that they are the owner of. """
        index = self.app.get(reverse('dojo-index'))

        # Specify the file content to upload and submit the form
        form = index.forms['upload_form']
        # CSV content should be: username, credits, start_date, end_date
        content = "10000,250,2012-01-01,2013-01-01"
        form['file'] = 'credits.csv', content
        form.submit()

        # Check that an allocation has been created
        self.assertEqual(250, api.balance(customer))
        self.assertEqual(1, api.allocations(customer).count())

