from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from lms import models
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils import timezone
import pytz
import datetime
from django.conf import settings


class CourseListDatatable(BaseDatatableView):
    model = models.Course

    columns = [
        'id', 'name', 'abbr', 'duration', 'id', 'id'
    ]
    order_columns = [
        'id', 'name', 'abbr', 'duration', 'id', 'id'
    ]

    max_display_length = 500

    def get_initial_queryset(self):
        return models.Course.objects.filter(soft_delete=False).order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(abbr__icontains=search) | 
                    Q(duration__icontains=search)
            )
        return qs

    def prepare_results(self, qs):
        data = []
        for item in qs:
            data.append([
                item.id,
                item.name,
                item.abbr,
                item.duration,
                'edit-course/'+str(item.pk),
                'delete-course/'+str(item.pk),
            ])
        return data
