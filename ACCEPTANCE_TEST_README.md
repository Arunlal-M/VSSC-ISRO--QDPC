# Acceptance Test System

This document describes the enhanced acceptance test system that has been integrated into the existing Django project.

## Overview

The acceptance test system allows users to create, manage, and track acceptance tests for various products, components, and materials. It supports both quantitative and qualitative test types with comprehensive validation and user-friendly interfaces.

## Features

### Core Functionality
- **Test Creation**: Create new acceptance tests with detailed specifications
- **Test Types**: Support for both quantitative and qualitative tests
- **Dynamic Fields**: Fields change based on test type selection
- **Validation**: Comprehensive client-side and server-side validation
- **AJAX Support**: Modern AJAX-based form submission
- **Responsive Design**: Mobile-friendly interface

### Test Types

#### Quantitative Tests
- Min/Max value ranges
- Unit selection
- Numeric validation
- Range validation (min < max)

#### Qualitative Tests
- Test result specification
- Specification result input
- Text-based validation

### Common Fields
- Test name (required)
- Reevaluation frequency value (required)
- Time period selection (required)
- Test type selection (required)

## Access Points

### Main Navigation
- **Sidebar**: `Acceptance Test` link in the main navigation
- **List View**: Access from the acceptance test list page

### URLs
- **List View**: `/acceptance-tests/`
- **Standard Create**: `/acceptance-tests/create/`
- **Enhanced Create**: `/acceptance-tests/add/`
- **Edit**: `/acceptance-tests/<id>/edit/`
- **View**: `/acceptance-tests/<id>/view/`
- **Delete**: `/acceptance-tests/<id>/delete/`

## Usage

### Creating a New Acceptance Test

1. **Navigate** to the acceptance test list page
2. **Click** either "Add New Test" (standard) or "Enhanced Add" (new interface)
3. **Fill** in the required fields:
   - Test name
   - Test type (quantitative/qualitative)
   - Reevaluation frequency
   - Time period
4. **Configure** type-specific fields:
   - For quantitative: min/max values and unit
   - For qualitative: test result and specification result
5. **Submit** the form

### Form Validation

The system provides real-time validation:
- Required field highlighting
- Numeric value validation
- Range validation for quantitative tests
- Clear error messages
- Success/error notifications

### AJAX Features

- **Real-time submission** without page reload
- **Loading states** during submission
- **Success/error handling** with user-friendly messages
- **Automatic redirect** on successful submission

## Technical Implementation

### Backend
- **Django Views**: Enhanced views with AJAX support
- **Models**: Integration with existing `AcceptanceTest` model
- **Validation**: Server-side validation with proper error handling
- **Permissions**: Role-based access control

### Frontend
- **Bootstrap**: Responsive design framework
- **jQuery**: AJAX functionality and DOM manipulation
- **Custom CSS**: Enhanced styling and user experience
- **JavaScript**: Form validation and submission logic

### Database
- **Model**: `qdpc_core_models.models.acceptance_test.AcceptanceTest`
- **Fields**: All standard acceptance test fields
- **Relationships**: Unit foreign key relationship
- **Validation**: Model-level validation

## Integration

### Existing System
- **Permissions**: Uses existing role-based permission system
- **Navigation**: Integrated with main sidebar navigation
- **Models**: Extends existing acceptance test infrastructure
- **URLs**: Follows existing URL patterns

### New Features
- **Enhanced UI**: Modern, responsive interface
- **AJAX Support**: Improved user experience
- **Better Validation**: Comprehensive client-side validation
- **Error Handling**: User-friendly error messages

## File Structure

```
templates/
├── acceptance_test_add.html          # New enhanced template
├── acceptance_test/
│   ├── list.html                    # List view
│   ├── create.html                  # Standard create view
│   ├── edit.html                    # Edit view
│   └── view.html                    # Detail view

qdpc/views/
└── acceptance_test.py               # Enhanced views

product/views/
└── raw_matrial_accepatance.py      # Product-specific views
```

## Dependencies

- Django 5.0+
- Bootstrap 5+
- jQuery 3+
- Font Awesome icons
- Existing permission system

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure user has acceptance test access
2. **Validation Errors**: Check required fields and data types
3. **AJAX Failures**: Verify CSRF token and network connectivity
4. **Template Errors**: Ensure all required context variables are passed

### Debug Mode

Enable Django debug mode to see detailed error messages and tracebacks.

## Future Enhancements

- **Bulk Operations**: Import/export multiple tests
- **Advanced Validation**: Custom validation rules
- **Test Templates**: Predefined test configurations
- **Reporting**: Test result analytics and reporting
- **API Endpoints**: REST API for external integrations

## Support

For technical support or feature requests, please contact the development team or create an issue in the project repository.
