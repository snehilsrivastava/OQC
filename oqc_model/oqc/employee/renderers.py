import os
from django.conf import settings
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # Make sure media and static files are correctly handled
    base_url = os.path.join(settings.BASE_DIR, 'static')

    # Create a PDF document
    pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=result, link_callback=link_callback, path=base_url)

    if pdf.err:
        return None  # Return None if an error occurs during PDF generation
    else:
        return result.getvalue()

def link_callback(uri, rel):
    # Convert HTML URIs to absolute system paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (settings.MEDIA_URL, settings.STATIC_URL)
        )
    return path
