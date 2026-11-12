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

class HeroFeaturedCard(models.Model):
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, help_text="Select a course to feature")
    is_active = models.BooleanField(default=True, help_text="Check to show this card on the homepage, uncheck to hide it completely")
    button_text = models.CharField(max_length=50, default="Enroll Now")

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton enforcement
        super().save(*args, **kwargs)

    @property
    def should_display(self):
        """Returns True only if card is active AND a course is selected"""
        return self.is_active and self.course is not None

    @property
    def title(self):
        return self.course.title if self.course else ""

    @property
    def price(self):
        return self.course.price if self.course else 0

    @property
    def original_price(self):
        return self.course.original_price if self.course else 0

    @property
    def course_slug(self):
        return self.course.slug if self.course else ""

    @property
    def learning_points(self):
        if self.course:
            return self.course.learning_points.all()
        return []

    def __str__(self):
        status = "Visible" if self.should_display else "Hidden"
        return f"Hero Featured Card [{status}]: {self.course.title if self.course else 'No Course Selected'}"

class Feature(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_image = models.ImageField(upload_to='features/', blank=True, null=True, help_text="Upload feature icon or image")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title

class PremiumResource(models.Model):
    ICON_CHOICES = [
        ('⭐', 'Star (⭐)'),
        ('📚', 'Book (📚)'),
        ('💡', 'Bulb (💡)'),
        ('📝', 'Document / Notes (📝)'),
        ('🎯', 'Target (🎯)'),
        ('🏆', 'Trophy (🏆)'),
        ('🔒', 'Lock / Exclusive (🔒)'),
        ('📊', 'Chart (📊)'),
    ]

    title = models.CharField(max_length=150)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default='⭐', help_text="Select an icon from the dropdown")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default="course-slug")
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(default="This comprehensive course introduces you to the world of medical coding.")
    instructor = models.CharField(max_length=100)
    instructor_bio = models.TextField(default="Certified professional coder with years of industry experience.")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    reviews_count = models.CharField(max_length=50, default="1250")
    students_count = models.CharField(max_length=50, default="1.2k")
    price = models.CharField(max_length=50, default="12,999")
    original_price = models.CharField(max_length=50, default="30,000")
    exam_fees = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. $721 exam fees")
    badge_text = models.CharField(max_length=150, default="For freshers")
    status_badge = models.CharField(max_length=50, blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Enroll Now")
    button_url = models.CharField(max_length=100, default="/login")
    
    level = models.CharField(max_length=50, default="Beginner Level")
    duration = models.CharField(max_length=50, default="4-6 weeks")
    format = models.CharField(max_length=100, default="Live Online Sessions")
    outcome = models.TextField(default="Ready for CPC/CCS preparation")

    lessons_count = models.IntegerField(blank=True, null=True)
    
    syllabus_data = models.TextField(
        blank=True, null=True,
        help_text="Format per line: Module Title | Lesson 1 (Time), Lesson 2 (Time)"
    )

    def __str__(self):
        return self.title

class CourseSlot(models.Model):
    TIME_SLOT_CHOICES = [
        ('08:00 AM - 10:00 AM', 'Morning Batch (08:00 AM - 10:00 AM)'),
        ('10:00 AM - 12:00 PM', 'Late Morning Batch (10:00 AM - 12:00 PM)'),
        ('02:00 PM - 04:00 PM', 'Afternoon Batch (02:00 PM - 04:00 PM)'),
        ('06:00 PM - 08:00 PM', 'Evening Batch (06:00 PM - 08:00 PM)'),
        ('08:00 PM - 10:00 PM', 'Night Batch (08:00 PM - 10:00 PM)'),
        ('Custom', 'Custom Timing'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='slots')
    slot_name = models.CharField(max_length=150, help_text="e.g., Batch 1 - Weekend / Weekday")
    start_date = models.DateField(help_text="Select batch start date")
    end_date = models.DateField(null=True, blank=True, help_text="Select batch end date") # <-- Added null=True, blank=True
    timing_info = models.CharField(
        max_length=50, 
        choices=TIME_SLOT_CHOICES, 
        default='06:00 PM - 08:00 PM',
        help_text="Select standard AM/PM time slot"
    )
    max_capacity = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.course.title} — {self.slot_name} ({self.timing_info})"

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
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text="Upload site-wide logo image")
    
    tagline = models.CharField(max_length=100, default="About")
    title = models.CharField(max_length=200, default="Empowering the Next Generation of Certified Medical Coders")
    subtitle = models.TextField(default="Based in Ameerpet, Hyderabad and Berhampur, Odisha, AspireFounder has a clear mission.")
    
    mission_title = models.CharField(max_length=150, default="Our Mission")
    mission_text = models.TextField(default="To make high-quality, affordable, and globally-aligned medical coding education accessible to freshers, graduates, and career-switchers across India.")
    
    why_choose_title = models.CharField(max_length=150, default="Why Choose AspireFounder?")
    why_choose_points = models.TextField(default="Courses aligned with CPC & CCS certifications\nTrainers with 7+ years of real-world experience")

    vision_title = models.CharField(max_length=150, default="Our Vision")
    vision_text = models.TextField(default="To become India's most trusted medical coding training institute.")

    commitment_title = models.CharField(max_length=150, default="Our Commitment")
    commitment_text = models.TextField(default="We believe in honest, practical, and structured learning.")

    bottom_tagline = models.CharField(max_length=250, default="Whether you're starting from scratch or upskilling for your dream job.")
    button_text = models.CharField(max_length=50, default="Explore Our Courses")
    button_url = models.CharField(max_length=100, default="/#courses")

    def __str__(self):
        return "About Page Content"

class Enrollment(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    course_title = models.CharField(max_length=200)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=12999.00)
    upi_transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="12-digit UTR or UPI transaction reference number")
    
    # --- Course Slot Relation Added ---
    assigned_slot = models.ForeignKey(CourseSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrolled_students')
    
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        status = 'Verified' if self.verified else 'Pending'
        slot_info = f" | Slot: {self.assigned_slot.slot_name}" if self.assigned_slot else ""
        return f"{self.full_name} - {self.course_title}{slot_info} ({status})"

class PaymentSetting(SingletonModel):
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI QR Code Payment'),
        ('bank', 'Direct Bank Transfer'),
    ]
    
    active_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='upi', 
        help_text="Select which payment method to display on the checkout page"
    )
    
    upi_id = models.CharField(max_length=100, default="yourbusiness@upi", help_text="e.g. aspirefounder@okhdfcbank")
    upi_name = models.CharField(max_length=100, default="AspireFounder")
    qr_code_image = models.ImageField(upload_to='payments/', blank=True, null=True, help_text="Upload your UPI QR code image")
    
    bank_account_name = models.CharField(max_length=150, default="AspireFounder Education")
    bank_account_number = models.CharField(max_length=50, default="123456789012")
    bank_ifsc = models.CharField(max_length=20, default="HDFC0001234")
    bank_name = models.CharField(max_length=100, default="HDFC Bank")
    bank_logo = models.ImageField(upload_to='payments/banks/', blank=True, null=True, help_text="Upload bank logo image")

    def __str__(self):
        return f"Payment Settings [Active: {self.get_active_method_display()}]"