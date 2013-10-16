from django import forms
from django.forms.formsets import formset_factory

from .models import TestQuestion, TestAttempt


class TestAttemptForm(forms.ModelForm):
    model = TestAttempt


class QuestionForm(forms.Form):
    #answers = forms.ChoiceField(widget=forms.RadioSelect(), label=u"")

    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.question = question.question
        answers = question.answers.order_by('order')
        answer_id = 'question_' + str(question.id)
        self.fields[answer_id] = forms.ChoiceField(widget=forms.RadioSelect(),
                                                      label=u"")
        self.fields[answer_id].choices = [(a.id, a.answer) for a in answers]

        for pos, answer in enumerate(answers):
            if answer.id == question.correct_answer_id:
                self.correct_answer = pos
            break

    def is_correct(self):
        if not self.is_valid():
            return False

        return self.cleaned_data['answers'] == str(self.correct_answer)


def test_forms(test, data=None):
    questions = TestQuestion.objects.filter(test=test).order_by('id')
    form_list = []
    for pos, question in enumerate(questions):
        form_list.append(QuestionForm(question, data, prefix=pos))
    return form_list
