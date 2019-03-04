from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from lms import models
from django.urls import reverse
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils import timezone
import pytz
import datetime
from django.conf import settings


class UserTopicListDatatable(BaseDatatableView):
	model = models.Topic

	columns = [
		'id', 'name', 'subject', 'title', 'id',
	]
	order_columns = [
		'id', 'name', 'subject', 'title', 'id',
	]

	max_display_length = 500

	def get_initial_queryset(self):
		user = models.UserProfile.objects.filter(username=self.request.user).last()
		user_course = models.UserCourse.objects.filter(user=user).last()
		user_payment = models.PaymentDetails.objects.filter(user=user).last()
		if not user_payment or user_payment.payment_done == False:
			qs = models.Topic.objects.filter(soft_delete=False, subject__course=user_course.course)
			valid_ids = qs.values_list('id', flat=True)[:5]
			list_ids = list(valid_ids)
			return models.Topic.objects.filter(id__in=list_ids)
		return models.Topic.objects.filter(soft_delete=False, subject__course=user_course.course).order_by('-id')

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(
				Q(name__icontains=search)
			)
		return qs

	def prepare_results(self, qs):
		data = []
		for idx, item in enumerate(qs, 1):
			data.append([
				idx,
				item.name,
				item.subject.name,
				item.title,
				'topic/'+str(item.pk),
			])
		return data
