from django.contrib import admin
from django.forms import widgets
from dojo.models import Student, Dojo, Discipline, Rank, Test, TestQuestion, TestAnswer, TestAttempt


class DisciplineAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'private', 'test_in_order', 'dojo')

    def save_model(self, request, obj, form, change):
        obj.created_by = Student.objects.get(user=request.user)
        obj.save()


admin.site.register(Discipline, DisciplineAdmin)


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    widgets = {
        'question': widgets.TextInput(),
    }


class TestAdmin(admin.ModelAdmin):
    inlines = [
        TestQuestionInline,
    ]


admin.site.register(Test, TestAdmin)

admin.site.register(Rank)
admin.site.register(Student)
admin.site.register(Dojo)
admin.site.register(TestQuestion)
admin.site.register(TestAnswer)
admin.site.register(TestAttempt)
