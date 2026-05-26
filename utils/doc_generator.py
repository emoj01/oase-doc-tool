# file: doc_genertor.py
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path

TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("output")

def generate_pdf(data: dict, output_file_name: str):
    OUTPUT_DIR.mkdir(exist_ok=True)

    # loading Jinja2 Environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("oase_dokument.html")

    html_string = template.render(**data)

    output_path = OUTPUT_DIR / output_file_name
    HTML(string=html_string).write_pdf(output_path)

    return output_path