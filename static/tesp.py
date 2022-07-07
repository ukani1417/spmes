import pdfkit
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
# pdfkit.from_string(html, 'MyPDF.pdf', configuration=config)
pdfkit.from_file("C://Users//Dhruvin Moradiya//Downloads//spmes-20220623T054856Z-001//spmes//static//template.html", 'out.pdf',configuration=config)