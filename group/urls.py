from django.urls import path

from .views import (
    start,
    group_form,
    group_list,
    add_student,
    teacher_form,
    teacher_edit,
    teacher_list,
    student_form,
    student_edit,
    student_list,
)

urlpatterns = [
    path("student", student_form, name="student_form"),
    path("student/<int:pk>", student_edit, name="student_edit"),
    path("students", student_list, name="student_list"),
    path("teacher", teacher_form, name="teacher_form"),
    path("teacher/<int:pk>", teacher_edit, name="teacher_edit"),
    path("teachers", teacher_list, name="teacher_list"),
    path("group", group_form, name="group_form"),
    path("group/<int:pk>", add_student, name="add_student"),
    path("groups", group_list, name="group_list"),
    path("", start, name="start"),
]
