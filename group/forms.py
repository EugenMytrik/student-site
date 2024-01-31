import datetime
import re
from datetime import date, timedelta

from django import forms
from django.forms import SelectDateWidget

from .models import Teacher, Group, Student


class TeacherForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=SelectDateWidget(years=range(1900, datetime.datetime.now().year))
    )

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "patronymic", "birth_date"]

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", first_name):
            raise forms.ValidationError("The first name must contain only letters")
        if len(first_name) < 2:
            raise forms.ValidationError("Too short a first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", last_name):
            raise forms.ValidationError("The last name must contain only letters")
        if len(last_name) < 2:
            raise forms.ValidationError("Too short a last name")
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data["patronymic"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", patronymic):
            raise forms.ValidationError("The patronymic must contain only letters")
        if len(patronymic) < 2:
            raise forms.ValidationError("Too short a patronymic")
        return patronymic

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if date.today() - birth_date < timedelta(days=6575):
            raise forms.ValidationError(
                "You must be at least 18 years old to become a teacher"
            )
        return birth_date


class GroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ["name", "curator"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("Too short a name")
        return name


class StudentForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    birth_date = forms.DateField(
        widget=SelectDateWidget(years=range(1900, datetime.datetime.now().year))
    )

    date_of_admission = forms.DateField(
        widget=SelectDateWidget(years=range(1900, datetime.datetime.now().year))
    )

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "birth_date",
            "date_of_admission",
            "group",
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", first_name):
            raise forms.ValidationError("The first name must contain only letters")
        if len(first_name) < 2:
            raise forms.ValidationError("Too short a first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", last_name):
            raise forms.ValidationError("The last name must contain only letters")
        if len(last_name) < 2:
            raise forms.ValidationError("Too short a last name")
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data["patronymic"]
        if not re.match("^[a-zA-Zа-яА-ЯЇїЄєІіҐґ-]+$", patronymic):
            raise forms.ValidationError("The patronymic must contain only letters")
        if len(patronymic) < 2:
            raise forms.ValidationError("Too short a patronymic")
        return patronymic

    def clean_date_of_admission(self):
        date_of_admission = self.cleaned_data["date_of_admission"]
        birth_date = self.cleaned_data["birth_date"]
        if date_of_admission < birth_date:
            raise forms.ValidationError("A student cannot enroll before birth")
        return date_of_admission
