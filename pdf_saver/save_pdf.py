from weasyprint import HTML
import markdown

def markdown_to_pdf(md_text):
    md_text = str(md_text)  # ensures it’s a string
    html_content = markdown.markdown(md_text, extensions=["tables"])

    styled_html = f"""
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 12mm; }}
        body {{ font-family: Arial, sans-serif; line-height: 1.4; font-size: 10pt; word-wrap: break-word; }}
        h1 {{ color: #2C3E50; margin-top: 0; }}
        h2 {{ color: #34495E; }}
        h3 {{ color: #555; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
            table-layout: fixed; /* <-- key to prevent overflow */
            word-wrap: break-word; /* <-- ensures text wraps */
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 6px 8px;
            text-align: left;
            font-size: 9pt;
            overflow-wrap: break-word; /* wrap long words */
        }}
        th {{ background-color: #f2f2f2; }}
        table, tr, td, th {{ page-break-inside: avoid; }}
        img {{
            display: block;
            margin: 12px auto;
            max-width: 90%;
            height: auto;
        }}
    </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    pdf_bytes = HTML(string=styled_html).write_pdf()
    return pdf_bytes