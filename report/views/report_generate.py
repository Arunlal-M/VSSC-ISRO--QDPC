from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render
from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
import os
from django.conf import settings
# from .models import Report

# def generate_pdf(request):
#     template_path = 'report/qar_report_template.html'
#     context = {
#         "report_no": "VSSC/QDPC/AK/F1691/2024/Rec.: 2451",
#         "date": "25-10-2024",
#         "product_name": "Product-A",
#         "batch_details": [
#             {"batch_no": "Div-1/Product-A/0116/2024", "dom": "27.07.2024", "doe": "26.07.2025", "size": "2250"},
#             {"batch_no": "Div-1/Product-A/0117/2024", "dom": "27.07.2024", "doe": "26.07.2025", "size": "2310"},
#         ],
#     }
    
#     template = get_template()
#     html = template.render(context)
    
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'

#     pdf_status = pisa.CreatePDF(html, dest=response)
    
#     if pdf_status.err:
#         return HttpResponse("Error rendering PDF", status=400)

#     return response

class ReportView(BaseModelViewSet):
    template_name = 'qar_report_template.html'

    def get(self, request):
        return render(request, self.template_name)
