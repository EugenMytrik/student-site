# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from .forms import TeacherForm, GroupForm, StudentForm
from .models import Group, Teacher, Student


def start(request):
    return render(request, "start.html")


def teacher_form(request):
    if request.method == "GET":
        form = TeacherForm()
        return render(request, "teacher_form.html", {"form": form})
    form = TeacherForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("teacher_edit", args={form.instance.pk}))
    return render(request, "teacher_form.html", {"form": form})


def teacher_edit(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    if request.method == "GET":
        form = TeacherForm(instance=teacher)
        return render(request, "teacher_edit.html", {"form": form})
    form = TeacherForm(request.POST, instance=teacher)
    if form.is_valid() and "ok" in request.POST:
        form.save()
        return redirect("teacher_list")
    if "delete" in request.POST:
        groups = teacher.group.all()
        if not groups:
            teacher.delete()
            return redirect("teacher_list")
        return HttpResponse("<h3>This teacher has groups and cannot be deleted<м/h3>")
    return render(request, "teacher_edit.html", {"form": form})


def teacher_list(request):
    teacher = Teacher.objects.all()
    return render(request, "teacher_list.html", {"teacher": teacher})


def group_form(request):
    if request.method == "GET":
        form = GroupForm()
        return render(request, "group_form.html", {"form": form})
    form = GroupForm(request.POST)
    if form.is_valid():
        form.save()
        form.instance.students.set(form.cleaned_data["students"])
        return redirect(reverse("add_student", args={form.instance.pk}))
    return render(request, "group_form.html", {"form": form})


def group_list(request):
    group = Group.objects.all()
    return render(request, "group_list.html", {"group": group})


def student_form(request):
    if request.method == "GET":
        form = StudentForm()
        return render(request, "student_form.html", {"form": form})
    form = StudentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("student_edit", args={form.instance.pk}))
    return render(request, "student_form.html", {"form": form})


def student_edit(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "GET":
        form = StudentForm(instance=student)
        return render(request, "student_edit.html", {"form": form})
    form = StudentForm(request.POST, instance=student)
    if form.is_valid() and "ok" in request.POST:
        form.save()
        return redirect("student_list")
    if "delete" in request.POST:
        student.delete()
        return redirect("student_list")
    return render(request, "student_edit.html", {"form": form})


def student_list(request):
    student = Student.objects.all()
    return render(request, "student_list.html", {"student": student})


def add_student(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == "GET":
        form = GroupForm(instance=group)
        return render(request, "add_student.html", {"form": form, "group": group})
    form = GroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        for student in form.cleaned_data["students"]:
            form.instance.students.add(student)
        return redirect("group_list")
    return render(request, "add_student.html", {"form": form, "group": group})
