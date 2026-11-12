from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    HeroSection, HeroFeaturedCard, Feature, PremiumResource, 
    Course, SuccessStory, FAQ, PaymentSetting
)
from .forms import EnrollmentForm

def home(request):
    hero = HeroSection.load() if hasattr(HeroSection, 'load') else HeroSection.objects.first()
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
    from .models import AboutPageContent
    about_content = AboutPageContent.load() if hasattr(AboutPageContent, 'load') else AboutPageContent.objects.first()
    
    why_points = []
    if about_content and about_content.why_choose_points:
        why_points = [p.strip() for p in about_content.why_choose_points.split('\n') if p.strip()]

    context = {
        'about': about_content,
        'why_points': why_points,
    }
    return render(request, 'about.html', context)


# --- Enrollment & UPI / Bank Transfer Checkout Views ---

def checkout_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    payment_settings = PaymentSetting.load() if hasattr(PaymentSetting, 'load') else PaymentSetting.objects.first()
    
    course_name = course.title
    course_price = str(course.price)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course_title = course_name
            clean_price = course_price.replace(',', '').strip()
            enrollment.amount_paid = float(clean_price) if clean_price else 12999.00
            enrollment.save()
            return redirect('enrollment_success')
    else:
        form = EnrollmentForm()

    context = {
        'form': form,
        'course': course,
        'course_name': course_name,
        'course_price': course_price,
        'payment_settings': payment_settings,
    }
    return render(request, 'courses/checkout.html', context)

def enrollment_success(request):
    return render(request, 'courses/enrollment_success.html')