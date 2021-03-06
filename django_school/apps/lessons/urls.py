from django.urls import path

from django_school.apps.lessons.views import (ClassSubjectListView,
                                              ClassTimetableView,
                                              HomeworkDetailView,
                                              HomeworkListView,
                                              LessonSessionListView,
                                              SetHomeworkView,
                                              TeacherTimetableView,
                                              class_attendance_summary_view,
                                              lesson_session_detail_view,
                                              student_attendance_summary_view,
                                              submit_homework_realisation_view,
                                              timetable_list_view)

app_name = "lessons"

urlpatterns = [
    path("timetables/", timetable_list_view, name="timetables_list"),
    path(
        "class_timetable/<slug:class_slug>/",
        ClassTimetableView.as_view(),
        name="class_timetable",
    ),
    path(
        "teacher_timetable/<slug:teacher_slug>/",
        TeacherTimetableView.as_view(),
        name="teacher_timetable",
    ),
    path(
        "sessions/",
        LessonSessionListView.as_view(),
        name="session_list",
    ),
    path(
        "sessions/<int:session_pk>/",
        lesson_session_detail_view,
        name="session_detail",
    ),
    path(
        "subjects/<slug:class_slug>/",
        ClassSubjectListView.as_view(),
        name="class_subject_list",
    ),
    path(
        "attendance/student/<slug:student_slug>/",
        student_attendance_summary_view,
        name="student_attendance",
    ),
    path(
        "attendance/class/<slug:class_slug>/",
        class_attendance_summary_view,
        name="class_attendance",
    ),
    path(
        "<slug:class_slug>/<slug:subject_slug>/set_homework/",
        SetHomeworkView.as_view(),
        name="set_homework",
    ),
    path("homeworks/", HomeworkListView.as_view(), name="homework_list"),
    path(
        "homeworks/<int:homework_pk>/",
        HomeworkDetailView.as_view(),
        name="homework_detail",
    ),
    path(
        "homeworks/<int:homework_pk>/submit_realisation/",
        submit_homework_realisation_view,
        name="submit_homework_realisation",
    ),
]
