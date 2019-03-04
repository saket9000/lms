from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

from lms.helpers import context_helper
from lms import models

# Create your views here.

def index(request):

	"""
	This view redirects user to home if logged in else it redirects user
	to login page.
	"""

	if request.user.is_authenticated:
		return HttpResponseRedirect('home')
	return HttpResponseRedirect('login')

@login_required
def change_password(request):

	"""
	Change password form
	"""

	user = models.UserProfile.objects.get(username=request.user)
	context_dict = {}
	if request.method == 'POST':
		form = AdminPasswordChangeForm(user=user, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			context_dict['message'] = "Password changed successfully"
		else:
			context_dict['errors'] = form.errors
			context_dict['message'] = "Password not changed"
	return render(request, "changePassword.html", context_dict)

def user_registration(request):
	context_dict = {}
	if request.method == 'POST':
		name = request.POST.get('name')
		mobile = request.POST.get('mobile')
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = models.UserProfile.objects.filter(mobile=mobile).last()
		if user:
			context_dict.update({'message': 'User already exists with this mobile number'})
			return render(request, "userRegistration.html", context_dict)
		user = models.UserProfile.objects.create(
			name=name, mobile=mobile, email=email, is_student=True, username=name
		)
		user.save()
		user.set_password(password)
		user.save()
		context_dict.update({'message': 'New user created'})
		login(request, user)
		return HttpResponseRedirect('home')
	return render(request, "userRegistration.html", context_dict)

@login_required
def home(request):

	context_dict = {}
	user = models.UserProfile.objects.filter(
		username=request.user
	).first()
	context_dict.update(context_helper.get_user_info(user))
	if user.is_student:
		return render(request, "homePageUser.html", context_dict)
	return render(request, "homePage.html", context_dict)

def login_view(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect('home')
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user:
				login(request, user)
				return HttpResponseRedirect('home')
			return render(
				request, 'login.html',
				{'message': 'Invalid login details'}
			)
	return render(request, "login.html", {})

def logout_view(request):

	logout(request)
	return HttpResponseRedirect('login')

@login_required
def add_course(request):
	context_dict = {}
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	if request.method == 'POST':
		cname = request.POST.get('name')
		abb = request.POST.get('abb')
		duration = request.POST.get('duration')
		if int(duration) > 0:
			course = models.Course.objects.filter(
				name=cname, abbr=abb
			).last()
			if course:
				course.duration = duration
				course.save()
			else:
				models.Course.objects.create(
					name=cname, abbr=abb, duration=duration
				)
		context_dict.update({'message': 'Data saved successfully'})
		return render(request, "addCourse.html", context_dict)
	return render(request, "addCourse.html", context_dict)

@login_required
def add_subject(request):
	courses = models.Course.objects.all()
	context_dict = {
		"all_courses": courses,
	}
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	if request.method == 'POST':
		course = request.POST.get('course_picker')
		name = request.POST.get('name')
		info = request.POST.get('information')

		subject = models.Subject.objects.filter(
			name=name, course_id=course
		).last()
		if subject:
			subject.information = info
			subject.save()
		else:
			models.Subject.objects.create(
				name=name, information=info, course_id=course
			)
		context_dict.update({'message': 'Data saved successfully'})
		return render(request, "addSubject.html", context_dict)
	return render(request, "addSubject.html", context_dict)

@login_required
def add_topic(request):
	context_dict = {
		"all_subjects": context_helper.subject_helper(),
	}
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	if request.method == 'POST':
		subject = request.POST.get('subject')
		name = request.POST.get('name')
		video = request.POST.get('video')
		title = request.POST.get('title')
		desc = request.POST.get('desc')

		topic = models.Topic.objects.filter(
			subject_id=subject, name=name
		).last()
		if topic:
			topic.video = video
			topic.title = title
			topic.description = desc
			topic.save()
		else:
			models.Topic.objects.create(
				name=name, description=desc, subject_id=subject, video=video, title=title
			)
		context_dict.update({'message': 'Data saved successfully'})
		return render(request, "addTopic.html", context_dict)
	return render(request, "addTopic.html", context_dict)

@login_required
def add_payment_details(request):
	context_dict = {}
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user = models.UserProfile.objects.filter(id=user_id).last()
		if not user:
			context_dict.update({'message': 'User ID is incorret'})
			return render(request, "addPaymentStatus.html", context_dict)
		payment_status = request.POST.get('payment_status') #checkbox
		payment_status = True if payment_status == 'on' else False
		payment_details = models.PaymentDetails.objects.filter(user=user).last()
		if payment_details:
			payment_details.payment_done = payment_status
			payment_details.save()
		else:
			models.PaymentDetails.objects.create(
				user=user, payment_done=payment_status
			)
		context_dict.update({'message': 'Data saved successfully'})
		return render(request, "addPaymentStatus.html", context_dict)
	return render(request, "addPaymentStatus.html", context_dict)

@login_required
def view_courses(request):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	context_dict = {
		'title': 'All Courses'
	}
	return render(
		request,
		'viewCourse.html',
		context_dict
	)

@login_required
def view_subjects(request):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	context_dict = {
		'title': 'All Subjects'
	}
	return render(
		request,
		'viewSubject.html',
		context_dict
	)

@login_required
def view_topics(request):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	context_dict = {
		'title': 'All Topics'
	}
	return render(
		request,
		'viewTopic.html',
		context_dict
	)

@login_required
def view_payments(request):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	context_dict = {
		'title': 'All Payment Records'
	}
	return render(
		request,
		'viewPayment.html',
		context_dict
	)

@login_required
def delete_course(request, course_id):

	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	course = models.Course.objects.filter(
		pk=course_id, soft_delete=False
	).first()
	if not course:
		raise Http404
	course.soft_delete = True
	subjects = models.Subject.objects.filter(course=course)
	topics = models.Topic.objects.filter(subject__in=subjects)
	subjects.update(soft_delete=True)
	topics.update(soft_delete=True)
	course.save()
	return HttpResponseRedirect(reverse('view-courses'))

@login_required
def delete_subject(request, subject_id):

	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	subject = models.Subject.objects.filter(
		pk=subject_id, soft_delete=False
	).first()
	if not subject:
		raise Http404
	subject.soft_delete = True
	models.Topic.objects.filter(subject=subject).update(soft_delete=True)
	subject.save()
	return HttpResponseRedirect(reverse('view-subjects'))

@login_required
def delete_topic(request, topic_id):

	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	topic = models.Topic.objects.filter(
		pk=topic_id, soft_delete=False
	).first()
	if not topic:
		raise Http404
	topic.soft_delete = True
	topic.save()
	return HttpResponseRedirect(reverse('view-topics'))

@login_required
def edit_course(request, course_id):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	course = models.Course.objects.filter(
		pk=course_id, soft_delete=False
	).first()
	if not course:
		raise Http404
	context_dict = {
		'course': course
	}
	if request.method == 'POST':
		cname = request.POST.get('name')
		abb = request.POST.get('abb')
		duration = request.POST.get('duration')
		if int(duration) > 0:
			try:
				if course.name != cname:
					course.name = cname
				if course.abbr != abb:
					course.abbr = abb
				if course.duration != duration:
					course.duration = duration
				course.save()
				context_dict['message'] = 'Successfully updated course.'
				context_dict['success'] = True
			except Exception as e:
				context_dict['message'] = str(e)
				context_dict['success'] = False
				print(e)
	if context_dict.get('success', False):
		return HttpResponseRedirect(reverse('view-courses'))
	return render(
		request, "editCourse.html", context_dict
	)

@login_required
def edit_subject(request, subject_id):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	subject = models.Subject.objects.filter(
		pk=subject_id, soft_delete=False
	).first()
	if not subject:
		raise Http404
	courses = models.Course.objects.all()
	context_dict = {
		'subject': subject,
		'course_helper': courses,
	}
	if request.method == 'POST':
		name = request.POST.get('name')
		course = request.POST.get('course_picker')
		info = request.POST.get('information')
		try:
			if subject.name != name:
				subject.name = name
			if subject.course_id != course:
				subject.course_id = course
			if subject.information != info:
				subject.information = info
			subject.save()
			context_dict["message"] = 'Successfully updated subject.'
			context_dict["success"] = True
		except Exception as e:
			context_dict["message"] = str(e)
			context_dict["success"] = False
			print(e)
	if context_dict.get('success', False):
		return HttpResponseRedirect(reverse('view-subjects'))
	return render(
		request, "editSubject.html", context_dict
	)

@login_required
def edit_topic(request, topic_id):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	topic = models.Topic.objects.filter(
		pk=topic_id, soft_delete=False
	).first()
	if not topic:
		raise Http404
	subjects = models.Subject.objects.all()
	context_dict = {
		'topic': topic,
		'subject_helper': subjects,
	}
	if request.method == 'POST':
		name = request.POST.get('name')
		subject = request.POST.get('subject_picker')
		video = request.POST.get('video_link')
		title = request.POST.get('title')
		desc = request.POST.get('description')
		try:
			if topic.name != name:
				topic.name = name
			if topic.subject_id != subject:
				topic.subject_id = subject
			if topic.description != desc:
				topic.description = desc
			if topic.title != title:
				topic.title = title
			if topic.video != video:
				topic.video = video
			topic.save()
			context_dict["message"] = 'Successfully updated topic.'
			context_dict["success"] = True
		except Exception as e:
			context_dict["message"] = str(e)
			context_dict["success"] = False
			print(e)
	if context_dict.get('success', False):
		return HttpResponseRedirect(reverse('view-topics'))
	return render(
		request, "editTopic.html", context_dict
	)

@login_required
def edit_payment_details(request, payment_id):
	emp = models.UserProfile.objects.filter(username=request.user).first()
	if not emp.is_employee:
		raise Http404
	payment = models.PaymentDetails.objects.filter(
		pk=payment_id, soft_delete=False
	).first()
	if not payment:
		raise Http404
	context_dict = {
		'payment': payment,
	}
	if request.method == 'POST':
		payment_status = request.POST.get('payment_status') #checkbox
		payment_status = True if payment_status == 'on' else False
		try:
			if payment.payment_done != payment_status:
				payment.payment_done = payment_status
			payment.save()
			context_dict["message"] = 'Successfully updated payment status.'
			context_dict["success"] = True
		except Exception as e:
			context_dict["message"] = str(e)
			context_dict["success"] = False
			print(e)
	if context_dict.get('success', False):
		return HttpResponseRedirect(reverse('view-payments'))
	return render(
		request, "editPayment.html", context_dict
	)

@login_required
def add_user_course(request):
	
	user = models.UserProfile.objects.filter(username=request.user).first()
	if not user.is_student:
		raise Http404
	courses = models.Course.objects.all()
	user_course = models.UserCourse.objects.filter(
		user=user
	).last()
	context_dict = {
		'courses': courses,
		'user_course': user_course,
	}
	user_payment = models.PaymentDetails.objects.filter(user=user).last()
	if user_payment:
		context_dict.update({'user_payment': user_payment})
	if request.method == 'POST':
		course_id = request.POST.get('course_picker')
		user_course = models.UserCourse.objects.filter(
			user=user
		).last()
		if not user_course:
			user_course = models.UserCourse.objects.create(
				user=user, course_id=course_id
			)
		context_dict.update({'message': 'Course added Successfully'})
		return HttpResponseRedirect(reverse('home'))
	return render(request, "addUserCourse.html", context_dict)

@login_required
def user_view_subject(request):
	user = models.UserProfile.objects.filter(username=request.user).first()
	if not user.is_student:
		raise Http404
	context_dict = {
		'title': 'All Subjects'
	}
	user_course = models.UserCourse.objects.filter(user=user).last()
	if not user_course:
		return HttpResponseRedirect(reverse('add-user-course'))
	return render(request, "userSubjects.html", context_dict)

@login_required
def user_view_topic(request):
	user = models.UserProfile.objects.filter(username=request.user).first()
	if not user.is_student:
		raise Http404
	context_dict = {
		'title': 'All Topics'
	}
	user_course = models.UserCourse.objects.filter(user=user).last()
	if not user_course:
		return HttpResponseRedirect(reverse('add-user-course'))
	return render(request, "userTopics.html", context_dict)

@login_required
def topic_page(request, topic_id):
	user = models.UserProfile.objects.filter(username=request.user).first()
	if not user.is_student:
		raise Http404
	topic = models.Topic.objects.filter(id=topic_id).last()
	context_dict = {'topic': topic}
	return render(request, "topic.html", context_dict)

@login_required
def user_make_payment(request):
	context_dict = {}
	user = models.UserProfile.objects.filter(username=request.user).first()
	if not user.is_student:
		raise Http404
	user_payment = models.PaymentDetails.objects.filter(user=user).last()
	if user_payment:
		context_dict.update({'user_payment': user_payment, 'user': user, 'message': 'Already Paid'})
	if request.method == 'POST':
		models.PaymentDetails.objects.create(user=user, payment_done=False)
		context_dict.update({'message': 'Payment done, waiting for approval.'})
		return HttpResponseRedirect(reverse('home'))
	return render(request, "userMakePayment.html", context_dict)
