from lms import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from lms import courses_datatables_views
from lms import subjects_datatables_views
from lms import topics_datatables_views
from lms import payments_datatables_views
from lms import users_subjects_datatables_views
from lms import users_topics_datatables_views

urlpatterns = [
	path('', views.index, name='index'),
	path('change-password', views.change_password, name='change_password'),
	path('home', views.home, name='home'),
	path('user-registration', views.user_registration, name='user_registration'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('add-course', views.add_course, name='add-course'),
	path('add-subject', views.add_subject, name='add-subject'),
	path('add-topic', views.add_topic, name='add-topic'),
	path('add-payment', views.add_payment_details, name='add_payment'),
    path('view-payments', views.view_payments, name='view-payments'),
    path('view-payments-dt', login_required(payments_datatables_views.PaymenttListDatatable.as_view()), 
        name='view-payments-dt'),
	path('view-courses', views.view_courses, name='view-courses'),
    path('view-courses-dt', login_required(courses_datatables_views.CourseListDatatable.as_view()), 
        name='view-courses-dt'),
    path('view-subjects', views.view_subjects, name='view-subjects'),
    path('view-subjects-dt', login_required(subjects_datatables_views.SubjectListDatatable.as_view()), 
        name='view-subjects-dt'),
    path('view-topics', views.view_topics, name='view-topics'),
    path('view-topics-dt', login_required(topics_datatables_views.TopicListDatatable.as_view()), 
        name='view-topics-dt'),
    path('delete-course/<int:course_id>', views.delete_course, name='delete_course'),
    path('delete-subject/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('delete-topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    path('edit-course/<int:course_id>', views.edit_course, name='edit_course'),
    path('edit-subject/<int:subject_id>', views.edit_subject, name='edit_subject'),
    path('edit-topic/<int:topic_id>', views.edit_topic, name='edit_topic'),
    path('edit-payment/<int:payment_id>', views.edit_payment_details, name='edit-payment'),

    path('add-user-course', views.add_user_course, name='add-user-course'),
    path('user-subjects', views.user_view_subject, name='user-subjects'),
    path('view-user-subjects-dt', login_required(users_subjects_datatables_views.UserSubjectListDatatable.as_view()), 
        name='view-user-subjects-dt'),
    path('user-topics', views.user_view_topic, name='user-topics'),
    path('view-user-topics-dt', login_required(users_topics_datatables_views.UserTopicListDatatable.as_view()), 
        name='view-user-topics-dt'),
    path('topic/<int:topic_id>', views.topic_page, name='topic'),
    path('user-make-payment', views.user_make_payment, name='user-make-payment'),
]
