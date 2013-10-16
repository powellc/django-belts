from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse

from dojo.models import Student, Dojo, Discipline, Test, TestAttempt, TestAnswer, TestQuestion
from dojo.forms import test_forms


class ProtectedView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)

class DojoIndexView(TemplateView):
    template_name = 'dojo/dojo_index.html'

    def get_context_data(self, **kwargs):
        context = super(DojoIndexView, self).get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.filter(private=False)
        return context


class StudentDetailView(ProtectedView, DetailView):
    model = Student


class DojoDetailView(DetailView):
    model = Dojo


class DojoListView(ListView):
    model = Dojo


class DisciplineDetailView(DetailView):
    model = Discipline


class DisciplineListView(ListView):
    model = Discipline


class TestDetailView(ProtectedView, DetailView):
    model = Test

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        context['form'] = test_forms(self.object)
        return context

    def post(self, request, *args, **kwargs):
        """ Create a TestAttempt and save """
        test = Test.objects.get(id=request.POST['test_id'])
        student = Student.objects.get(user=request.user)
        attempt = TestAttempt.objects.create(student=student, test=test)
        print request.POST
        for item in request.POST:
            if 'question' in item:
                question = TestQuestion.objects.get(id=item.split('_')[-1])
                if question.correct_answer.id == int(request.POST[item]):
                    attempt.correct_answers.add(TestQuestion.objects.get(id=item.split('_')[-1]))
        attempt.save()
        return redirect(reverse('dojo-test-attempts', kwargs={'test_slug': test.slug, 'pk': attempt.id}))


class TestCompleteView(DetailView):
    model = TestAttempt


class TestAttemptListView(ListView):
    model = TestAttempt

    def get_queryset(self):
        return TestAttempt.objects.filter(student__user=self.request.user)


class DisciplineCreateView(CreateView):
    model = Discipline


class TestCreateView(CreateView):
    model = Test
    fields = ('rank_awarded', 'pass_percentage')
