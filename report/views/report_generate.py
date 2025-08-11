


from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from qdpc_core_models.models.product_batchlist import ProductBatch
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
import os
from django.contrib.contenttypes.models import ContentType
from qdpc_core_models.models.consumable import Consumable,PreCertification
from django.conf import settings
from io import BytesIO

class ReportView(BaseModelViewSet):
    template_name = 'qar_report_template.html'
    pdf_template_name = 'qar_report_pdf_template.html'
    def get_precertification(self, obj):
            try:
                content_type = ContentType.objects.get_for_model(obj)
                precert = PreCertification.objects.get(content_type=content_type, object_id=obj.id)
                return {
                    'certified_by': precert.certified_by.name,
                    'certificate_reference_no': precert.certificate_reference_no,
                    'certificate_issue_date': precert.certificate_issue_date,
                    'certificate_valid_till': precert.certificate_valid_till,
                    'certificate_file': precert.certificate_file.url if precert.certificate_file else None,
                    'certificate_disposition': precert.certificate_disposition,
                }
            except PreCertification.DoesNotExist:
                return None

    def get(self, request, batch_id=None):
        try:
            if not batch_id:
                return HttpResponseNotFound("Batch ID is required")

            batch = ProductBatch.objects.get(id=batch_id)
            product = batch.product
            process = batch.Process

            raw_materials = []
            if product and hasattr(product, 'rawmaterial'):
                for rm in product.rawmaterial.all():
                    acceptance_test_data = [
                        {
                            'name': test.name,
                            'min_value': test.min_value,
                            'max_value': test.max_value,
                            'unit': test.unit.name if test.unit else None,
                            'test_type': test.test_type,
                            'test_result': test.test_result,
                            'specification_result': test.specification_result,
                            'reevaluation_frequency_value': test.reevaluation_frequency_value,
                            'reevaluation_frequency_unit': test.reevaluation_frequency_unit,
                            'reevaluation_frequency': str(test.reevaluation_frequency)
                        }
                        for test in rm.acceptance_test.all()
                    ]

                    raw_materials.append({
                        'material': rm.id,
                        'rawmaterial_name': rm.name,
                        'suppliers': rm.suppliers,
                        'sources':rm.sources,
                        'grade':rm.grade,
                        'acceptance_tests': acceptance_test_data,
                        'precertification': self.get_precertification(rm)
                    })

            consumables = []
            if product and hasattr(product, 'consumable'):
                for c in product.consumable.all():
                    consumables.append({
                        'consumable': c.id,
                        'consumable_name': c.name,
                        'suppliers': c.suppliers,
                        'sources':rm.sources,
                        'grade':rm.grade,
                        'precertification': self.get_precertification(c)
                    })

            components = []
            if product and hasattr(product, 'components'):
                for comp in product.components.all():
                    components.append({
                        'component': comp.id,
                        'component_name': comp.name,
                        'suppliers': comp.suppliers,
                        'sources':rm.sources,
                        'grade':rm.grade,
                        'precertification': self.get_precertification(comp)
                    })

            process_steps = process.processstep_set.all() if process and hasattr(process, 'processstep_set') else []
            equipment_list = product.equipment.all() if product and hasattr(product, 'equipment') else []

            context = {
                'batch': batch,
                'product': product,
                'process': process,
                'raw_materials': raw_materials,
                'consumables': consumables,
                'components': components,
                'process_steps': process_steps,
                'equipment_list': equipment_list,
                'today': timezone.now().date(),
                'batch_id': batch_id,
                'company_logo': os.path.join(settings.STATIC_URL, 'img/logo.png'),
            }

            if request.GET.get('format') == 'pdf':
                return self._generate_pdf_response(context)

            return render(request, self.template_name, context)

        except ProductBatch.DoesNotExist:
            return HttpResponseNotFound(f"Batch with ID {batch_id} not found")
        except Exception as e:
            return HttpResponse(f"Error generating report: {str(e)}", status=500)





    def _generate_pdf_response(self, context):
        """Generate PDF from the template and return as response"""
        try:
            template = get_template(self.pdf_template_name or self.template_name)
            html = template.render(context)
            
            result = BytesIO()
            pdf = pisa.pisaDocument(
                BytesIO(html.encode("UTF-8")), 
                result,
                encoding='UTF-8',
                link_callback=self._link_callback
            )
            
            if not pdf.err:
                response = HttpResponse(
                    result.getvalue(), 
                    content_type='application/pdf'
                )
                filename = f"QAR_Report_{context['batch_id']}_{context['today']}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            return HttpResponse("Error generating PDF", status=500)
        except Exception as e:
            return HttpResponse(f"PDF generation error: {str(e)}", status=500)

    def _link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        static_url = settings.STATIC_URL
        static_root = settings.STATIC_ROOT
        media_url = settings.MEDIA_URL
        media_root = settings.MEDIA_ROOT
        
        if uri.startswith(media_url):
            path = os.path.join(media_root, uri.replace(media_url, ""))
        elif uri.startswith(static_url):
            path = os.path.join(static_root, uri.replace(static_url, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(f"Media file not found: {path}")
        return path



