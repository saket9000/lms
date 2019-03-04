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


class UserSubjectListDatatable(BaseDatatableView):
    model = models.Subject

    columns = [
        'id', 'name', 'id'
    ]
    order_columns = [
        'id', 'name', 'id'
    ]

    max_display_length = 500

    def get_initial_queryset(self):
        user = models.UserProfile.objects.filter(username=self.request.user).last()
        user_course = models.UserCourse.objects.filter(user=user).last()
        user_payment = models.PaymentDetails.objects.filter(user=user).last()
        if not user_payment or user_payment.payment_done == False:
            qs = models.Subject.objects.filter(soft_delete=False, course=user_course.course)
            valid_ids = qs.values_list('id', flat=True)[:2]
            list_ids = list(valid_ids)
            return models.Subject.objects.filter(id__in=list_ids)
        return models.Subject.objects.filter(soft_delete=False, course=user_course.course).order_by('-id')

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
                'user-topics',
            ])
        return data
