from django.contrib import admin
from .models import HeroSection, HeroFeaturedCard, Feature, PremiumResource, Course, CourseLearningPoint, SuccessStory, FAQ, AboutPageContent

class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

class CourseLearningPointInline(admin.TabularInline):
    model = CourseLearningPoint
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseLearningPointInline]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(HeroSection, SingletonAdmin)
admin.site.register(HeroFeaturedCard, SingletonAdmin)
admin.site.register(Feature)
admin.site.register(PremiumResource)
admin.site.register(Course, CourseAdmin)
admin.site.register(SuccessStory)
admin.site.register(FAQ)
admin.site.register(AboutPageContent, SingletonAdmin)