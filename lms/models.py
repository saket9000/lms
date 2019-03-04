from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TimeStampModel(models.Model):

	""" 
	Abstract class for all models to store created, updated and
	deleted informarion (Time Manage).
	"""

	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
	soft_delete = models.BooleanField(default=False)

	class Meta:
		abstract = True


class UserProfile(AbstractUser, TimeStampModel):

	GENDER_TYPE = (
		('M', 'Male'),
		('F', 'Female'),
	)

	name = models.CharField(max_length=100)
	username = models.CharField(max_length=50, null=True, blank=True, unique=True)
	mobile = models.CharField(max_length=10, null=True, blank=True, unique=True)
	dob = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=2, null=False, choices=GENDER_TYPE, blank=True)
	email = models.CharField(max_length=100)
	address = models.CharField(max_length=250, null=True, blank=True)
	photo = models.ImageField(upload_to='profile-images', null=True)
	is_student = models.BooleanField(default=False)
	is_employee = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(str(self.name) + '-' + str(self.id))

	class Meta:
		unique_together = ["mobile", "email"]


class Course(TimeStampModel):

	"""
	Course details.
	"""

	name = models.CharField(max_length=100, null=False, unique=True)
	abbr = models.CharField(max_length=20, db_index=True, unique=True)
	duration = models.IntegerField()

	def __unicode__(self):
		return unicode((self.name) + '-' + (self.abbr))


class Subject(TimeStampModel):
	course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
	name = models.CharField(max_length=30 ,null=False, blank=False)
	information = models.TextField()

	def __unicode__(self):
		return unicode(str(self.name))


class Topic(TimeStampModel):
	subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True, blank=True)
	name = models.CharField(max_length=100, db_index=True)
	video = models.CharField(max_length=200, null=True, blank=True)
	title = models.TextField()
	description = models.TextField()

	def __unicode__(self):
		return unicode(str(self.name) + '-' + str(self.title))


class UserCourse(TimeStampModel):
	user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
	course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

	def __unicode__(self):
		return unicode(str(userprofile) + '-' + str(self.course))


class PaymentDetails(TimeStampModel):
	user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, null=False, blank=False)
	payment_done = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(str(userprofile) + '-' + str(self.payment_done))
