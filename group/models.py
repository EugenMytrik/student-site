from django.db import models


# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.patronymic}"


class Group(models.Model):
    name = models.CharField(max_length=50)
    curator = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="group")

    def __str__(self):
        return f"ID: {self.id} Group name: {self.name}"


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birth_date = models.DateField()
    date_of_admission = models.DateField()

    group = models.ManyToManyField(Group, related_name="students")

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.patronymic}"
