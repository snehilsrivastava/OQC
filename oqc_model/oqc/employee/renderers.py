import os
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
import pdfkit
from weasyprint import HTML, CSS
from xhtml2pdf import pisa
from io import BytesIO
from bs4 import BeautifulSoup


# def render_to_pdf(html_content, request):
#     # html_content = render_to_string(template, context)
#     pdf_buffer = BytesIO()
#     # Make sure media and static files are correctly handled
#     base_url = os.path.join(settings.BASE_DIR, 'media')
#     print(settings.BASE_DIR)
#     print(base_url)
#     pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_buffer, path=base_url)
#     pdf_buffer.seek(0)
#     pdf_data = pdf_buffer.getvalue()
#     pdf_buffer.close()
#     return pdf_data

# def link_callback(uri, rel):
#     # uri = uri.replace('/','\\')
#     # print(settings.MEDIA_URL.replace('/','\\'))
#     # print(settings.MEDIA_ROOT)
#     # Convert HTML URIs to absolute system paths
#     if uri.startswith(settings.MEDIA_URL.replace('/','\\')):
#         # print(f"TEST MEDIA")
#         path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL.replace('/','\\'), ""))
#     elif uri.startswith(settings.STATIC_URL):
#         # print(f"TEST STATIC")
#         path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
#     else:
#         # print(f"TEST???")
#         return uri
#     # print(f"TEST?: {uri}")
#     # print(f"{path}")
#     if not os.path.isfile(path):
#         raise Exception(
#             'media URI must start with %s or %s' % (settings.MEDIA_URL, settings.STATIC_URL)
#         )
#     return path

# def render_to_pdf(template_name, context={}):
#     html_content = render_to_string(template_name, context)
#     # html_content = html_content.encode('utf-8')
#     path = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=path)
#     pdf_options = {
#         # 'quiet': True,
#         # 'font': 'Courier',
#         # 'margin-left': 0,
#         'enable-local-file-access': None,
#     }
#     pdf = pdfkit.from_string(html_content, options=pdf_options, configuration=config, css=None)
#     # response = HttpResponse(pdf, content_type='application/pdf')
#     # response['Content-Disposition'] = 'attachment; filename=view_test_record.pdf'
#     # return response
#     return pdf

def render_to_pdf(template_name, context, request):
    rtf = context['test'].result
    soup = BeautifulSoup(rtf, 'html.parser')
    images = []
    i = 1
    for img in soup.find_all('img'):
        img['class'] = f'c{i}'
        height = img.get('height')
        width = img.get('width')
        images.append((i, height, width))
        i += 1
    css_string = '@page {size: A4; margin: 0;}\n'
    for i, height, width in images:
        css_string += f'.c{i} {{height: {height}px; width: {width}px}}\n'
    context['test'].result = str(soup)
    html_content = render_to_string(template_name, context)
    css = CSS(string=css_string)
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    return pdf
