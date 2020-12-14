from django.contrib import admin
from  .models import Topic, Course, Student, Order, Review
from decimal import Decimal


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')
    actions = ['reduce_price']

    def reduce_price(self, request, queryset):
        for course in queryset:
            course.price = course.price * Decimal.from_float(0.9)
            course.save()
    reduce_price.short_description = "Reduce Course Price by 10%%"


class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')
    inlines = [CourseInline]


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'level', 'get_registered_courses')


class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('student', 'order_status', 'order_date')]
    list_display = ('id', 'student', 'order_status', 'order_date', 'total_items')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'course', 'rating', 'comments', 'date')


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
