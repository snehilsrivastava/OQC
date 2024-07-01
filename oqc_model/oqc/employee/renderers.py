from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
from bs4 import BeautifulSoup

def render_to_pdf(template_name, context, request):
    soup = BeautifulSoup(context['test'].result, 'html.parser')
    images = []
    i = 1
    for img in soup.find_all('img'):
        img['class'] = f'c{i}'
        height = img.get('height')
        width = img.get('width')
        images.append((i, height, width))
        i += 1
    css_string = '@page {size: A4; margin: 20px;}\n'
    for i, height, width in images:
        css_string += f'.c{i} {{height: {height}px; width: {width}px}}\n'
    context['test'].result = str(soup)

    soup = BeautifulSoup(context['test'].additional_details, 'html.parser')
    paragraphs = soup.find_all('p')
    page_break_paragraphs = [p for p in paragraphs if p.text.strip().lower() == "pagebreak"]
    for p in page_break_paragraphs:
        p.string = ""
        p['class'] = 'page_break'
    context['test'].additional_details = str(soup)

    html_content = render_to_string(template_name, context)
    css = CSS(string=css_string)
    pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])
    return pdf
