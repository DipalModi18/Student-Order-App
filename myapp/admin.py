from django.contrib import admin
from  .models import Topic, Course, Student, Order, Review


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'price', 'for_everyone', 'description')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('student', 'order_status', 'order_date')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'course', 'rating', 'comments', 'date')


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
