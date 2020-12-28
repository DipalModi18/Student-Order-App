from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)

    def __str__(self):
        return self.name


def validate_price(price):
    if price < 50 or price > 500:
        raise ValidationError('Price should be between 50$ to 500$')


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='uploads/', blank=True)

    def __str__(self):
        return "Student Name: {} {} || Address: {}, {}".format(self.first_name, self.last_name, self.address, self.province)

    def get_registered_courses(self):
        return ", ".join([course.title for course in self.registered_courses.all()])
    get_registered_courses.short_description = 'Registered Courses'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')]
    courses = models.ManyToManyField(Course, blank=True)
    student = models.ForeignKey(Student, related_name="orders", on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return "{} {} {} {}".format(self.order_date, self.courses, self.student, self.order_status)

    def total_cost(self):
        cost = 0
        for course in self.courses.all():
            cost = cost + course.price
        return cost

    def total_items(self):
        return self.courses.count()


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return "Reviewer {} has provided rating {} for the Course {}".format(self.reviewer, self.course, self.rating)


class City(models.Model):
  name = models.CharField(max_length=100, unique=True)
  population = models.IntegerField()

  def __str__(self):
    return self.name


class Team(models.Model):
  name = models.CharField(max_length=50)
  sport = models.CharField(max_length=50)
  city = models.ForeignKey(City, on_delete=CASCADE)

  def __str__(self):
    return self.name

class Player(models.Model):
  name = models.CharField(max_length=50)
  teams = models.ManyToManyField(Team)

  def __str__(self):
    return self.name