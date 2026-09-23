from django.db import models

class SingletonModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class HeroSection(SingletonModel):
    title_line_1 = models.CharField(max_length=150, default="Decode your future.")
    title_line_2 = models.CharField(max_length=150, default="Learn, Certify, Get Hired.")
    subtitle = models.TextField(default="Master Medical Coding, Billing, CCS, CPC, and RCM with industry experts.")
    students_count = models.CharField(max_length=50, default="1000+")
    placement_rate = models.CharField(max_length=50, default="95%")
    content_hours = models.CharField(max_length=50, default="50+")

class HeroFeaturedCard(SingletonModel):
    title = models.CharField(max_length=200, default="Medical Coding Foundation Program")
    price = models.CharField(max_length=50, default="12,999")
    original_price = models.CharField(max_length=50, default="30,000")
    button_text = models.CharField(max_length=50, default="Enroll Now")
    button_url = models.CharField(max_length=100, default="/login")

class Feature(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_emoji = models.CharField(max_length=10, default="👥")
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title

class PremiumResource(models.Model):
    title = models.CharField(max_length=150)
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default="course-slug")
    subtitle = models.CharField(max_length=250, blank=True, null=True) # Not mandatory
    description = models.TextField(default="This comprehensive course introduces you to the world of medical coding.")
    instructor = models.CharField(max_length=100)
    instructor_bio = models.TextField(default="Certified professional coder with years of industry experience.")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    reviews_count = models.CharField(max_length=50, default="1250")
    students_count = models.CharField(max_length=50, default="1.2k")
    price = models.CharField(max_length=50, default="12,999")
    original_price = models.CharField(max_length=50, default="30,000")
    exam_fees = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. $721 exam fees") # Added exam fees
    badge_text = models.CharField(max_length=150, default="For freshers")
    status_badge = models.CharField(max_length=50, blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Enroll Now")
    button_url = models.CharField(max_length=100, default="/login")
    
    level = models.CharField(max_length=50, default="Beginner Level")
    duration = models.CharField(max_length=50, default="4-6 weeks")
    format = models.CharField(max_length=100, default="Live Online Sessions")
    outcome = models.TextField(default="Ready for CPC/CCS preparation")

    lessons_count = models.IntegerField(blank=True, null=True) # Not mandatory field
    
    # Syllabus Data is optional now
    syllabus_data = models.TextField(
        blank=True, null=True,
        help_text="Format per line: Module Title | Lesson 1 (Time), Lesson 2 (Time)"
    )

    def __str__(self):
        return self.title

# Added inline/related model for adding learning points one by one
class CourseLearningPoint(models.Model):
    course = models.ForeignKey(Course, related_name='learning_points', on_delete=models.CASCADE)
    point_text = models.CharField(max_length=250)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.point_text

class SuccessStory(models.Model):
    student_name = models.CharField(max_length=100)
    quote = models.TextField()
    designation = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    rating_stars = models.IntegerField(default=5, help_text="Enter number of filled stars (1 to 5)")

    def __str__(self):
        return self.student_name

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.question

class AboutPageContent(SingletonModel):
    tagline = models.CharField(max_length=100, default="About")
    title = models.CharField(max_length=200, default="Empowering the Next Generation of Certified Medical Coders")
    subtitle = models.TextField(default="Based in Ameerpet, Hyderabad and Berhampur, Odisha, AspireFounder has a clear mission.")
    
    # Mission Card
    mission_title = models.CharField(max_length=150, default="Our Mission")
    mission_text = models.TextField(default="To make high-quality, affordable, and globally-aligned medical coding education accessible to freshers, graduates, and career-switchers across India. At AspireFounder, we specialize in training students for CPC (AAPC) and CCS (AHIMA) certifications – the most recognized medical coding credentials in the world. Whether you're from BPharma, MPharma, BSc, MSc, BHMS, BAMS, BSc Nursing, MSc Nursing, Life Sciences, or Allied Health backgrounds, our beginner-to-advanced programs help you build the skills and confidence to enter the rapidly growing global healthcare market.")
    
    # Why Choose Us Points (Comma separated or newline separated)
    why_choose_title = models.CharField(max_length=150, default="Why Choose AspireFounder?")
    why_choose_points = models.TextField(default="Courses aligned with CPC & CCS certifications\nTrainers with 7+ years of real-world hospital & healthcare coding experience\nCareer-focused curriculum for freshers\nFlexible live online training from Ameerpet, Hyderabad and Berhampur, Odisha\nHands-on practice with real coding scenarios & mock exams\nAffordable pricing with exam & career guidance")

    # Vision Card
    vision_title = models.CharField(max_length=150, default="Our Vision")
    vision_text = models.TextField(default="To become India's most trusted medical coding training institute, where thousands of students launch rewarding careers in the healthcare and healthtech industries both in India and abroad.")

    # Commitment Card
    commitment_title = models.CharField(max_length=150, default="Our Commitment")
    commitment_text = models.TextField(default="We believe in honest, practical, and structured learning. No overpromises – just focused, step-by-step guidance to help you get certification-ready and career-confident.")

    # Bottom Callout
    bottom_tagline = models.CharField(max_length=250, default="Whether you're starting from scratch or upskilling for your dream job, AspireFounder is here to support your journey every step of the way.")
    button_text = models.CharField(max_length=50, default="Explore Our Courses")
    button_url = models.CharField(max_length=100, default="/#courses")

    def __str__(self):
        return "About Page Content"