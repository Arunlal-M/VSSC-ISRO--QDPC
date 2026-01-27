from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.unit import Unit
from qdpc.core.decorators import require_page_permission
from qdpc.services.notification_service import NotificationService
import json

@login_required
def acceptance_test_list(request):
    """List all acceptance tests"""
    
    acceptance_tests = AcceptanceTest.objects.all().order_by('-id')
    
    context = {
        'page_title': 'Acceptance Tests',
        'breadcrumb': [
            {'name': 'Home', 'url': 'user-dashboard'},
            {'name': 'Acceptance Tests', 'url': 'acceptance-test-list'}
        ],
        'acceptance_tests': acceptance_tests
    }
    
    return render(request, 'acceptance_test/list.html', context)

@login_required
def acceptance_test_create(request):
    """Create a new acceptance test"""
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            test_type = request.POST.get('test_type')
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            unit_id = request.POST.get('unit')
            reevaluation_frequency_value = request.POST.get('reevaluation_frequency_value')
            reevaluation_frequency_unit = request.POST.get('reevaluation_frequency_unit')
            test_result = request.POST.get('test_result')
            specification_result = request.POST.get('specification_result')
            
            # Validate required fields
            if not name or not test_type or not reevaluation_frequency_value or not reevaluation_frequency_unit:
                messages.error(request, 'Required fields are missing')
                raise ValueError('Required fields are missing')
            
            # Validate numeric values
            try:
                if min_value:
                    min_value = int(min_value)
                if max_value:
                    max_value = int(max_value)
                reevaluation_frequency_value = int(reevaluation_frequency_value)
            except ValueError:
                messages.error(request, 'Invalid numeric values')
                raise ValueError('Invalid numeric values')
            
            # Validate quantitative test requirements
            if test_type == 'quantitative':
                if not min_value or not max_value or not unit_id:
                    messages.error(request, 'Quantitative tests require min value, max value, and unit')
                    raise ValueError('Quantitative tests require min value, max value, and unit')
                if min_value >= max_value:
                    messages.error(request, 'Min value must be less than max value')
                    raise ValueError('Min value must be less than max value')
            
            # Clean up empty strings to None for optional fields
            min_value = min_value if min_value and min_value.strip() else None
            max_value = max_value if max_value and max_value.strip() else None
            unit_id = unit_id if unit_id and unit_id.strip() else None
            test_result = test_result if test_result and test_result.strip() else None
            specification_result = specification_result if specification_result and specification_result.strip() else None
            
            # Validate field lengths
            if test_result and len(test_result) > 100:
                messages.error(request, 'Test result must be 100 characters or less')
                raise ValueError('Test result must be 100 characters or less')
            
            if specification_result and len(specification_result) > 100:
                messages.error(request, 'Specification result must be 100 characters or less')
                raise ValueError('Specification result must be 100 characters or less')
            
            # Create acceptance test
            acceptance_test = AcceptanceTest.objects.create(
                name=name,
                test_type=test_type,
                min_value=min_value,
                max_value=max_value,
                unit_id=unit_id if unit_id else None,
                reevaluation_frequency_value=reevaluation_frequency_value,
                reevaluation_frequency_unit=reevaluation_frequency_unit,
                test_result=test_result,
                specification_result=specification_result
            )
            
            # Create notification
            NotificationService.create_entity_notification(
                entity_type='acceptance_test',
                entity_id=acceptance_test.id,
                entity_name=acceptance_test.name,
                notification_type='create',
                created_by=request.user
            )
            
            messages.success(request, f'Acceptance test "{name}" created successfully!')
            return redirect('acceptance-test-list')
            
        except Exception as e:
            messages.error(request, f'Error creating acceptance test: {str(e)}')
    
    # Get units for dropdown
    units = Unit.objects.all().order_by('name')
    
    context = {
        'page_title': 'Create Acceptance Test',
        'breadcrumb': [
            {'name': 'Home', 'url': 'user-dashboard'},
            {'name': 'Acceptance Tests', 'url': 'acceptance-test-list'},
            {'name': 'Create', 'url': 'acceptance-test-create'}
        ],
        'units': units
    }
    
    return render(request, 'acceptance_test/create.html', context)

@login_required
def acceptance_test_create_enhanced(request):
    """Create a new acceptance test with enhanced functionality and AJAX support"""
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            test_type = request.POST.get('test_type')
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            unit_id = request.POST.get('unit')
            reevaluation_frequency_value = request.POST.get('reevaluation_frequency_value')
            reevaluation_frequency_unit = request.POST.get('reevaluation_frequency_unit')
            test_result = request.POST.get('test_result')
            specification_result = request.POST.get('specification_result')
            
            # Validate required fields
            if not name or not test_type or not reevaluation_frequency_value or not reevaluation_frequency_unit:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Required fields are missing'
                    }, status=400)
                else:
                    messages.error(request, 'Required fields are missing')
                    raise ValueError('Required fields are missing')
            
            # Validate numeric values
            try:
                if min_value:
                    min_value = int(min_value)
                if max_value:
                    max_value = int(max_value)
                reevaluation_frequency_value = int(reevaluation_frequency_value)
            except ValueError:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid numeric values'
                    }, status=400)
                else:
                    messages.error(request, 'Invalid numeric values')
                    raise ValueError('Invalid numeric values')
            
            # Validate quantitative test requirements
            if test_type == 'quantitative':
                if not min_value or not max_value or not unit_id:
                    error_msg = 'Quantitative tests require min value, max value, and unit'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': error_msg
                        }, status=400)
                    else:
                        messages.error(request, error_msg)
                        raise ValueError(error_msg)
                
                if min_value >= max_value:
                    error_msg = 'Min value must be less than max value'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': error_msg
                        }, status=400)
                    else:
                        messages.error(request, error_msg)
                        raise ValueError(error_msg)
            
            # Validate field lengths for qualitative tests
            if test_type == 'qualitative':
                if test_result and len(test_result) > 100:
                    error_msg = 'Test result must be 100 characters or less'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': error_msg
                        }, status=400)
                    else:
                        messages.error(request, error_msg)
                        raise ValueError(error_msg)
                
                if specification_result and len(specification_result) > 100:
                    error_msg = 'Specification result must be 100 characters or less'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': error_msg
                        }, status=400)
                    else:
                        messages.error(request, error_msg)
                        raise ValueError(error_msg)
            
            # Create acceptance test
            acceptance_test = AcceptanceTest.objects.create(
                name=name,
                test_type=test_type,
                min_value=min_value,
                max_value=max_value,
                unit_id=unit_id if unit_id else None,
                reevaluation_frequency_value=reevaluation_frequency_value,
                reevaluation_frequency_unit=reevaluation_frequency_unit,
                test_result=test_result,
                specification_result=specification_result
            )
            
            # Create notification
            NotificationService.create_entity_notification(
                entity_type='acceptance_test',
                entity_id=acceptance_test.id,
                entity_name=acceptance_test.name,
                notification_type='create',
                created_by=request.user
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Acceptance test created successfully!',
                    'data': {
                        'id': acceptance_test.id,
                        'name': acceptance_test.name
                    }
                })
            else:
                messages.success(request, f'Acceptance test "{name}" created successfully!')
                return redirect('acceptance-test-list')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Error creating acceptance test: {str(e)}'
                }, status=500)
            else:
                messages.error(request, f'Error creating acceptance test: {str(e)}')
    
    # Get units for dropdown
    units = Unit.objects.all().order_by('name')
    
    context = {
        'page_title': 'Create Acceptance Test',
        'breadcrumb': [
            {'name': 'Home', 'url': 'user-dashboard'},
            {'name': 'Acceptance Tests', 'url': 'acceptance-test-list'},
            {'name': 'Create', 'url': 'acceptance-test-create'}
        ],
        'units': units
    }
    
    return render(request, 'acceptance_test_add.html', context)

@login_required
def acceptance_test_edit(request, test_id):
    """Edit an existing acceptance test"""
    
    acceptance_test = get_object_or_404(AcceptanceTest, id=test_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            test_type = request.POST.get('test_type')
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            unit_id = request.POST.get('unit')
            reevaluation_frequency_value = request.POST.get('reevaluation_frequency_value')
            reevaluation_frequency_unit = request.POST.get('reevaluation_frequency_unit')
            test_result = request.POST.get('test_result')
            specification_result = request.POST.get('specification_result')
            
            # Clean up empty strings to None for optional fields
            min_value = min_value if min_value and min_value.strip() else None
            max_value = max_value if max_value and max_value.strip() else None
            unit_id = unit_id if unit_id and unit_id.strip() else None
            test_result = test_result if test_result and test_result.strip() else None
            specification_result = specification_result if specification_result and specification_result.strip() else None
            
            # Validate required fields
            if not name or not test_type or not reevaluation_frequency_value or not reevaluation_frequency_unit:
                messages.error(request, 'Required fields are missing')
                raise ValueError('Required fields are missing')
            
            # Validate numeric values
            try:
                if min_value:
                    min_value = int(min_value)
                if max_value:
                    max_value = int(max_value)
                reevaluation_frequency_value = int(reevaluation_frequency_value)
            except ValueError:
                messages.error(request, 'Invalid numeric values')
                raise ValueError('Invalid numeric values')
            
            # Validate quantitative test requirements
            if test_type == 'quantitative':
                if not min_value or not max_value or not unit_id:
                    messages.error(request, 'Quantitative tests require min value, max value, and unit')
                    raise ValueError('Quantitative tests require min value, max value, and unit')
                if min_value >= max_value:
                    messages.error(request, 'Min value must be less than max value')
                    raise ValueError('Min value must be less than max value')
            
            # Validate field lengths for qualitative tests
            if test_type == 'qualitative':
                if test_result and len(test_result) > 100:
                    messages.error(request, 'Test result must be 100 characters or less')
                    raise ValueError('Test result must be 100 characters or less')
                
                if specification_result and len(specification_result) > 100:
                    messages.error(request, 'Specification result must be 100 characters or less')
                    raise ValueError('Specification result must be 100 characters or less')
            
            # Update acceptance test
            acceptance_test.name = name
            acceptance_test.test_type = test_type
            acceptance_test.min_value = min_value
            acceptance_test.max_value = max_value
            acceptance_test.unit_id = unit_id if unit_id else None
            acceptance_test.reevaluation_frequency_value = reevaluation_frequency_value
            acceptance_test.reevaluation_frequency_unit = reevaluation_frequency_unit
            acceptance_test.test_result = test_result
            acceptance_test.specification_result = specification_result
            
            acceptance_test.save()
            
            # Create notification
            NotificationService.create_entity_notification(
                entity_type='acceptance_test',
                entity_id=acceptance_test.id,
                entity_name=acceptance_test.name,
                notification_type='update',
                created_by=request.user
            )
            
            messages.success(request, f'Acceptance test "{acceptance_test.name}" updated successfully!')
            return redirect('acceptance-test-list')
            
        except Exception as e:
            messages.error(request, f'Error updating acceptance test: {str(e)}')
    
    # Get units for dropdown
    units = Unit.objects.all().order_by('name')
    
    context = {
        'page_title': 'Edit Acceptance Test',
        'breadcrumb': [
            {'name': 'Home', 'url': 'user-dashboard'},
            {'name': 'Acceptance Tests', 'url': 'acceptance-test-list'},
            {'name': 'Edit', 'url': 'acceptance-test-edit'}
        ],
        'acceptance_test': acceptance_test,
        'units': units
    }
    
    return render(request, 'acceptance_test/edit.html', context)

@login_required
def acceptance_test_view(request, test_id):
    """View acceptance test details"""
    
    acceptance_test = get_object_or_404(AcceptanceTest, id=test_id)
    
    context = {
        'page_title': 'View Acceptance Test',
        'breadcrumb': [
            {'name': 'Home', 'url': 'user-dashboard'},
            {'name': 'Acceptance Tests', 'url': 'acceptance-test-list'},
            {'name': 'View', 'url': 'acceptance-test-view'}
        ],
        'acceptance_test': acceptance_test
    }
    
    return render(request, 'acceptance_test/view.html', context)

@login_required
def acceptance_test_delete(request, test_id):
    """Delete an acceptance test"""
    
    if request.method == 'POST':
        acceptance_test = get_object_or_404(AcceptanceTest, id=test_id)
        name = acceptance_test.name
        
        try:
            # Create notification before deletion
            NotificationService.create_entity_notification(
                entity_type='acceptance_test',
                entity_id=acceptance_test.id,
                entity_name=acceptance_test.name,
                notification_type='delete',
                created_by=request.user
            )
            
            acceptance_test.delete()
            messages.success(request, f'Acceptance test "{name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting acceptance test: {str(e)}')
    
    return redirect('acceptance-test-list')

@login_required
@csrf_exempt
def acceptance_test_ajax(request):
    """Handle AJAX requests for acceptance tests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'delete':
                test_id = data.get('test_id')
                acceptance_test = get_object_or_404(AcceptanceTest, id=test_id)
                
                # Create notification before deletion
                NotificationService.create_entity_notification(
                    entity_type='acceptance_test',
                    entity_id=acceptance_test.id,
                    entity_name=acceptance_test.name,
                    notification_type='delete',
                    created_by=request.user
                )
                
                acceptance_test.delete()
                return JsonResponse({'status': 'success', 'message': 'Test deleted successfully'})
            
            elif action == 'get_test':
                test_id = data.get('test_id')
                acceptance_test = get_object_or_404(AcceptanceTest, id=test_id)
                return JsonResponse({
                    'status': 'success',
                    'test': {
                        'id': acceptance_test.id,
                        'name': acceptance_test.name,
                        'test_type': acceptance_test.test_type,
                        'min_value': acceptance_test.min_value,
                        'max_value': acceptance_test.max_value,
                        'unit_name': acceptance_test.unit.name if acceptance_test.unit else None,
                        'reevaluation_frequency_value': acceptance_test.reevaluation_frequency_value,
                        'reevaluation_frequency_unit': acceptance_test.reevaluation_frequency_unit,
                        'test_result': acceptance_test.test_result,
                        'specification_result': acceptance_test.specification_result
                    }
                })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
