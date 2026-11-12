from .models import AboutPageContent

def site_branding(request):
    """Globally injects about_content and logo to all templates"""
    about_content = AboutPageContent.load() if hasattr(AboutPageContent, 'load') else AboutPageContent.objects.first()
    return {
        'about_content': about_content,
        'about': about_content,  # Covers templates looking for either 'about_content' or 'about'
    }