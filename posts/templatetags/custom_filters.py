from django import template

register = template.Library()

@register.filter(name='is_image')
def is_image(file_url):
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))

@register.filter(name='is_video')
def is_video(url):
    if url.endswith('.mp4'):
        return 'mp4'
    elif url.endswith('.webm'):
        return 'webm'
    elif url.endswith('.ogg'):
        return 'ogg'
    else:
        return 'mp4'