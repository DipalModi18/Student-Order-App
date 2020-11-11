from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render
from .forms import SearchForm


# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    courses = Course.objects.filter(topic=Topic.objects.get(id=1))
    return render(request, 'myapp/detail.html', {'topic': topic, 'courses': courses})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            topics = Topic.objects.filter(length=length)
            courselist = []
            for top in topics:
                courselist = courselist + list(top.courses.all())
            return render(request, 'myapp/results.html', {'courselist':courselist, 'name':name})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form':form})
