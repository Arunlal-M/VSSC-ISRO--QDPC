


from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
import os
from django.contrib.contenttypes.models import ContentType
from qdpc_core_models.models.consumable import Consumable,PreCertification
from django.conf import settings
from io import BytesIO
from django.views import View
from qdpc_core_models.models.productBatch import ProductBatchs
from qdpc_core_models.models.process import Process, ProcessStep
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
import json

class ReportView(BaseModelViewSet):
    template_name = 'qar_report_template.html'
    pdf_template_name = 'qar_report_template.html'
    editable_template_name = 'qar_report_editable.html'
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
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Authentication required. Please log in to access this resource.',
                        'error_type': 'authentication_error'
                    }), 
                    content_type='application/json',
                    status=401
                )
                
            # Validate batch_id parameter
            if not batch_id:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Batch ID is required to generate QAR report.',
                        'error_type': 'validation_error'
                    }), 
                    content_type='application/json',
                    status=400
                )

            # Fetch batch with proper error handling
            try:
                batch = ProductBatchs.objects.select_related('product', 'qa_approved_by').get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Batch with ID {batch_id} not found in the system.',
                        'error_type': 'not_found_error'
                    }), 
                    content_type='application/json',
                    status=404
                )
            
            # Validate batch status
            if batch.status not in ['approved', 'active']:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Batch {batch.batch_id} is not approved for QAR report generation. Current status: {batch.status}',
                        'error_type': 'status_error',
                        'batch_status': batch.status
                    }), 
                    content_type='application/json',
                    status=400
                )

            # Get product with validation
            product = batch.product
            if not product:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Product information not found for batch {batch.batch_id}.',
                        'error_type': 'data_error'
                    }), 
                    content_type='application/json',
                    status=404
                )
            # Get process through the ProductBatchProcess relationship
            try:
                process_batch = batch.productbatchprocess_set.first()
                process = process_batch.process if process_batch else None
            except Exception as e:
                print(f"Warning: Error retrieving process for batch {batch.id}: {e}")
                process = None

            raw_materials = []
            # Get raw materials through ProductBatchRawMaterial relationship
            try:
                for rm_batch in batch.productbatchrawmaterial_set.all():
                    rm = rm_batch.raw_material
                    if rm:
                        acceptance_test_data = []
                        try:
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
                        except Exception as test_error:
                            print(f"Warning: Error retrieving acceptance tests for raw material {rm.id}: {test_error}")
                            acceptance_test_data = []

                        raw_materials.append({
                            'material': rm.id,
                            'rawmaterial_name': rm.name,
                            'suppliers': getattr(rm, 'suppliers', None),
                            'sources': getattr(rm, 'sources', None),
                            'grade': getattr(rm, 'grade', None),
                            'acceptance_tests': acceptance_test_data,
                            'precertification': self.get_precertification(rm)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving raw materials for batch {batch.id}: {e}")
                raw_materials = []

            consumables = []
            # Get consumables through ProductBatchConsumable relationship
            try:
                for c_batch in batch.productbatchconsumable_set.all():
                    c = c_batch.consumable
                    if c:
                        consumables.append({
                            'consumable': c.id,
                            'consumable_name': c.name,
                            'suppliers': getattr(c, 'suppliers', None),
                            'sources': getattr(c, 'sources', None),
                            'grade': getattr(c, 'grade', None),
                            'precertification': self.get_precertification(c)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving consumables for batch {batch.id}: {e}")
                consumables = []

            components = []
            # Get components through ProductBatchComponent relationship
            try:
                for comp_batch in batch.productbatchcomponent_set.all():
                    comp = comp_batch.component
                    if comp:
                        components.append({
                            'component': comp.id,
                            'component_name': comp.name,
                            'suppliers': getattr(comp, 'suppliers', None),
                            'sources': getattr(comp, 'sources', None),
                            'grade': getattr(comp, 'grade', None),
                            'precertification': self.get_precertification(comp)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving components for batch {batch.id}: {e}")
                components = []

            process_steps = []
            if process and hasattr(process, 'processstep_set'):
                try:
                    process_steps = process.processstep_set.all()
                except Exception as e:
                    print(f"Warning: Error retrieving process steps for process {process.id if process else 'N/A'}: {e}")
                    process_steps = []
            # Get equipment through ProductBatchEquipment relationship
            equipment_list = []
            try:
                for eq_batch in batch.productbatchequipment_set.all():
                    if eq_batch.equipment:
                        equipment_list.append(eq_batch.equipment)
            except Exception as e:
                print(f"Warning: Error retrieving equipment for batch {batch.id}: {e}")
                equipment_list = []

            # Fetch dynamic tables data
            dynamic_tables = []
            try:
                from product.models import DynamicTable, DynamicTableRow
                tables = DynamicTable.objects.filter(product_batch=batch)
                for table in tables:
                    rows = DynamicTableRow.objects.filter(table=table)
                    table_data = {
                        'title': table.title,
                        'columns': table.columns,
                        'rows': [row.data for row in rows]
                    }
                    dynamic_tables.append(table_data)
            except Exception as e:
                dynamic_tables = []

            context = {
                'batch': batch,
                'product': product,
                'process': process,
                'raw_materials': raw_materials,
                'consumables': consumables,
                'components': components,
                'process_steps': process_steps,
                'equipment_list': equipment_list,
                'dynamic_tables': dynamic_tables,
                'today': timezone.now().date(),
                'batch_id': batch_id,
                'company_logo': 'assets/images/logo.png',
                'generated_date': timezone.now(),
            }
            
            # Log successful data retrieval
            print(f"Success: Context created with {len(raw_materials)} raw materials, {len(consumables)} consumables, {len(components)} components")
            print(f"Success: Process: {process}, Process steps: {len(process_steps) if process_steps else 0}")
            print(f"Success: Equipment: {len(equipment_list)}")

            # Get or create QAR report data for both editable and regular views
            from qdpc_core_models.models.qar_report import QARReport
            qar_report, created = QARReport.objects.get_or_create(
                product_batch=batch,
                defaults={'created_by': request.user}
            )
            context['qar_data'] = qar_report
            
            # Check if user wants editable version
            if request.GET.get('editable') == 'true':
                # Get all users for personnel selection
                from qdpc_core_models.models.user import User
                users = User.objects.filter(is_active=True).order_by('username')
                context['users'] = users
                
                template_to_use = self.editable_template_name
            else:
                template_to_use = self.template_name

            if request.GET.get('format') == 'pdf':
                return self._generate_pdf_response(context)

            try:
                response = render(request, template_to_use, context)
                # Add success headers for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    response['X-Status'] = 'success'
                return response
            except Exception as template_error:
                error_message = f"Error rendering QAR report template: {str(template_error)}"
                print(f"Error: {error_message}")
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': error_message,
                        'error_type': 'template_error'
                    }), 
                    content_type='application/json',
                    status=500
                )

        except Exception as e:
            error_message = f"Unexpected error while generating QAR report: {str(e)}"
            print(f"Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )

    def post(self, request, batch_id=None):
        """Handle POST requests for saving QAR report data"""
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Authentication required. Please log in to access this resource.',
                        'error_type': 'authentication_error'
                    }), 
                    content_type='application/json',
                    status=401
                )
            
            # Validate batch_id parameter
            if not batch_id:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Batch ID is required to save QAR report.',
                        'error_type': 'validation_error'
                    }), 
                    content_type='application/json',
                    status=400
                )

            # Fetch batch
            try:
                batch = ProductBatchs.objects.get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Batch with ID {batch_id} not found in the system.',
                        'error_type': 'not_found_error'
                    }), 
                    content_type='application/json',
                    status=404
                )

            # Get or create QAR report
            from qdpc_core_models.models.qar_report import QARReport
            from report.serializers.qar_report_serializer import QARReportSerializer
            
            qar_report, created = QARReport.objects.get_or_create(
                product_batch=batch,
                defaults={'created_by': request.user}
            )

            # Prepare data for serializer
            data = request.POST.copy()
            data['product_batch'] = batch.id
            
            # Handle date field
            if 'report_date' in data and data['report_date']:
                try:
                    from datetime import datetime
                    data['report_date'] = datetime.strptime(data['report_date'], '%Y-%m-%d').date()
                except ValueError:
                    data['report_date'] = timezone.now().date()

            # Serialize and save
            serializer = QARReportSerializer(qar_report, data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(
                    json.dumps({
                        'success': True,
                        'message': 'QAR Report saved successfully!',
                        'data': serializer.data
                    }), 
                    content_type='application/json',
                    status=200
                )
            else:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Validation error',
                        'errors': serializer.errors
                    }), 
                    content_type='application/json',
                    status=400
                )

        except Exception as e:
            error_message = f"Unexpected error while saving QAR report: {str(e)}"
            print(f"Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )





    def _generate_pdf_response(self, context):
        """Generate PDF from the template and return as response"""
        try:
            print(f"Starting PDF generation with template: {self.pdf_template_name or self.template_name}")
            template = get_template(self.pdf_template_name or self.template_name)
            try:
                html = template.render(context)
                print("Template rendered successfully")
            except Exception as render_error:
                error_message = f"Error rendering PDF template: {str(render_error)}"
                print(f"PDF Error: {error_message}")
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': error_message,
                        'error_type': 'pdf_template_error'
                    }), 
                    content_type='application/json',
                    status=500
                )
            
            print("Starting PDF document generation...")
            result = BytesIO()
            pdf = pisa.pisaDocument(
                BytesIO(html.encode("UTF-8")), 
                result,
                encoding='UTF-8',
                link_callback=self._link_callback
            )
            
            if not pdf.err:
                print("PDF generated successfully")
                response = HttpResponse(
                    result.getvalue(), 
                    content_type='application/pdf'
                )
                filename = f"QAR_Report_{context['batch_id']}_{context['today']}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            
            # PDF generation failed
            error_message = f"PDF generation failed: {pdf.err}"
            print(f"PDF Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'pdf_generation_error'
                }), 
                content_type='application/json',
                status=500
            )
        except Exception as e:
            error_message = f"Unexpected error during PDF generation: {str(e)}"
            print(f"PDF Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'pdf_unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )

    def _link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        try:
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
                print(f"Warning: Media file not found: {path}")
                # Return a default image or empty string instead of raising exception
                return ""
            return path
        except Exception as e:
            print(f"Warning: Error in link callback for URI {uri}: {e}")
            return ""




class QARReportListView(BaseModelViewSet):
    """View for listing all product batches for QAR report generation"""
    template_name = 'qar_report_list.html'
    
    def get(self, request):
        try:
            # Get only approved batches (approved or active status)
            try:
                all_batches = ProductBatchs.objects.filter(
                    status__in=['approved', 'active']
                ).select_related(
                    'product', 'qa_approved_by'
                ).order_by('-created_at')
            except Exception as batch_error:
                error_message = f"Error querying approved batches: {str(batch_error)}"
                print(f"Error: {error_message}")
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': error_message,
                        'error_type': 'database_query_error'
                    }), 
                    content_type='application/json',
                    status=500
                )
            
            # Get approved batches count (same as all_batches since we're only showing approved)
            approved_batches = all_batches
            
            context = {
                'all_batches': all_batches,
                'approved_batches': approved_batches,
                'page_title': 'QAR Report - Approved Product Batches',
                'debug_info': {
                    'approved_count': approved_batches.count()
                }
            }
            

            
            response = render(request, self.template_name, context)
            # Add success headers for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response['X-Status'] = 'success'
            return response
            
        except Exception as e:
            error_message = f"Unexpected error loading QAR report list: {str(e)}"
            print(f"Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )




class ProcessLogSheetListView(BaseModelViewSet):
    """View for listing all product batches for Process Log-Sheet generation"""
    template_name = 'process_log_sheet_list.html'
    
    def get(self, request):
        try:
            # Get only approved batches (approved or active status) - same as QAR report list
            try:
                all_batches = ProductBatchs.objects.filter(
                    status__in=['approved', 'active']
                ).select_related(
                    'product', 'qa_approved_by'
                ).order_by('-created_at')
            except Exception as batch_error:
                error_message = f"Error querying approved batches: {str(batch_error)}"
                print(f"Error: {error_message}")
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': error_message,
                        'error_type': 'database_query_error'
                    }), 
                    content_type='application/json',
                    status=500
                )
            
            # Get approved batches count (same as all_batches since we're only showing approved)
            approved_batches = all_batches
            
            context = {
                'all_batches': all_batches,
                'approved_batches': approved_batches,
                'page_title': 'Process Log-Sheet - Approved Product Batches',
                'debug_info': {
                    'approved_count': approved_batches.count()
                }
            }
            
            response = render(request, self.template_name, context)
            # Add success headers for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response['X-Status'] = 'success'
            return response
            
        except Exception as e:
            error_message = f"Unexpected error loading Process Log-Sheet list: {str(e)}"
            print(f"Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )


class ProcessLogSheetView(BaseModelViewSet):
    """View for generating Process Log-Sheet from a product batch"""
    template_name = 'process_log_sheet_template.html'
    pdf_template_name = 'process_log_sheet_pdf_template.html'

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
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Authentication required. Please log in to access this resource.',
                        'error_type': 'authentication_error'
                    }), 
                    content_type='application/json',
                    status=401
                )
                
            # Validate batch_id parameter
            if not batch_id:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': 'Batch ID is required to generate Process Log-Sheet.',
                        'error_type': 'validation_error'
                    }), 
                    content_type='application/json',
                    status=400
                )

            # Fetch batch with proper error handling
            try:
                batch = ProductBatchs.objects.select_related('product', 'qa_approved_by').get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Batch with ID {batch_id} not found in the system.',
                        'error_type': 'not_found_error'
                    }), 
                    content_type='application/json',
                    status=404
                )
            
            # Validate batch status
            if batch.status not in ['approved', 'active']:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Batch {batch.batch_id} is not approved for Process Log-Sheet generation. Current status: {batch.status}',
                        'error_type': 'status_error',
                        'batch_status': batch.status
                    }), 
                    content_type='application/json',
                    status=400
                )

            # Get product with validation
            product = batch.product
            if not product:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': f'Product information not found for batch {batch.batch_id}.',
                        'error_type': 'data_error'
                    }), 
                    content_type='application/json',
                    status=404
                )
            # Get process through the ProductBatchProcess relationship
            try:
                process_batch = batch.productbatchprocess_set.first()
                process = process_batch.process if process_batch else None
            except Exception as e:
                print(f"Warning: Error retrieving process for batch {batch.id}: {e}")
                process = None

            raw_materials = []
            # Get raw materials through ProductBatchRawMaterial relationship
            try:
                for rm_batch in batch.productbatchrawmaterial_set.all():
                    rm = rm_batch.raw_material
                    if rm:
                        acceptance_test_data = []
                        try:
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
                        except Exception as test_error:
                            print(f"Warning: Error retrieving acceptance tests for raw material {rm.id}: {test_error}")
                            acceptance_test_data = []

                        # Get related data properly
                        suppliers_data = []
                        sources_data = []
                        grade_data = []
                        
                        try:
                            if hasattr(rm, 'suppliers') and rm.suppliers.exists():
                                suppliers_data = [supplier.name for supplier in rm.suppliers.all()]
                        except Exception as e:
                            print(f"Warning: Error getting suppliers for raw material {rm.id}: {e}")
                            
                        try:
                            if hasattr(rm, 'sources') and rm.sources.exists():
                                sources_data = [source.name for source in rm.sources.all()]
                        except Exception as e:
                            print(f"Warning: Error getting sources for raw material {rm.id}: {e}")
                            
                        try:
                            if hasattr(rm, 'grade') and rm.grade.exists():
                                grade_data = [grade.name for grade in rm.grade.all()]
                        except Exception as e:
                            print(f"Warning: Error getting grade for raw material {rm.id}: {e}")
                        
                        raw_materials.append({
                            'material': rm.id,
                            'rawmaterial_name': rm.name,
                            'suppliers': ', '.join(suppliers_data) if suppliers_data else 'N/A',
                            'sources': ', '.join(sources_data) if sources_data else 'N/A',
                            'grade': ', '.join(grade_data) if grade_data else 'N/A',
                            'batch_id': rm_batch.batch.batch_id if rm_batch.batch else None,
                            'date_added': rm_batch.date_added,
                            'status': rm_batch.status,
                            'acceptance_tests': acceptance_test_data,
                            'precertification': self.get_precertification(rm)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving raw materials for batch {batch.id}: {e}")
                raw_materials = []

            consumables = []
            # Get consumables through ProductBatchConsumable relationship
            try:
                for c_batch in batch.productbatchconsumable_set.all():
                    c = c_batch.consumable
                    if c:
                        # Get related data properly for consumables
                        c_suppliers_data = []
                        c_sources_data = []
                        c_grade_data = []
                        
                        try:
                            if hasattr(c, 'suppliers') and c.suppliers.exists():
                                c_suppliers_data = [supplier.name for supplier in c.suppliers.all()]
                        except Exception as e:
                            print(f"Warning: Error getting suppliers for consumable {c.id}: {e}")
                            
                        try:
                            if hasattr(c, 'sources') and c.sources.exists():
                                c_sources_data = [source.name for source in c.sources.all()]
                        except Exception as e:
                            print(f"Warning: Error getting sources for consumable {c.id}: {e}")
                            
                        try:
                            if hasattr(c, 'grade') and c.grade.exists():
                                c_grade_data = [grade.name for grade in c.grade.all()]
                        except Exception as e:
                            print(f"Warning: Error getting grade for consumable {c.id}: {e}")
                        
                        consumables.append({
                            'consumable': c.id,
                            'consumable_name': c.name,
                            'suppliers': ', '.join(c_suppliers_data) if c_suppliers_data else 'N/A',
                            'sources': ', '.join(c_sources_data) if c_sources_data else 'N/A',
                            'grade': ', '.join(c_grade_data) if c_grade_data else 'N/A',
                            'batch_id': c_batch.batch,
                            'date_added': c_batch.date_added,
                            'status': c_batch.status,
                            'precertification': self.get_precertification(c)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving consumables for batch {batch.id}: {e}")
                consumables = []

            components = []
            # Get components through ProductBatchComponent relationship
            try:
                for comp_batch in batch.productbatchcomponent_set.all():
                    comp = comp_batch.component
                    if comp:
                        # Get related data properly for components
                        comp_suppliers_data = []
                        comp_sources_data = []
                        comp_grade_data = []
                        
                        try:
                            if hasattr(comp, 'suppliers') and comp.suppliers.exists():
                                comp_suppliers_data = [supplier.name for supplier in comp.suppliers.all()]
                        except Exception as e:
                            print(f"Warning: Error getting suppliers for component {comp.id}: {e}")
                            
                        try:
                            if hasattr(comp, 'sources') and comp.sources.exists():
                                comp_sources_data = [source.name for source in comp.sources.all()]
                        except Exception as e:
                            print(f"Warning: Error getting sources for component {comp.id}: {e}")
                            
                        try:
                            if hasattr(comp, 'grade') and comp.grade.exists():
                                comp_grade_data = [grade.name for grade in comp.grade.all()]
                        except Exception as e:
                            print(f"Warning: Error getting grade for component {comp.id}: {e}")
                        
                        components.append({
                            'component': comp.id,
                            'component_name': comp.name,
                            'suppliers': ', '.join(comp_suppliers_data) if comp_suppliers_data else 'N/A',
                            'sources': ', '.join(comp_sources_data) if comp_sources_data else 'N/A',
                            'grade': ', '.join(comp_grade_data) if comp_grade_data else 'N/A',
                            'batch_id': comp_batch.batch,
                            'date_added': comp_batch.date_added,
                            'status': comp_batch.status,
                            'precertification': self.get_precertification(comp)
                        })
            except Exception as e:
                print(f"Warning: Error retrieving components for batch {batch.id}: {e}")
                components = []

            process_steps = []
            if process and hasattr(process, 'processstep_set'):
                try:
                    process_steps = process.processstep_set.all()
                except Exception as e:
                    print(f"Warning: Error retrieving process steps for process {process.id if process else 'N/A'}: {e}")
                    process_steps = []
            # Get equipment through ProductBatchEquipment relationship
            equipment_list = []
            try:
                for eq_batch in batch.productbatchequipment_set.all():
                    if eq_batch.equipment:
                        equipment_list.append({
                            'equipment': eq_batch.equipment,
                            'name': eq_batch.equipment.name,
                            'equipment_type': getattr(eq_batch.equipment, 'equipment_type', None),
                            'date_added': eq_batch.date_added
                        })
            except Exception as e:
                print(f"Warning: Error retrieving equipment for batch {batch.id}: {e}")
                equipment_list = []

            # Fetch dynamic tables data
            dynamic_tables = []
            try:
                from product.models import DynamicTable, DynamicTableRow
                tables = DynamicTable.objects.filter(product_batch=batch)
                for table in tables:
                    rows = DynamicTableRow.objects.filter(table=table)
                    table_data = {
                        'title': table.title,
                        'columns': table.columns,
                        'rows': [row.data for row in rows]
                    }
                    dynamic_tables.append(table_data)
            except Exception as e:
                dynamic_tables = []

            context = {
                'batch': batch,
                'product': product,
                'process': process,
                'raw_materials': raw_materials,
                'consumables': consumables,
                'components': components,
                'process_steps': [],  # Temporarily empty to fix the error
                'equipment_list': equipment_list,
                'dynamic_tables': dynamic_tables,
                'today': timezone.now().date(),
                'generated_date': timezone.now(),
                'batch_id': batch_id,
                'company_logo': 'assets/images/logo.png',
            }
            
            # Log successful data retrieval
            print(f"Success: Context created with {len(raw_materials)} raw materials, {len(consumables)} consumables, {len(components)} components")
            print(f"Success: Process: {process}, Process steps: {len(process_steps) if process_steps else 0}")
            print(f"Success: Equipment: {len(equipment_list)}")
            


            if request.GET.get('format') == 'pdf':
                print(f"PDF generation requested for batch {batch_id}")
                try:
                    return self._generate_pdf_response(context)
                except Exception as pdf_error:
                    print(f"PDF generation error: {pdf_error}")
                    return HttpResponse(
                        json.dumps({
                            'success': False,
                            'message': f'PDF generation failed: {str(pdf_error)}',
                            'error_type': 'pdf_generation_error'
                        }), 
                        content_type='application/json',
                        status=500
                    )

            try:
                response = render(request, self.template_name, context)
                # Add success headers for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    response['X-Status'] = 'success'
                return response
            except Exception as template_error:
                error_message = f"Error rendering Process Log-Sheet template: {str(template_error)}"
                print(f"Error: {error_message}")
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': error_message,
                        'error_type': 'template_error'
                    }), 
                    content_type='application/json',
                    status=500
                )

        except Exception as e:
            error_message = f"Unexpected error while generating Process Log-Sheet: {str(e)}"
            print(f"Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )

    def _generate_pdf_response(self, context):
        """
        Generate PDF response for Process Log-Sheet
        """
        try:
            print("Starting PDF generation for Process Log-Sheet...")
            
            # Import required modules
            from django.template.loader import get_template
            from django.conf import settings
            import os
            from xhtml2pdf import pisa
            from io import BytesIO
            
            # Get the PDF template
            template = get_template(self.pdf_template_name)
            html = template.render(context)
            
            print("Template rendered successfully")
            
            # Create PDF
            result = BytesIO()
            pdf = pisa.pisaDocument(
                BytesIO(html.encode("UTF-8")), 
                result,
                encoding='UTF-8',
                link_callback=self._link_callback
            )
            
            if not pdf.err:
                print("PDF generated successfully")
                response = HttpResponse(
                    result.getvalue(), 
                    content_type='application/pdf'
                )
                filename = f"Process_Log_Sheet_{context['batch_id']}_{context['today']}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            
            # PDF generation failed
            error_message = f"PDF generation failed: {pdf.err}"
            print(f"PDF Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'pdf_generation_error'
                }), 
                content_type='application/json',
                status=500
            )
        except Exception as e:
            error_message = f"Unexpected error during PDF generation: {str(e)}"
            print(f"PDF Error: {error_message}")
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': error_message,
                    'error_type': 'pdf_unexpected_error'
                }), 
                content_type='application/json',
                status=500
            )

    def _link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
        """
        try:
            from django.conf import settings
            import os
            
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
                print(f"Warning: Media file not found: {path}")
                # Return a default image or empty string instead of raising exception
                return ""
            return path
        except Exception as e:
            print(f"Warning: Error in link callback for URI {uri}: {e}")
            return ""



