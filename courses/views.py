from django.shortcuts import render, get_object_or_404
from .models import HeroSection, HeroFeaturedCard, Feature, PremiumResource, Course, SuccessStory, FAQ, AboutPageContent

def home(request):
    hero = HeroSection.objects.first()
    hero_card = HeroFeaturedCard.objects.first()
    features = Feature.objects.all()
    resources = PremiumResource.objects.all()
    courses = Course.objects.all()
    stories = SuccessStory.objects.all()
    faqs = FAQ.objects.all()
    
    context = {
        'hero': hero,
        'hero_card': hero_card,
        'features': features,
        'resources': resources,
        'courses': courses,
        'stories': stories,
        'faqs': faqs,
    }
    return render(request, 'index.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    parsed_modules = []
    if course.syllabus_data:
        for line in course.syllabus_data.split('\n'):
            if '|' in line:
                mod_title, lessons_raw = line.split('|', 1)
                lessons = []
                for item in lessons_raw.split(','):
                    item = item.strip()
                    if '(' in item and item.endswith(')'):
                        l_name, l_time = item.rsplit('(', 1)
                        lessons.append({'name': l_name.strip(), 'time': l_time[:-1].strip()})
                    else:
                        lessons.append({'name': item, 'time': ''})
                parsed_modules.append({'title': mod_title.strip(), 'lessons': lessons})

    context = {
        'course': course,
        'parsed_modules': parsed_modules,
    }
    return render(request, 'course_detail.html', context)

def about(request):
    about_content = AboutPageContent.objects.first()
    
    # Split why choose points into a clean list
    why_points = []
    if about_content and about_content.why_choose_points:
        why_points = [p.strip() for p in about_content.why_choose_points.split('\n') if p.strip()]

    context = {
        'about': about_content,
        'why_points': why_points,
    }
    return render(request, 'about.html', context)