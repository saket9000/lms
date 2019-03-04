from django.contrib import admin
from lms.models import UserProfile, Course, Subject, Topic, PaymentDetails, UserCourse
# Register your models here.

class DeleteNotAllowedAdmin(admin.ModelAdmin):
	def has_delete_permission(self, request, obj=None):
		return False

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(UserCourse)
admin.site.register(PaymentDetails)
admin.site.disable_action("delete_selected")
