from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
from bs4 import BeautifulSoup

def render_to_pdf(template_name, context, request):
    page_count = 1
    css_string = '@page {size: A4; margin: 20px;}\n'+'.header-column {width: 170px !important;}\n'
    temp_add_details = ""
    for additional_detail in context['test'].additional_details:
        page_count += 1
        if (additional_detail != context['test'].additional_details[-1]):
            temp_add_details += additional_detail+"<p class='page_break'></p>"
        else:
            temp_add_details += additional_detail
    context['test'].additional_details = temp_add_details
    html_content = render_to_string(template_name, context)
    css = CSS(string=css_string)
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    return pdf, page_count

def render_contents_to_pdf(template_name, context, request):
    html_content = render_to_string(template_name, context)
    css_string = '@page {size: A4; margin: 50px;}'
    css = CSS(string=css_string)
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    return pdf

def render_cover_to_pdf(template_name, context, request):
    html_content = render_to_string(template_name, context)
    css_string = '@page {size: A4; margin: 30px;}'
    css = CSS(string=css_string)
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    return pdf