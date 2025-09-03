# Dynamic Permission System Guide

## Overview

The VSSC application now features a fully dynamic permission system where UI elements (buttons, menu items, forms) automatically appear or disappear based on checkbox permissions set in the admin dashboard. This eliminates the need for hardcoded role-based access and provides granular control over user interface visibility.

## How It Works

### 1. Permission Dashboard Control
- **Location**: `/page-permissions/group/1/`
- **Function**: Checkboxes control all user permissions
- **Real-time Effect**: Changes immediately affect UI visibility for users

### 2. Dynamic UI Elements
The following UI elements are controlled by permissions:

#### Sidebar Menu Items
- Equipment, Product Batch, Acceptance Test, etc.
- **Controlled by**: `view` permission for each page
- **Example**: Unchecking "Product batch - View" hides the menu item

#### Action Buttons
- **Add buttons**: Controlled by `add` permission
- **Edit buttons**: Controlled by `edit` permission  
- **Delete buttons**: Controlled by `delete` permission
- **Approve buttons**: Controlled by `approve` permission

#### Form Elements
- Input fields, dropdowns, and form sections
- **Controlled by**: Relevant action permissions

## Permission Structure

### Page Names (as stored in database)
```
- Dashboard
- Equipment
- Acceptance test
- Raw material
- Raw material batch
- Consumable
- Consumable batch
- Component
- Component batch
- Product
- Product batch
- Process
- Units, Grade, Enduse, Document type
- Center, Division, Source, Supplier
- User management
- Reports, Stage clearance, QAR report
- Role management
- Permission management
```

### Action Types
```
- view: Access to page/list view
- add: Create new records
- edit: Modify existing records
- delete: Remove records
- approve: Approval workflows
- reject: Rejection workflows
```

## Implementation Details

### 1. Context Processor (`qdpc/core/context_processors.py`)
Provides permission flags to all templates:

```python
def user_permissions(request):
    permissions = {
        'can_access_product_batch': has_page_permission(request.user, 'Product batch', 'view'),
        'can_add_product_batch': has_page_permission(request.user, 'Product batch', 'add'),
        'can_edit_product_batch': has_page_permission(request.user, 'Product batch', 'edit'),
        'can_delete_product_batch': has_page_permission(request.user, 'Product batch', 'delete'),
        'can_approve_product_batch': has_page_permission(request.user, 'Product batch', 'approve'),
        # ... more permissions
    }
    return permissions
```

### 2. Template Usage
Templates use permission flags to control visibility:

```html
<!-- Add button - only show if user has add permission -->
{% if user.is_superuser or can_add_product_batch %}
    <a href="{% url 'product-batch-add' %}" class="btn btn-primary">
        <i class="fas fa-plus"></i> Add New Batch
    </a>
{% endif %}

<!-- Edit button - only show if user has edit permission -->
{% if user.is_superuser or can_edit_product_batch %}
    <a href="{% url 'product-batch-edit' batch.id %}" class="btn btn-warning">
        <i class="fas fa-edit"></i>
    </a>
{% endif %}
```

### 3. Sidebar Menu (`templates/sidebar.html`)
Menu sections are conditionally displayed:

```html
{% if can_access_equipment or can_access_raw_material or can_access_product_batch %}
<li class="submenu-open">
    <h6 class="submenu-hdr">Product Data Management</h6>
    <ul>
        {% if can_access_equipment %}
        <li><a href="{% url 'equipment-list' %}">Equipments</a></li>
        {% endif %}
        
        {% if can_access_product_batch %}
        <li><a href="{% url 'product-batch-list' %}">Product Batch</a></li>
        {% endif %}
    </ul>
</li>
{% endif %}
```

## Admin Role Handling

### Superuser Access
- **Superusers**: Full access to everything (bypass all permission checks)
- **System Administrators**: Full access based on role names:
  - 'System Administrator'
  - 'Super Admin' 
  - 'Master Admin/Super Admin'
  - 'Roles- System administrator'
  - 'System Administrator-1', 'System Administrator-2', 'System Administrator-3'

### Regular Users
- **Permission Source**: Only PagePermission model checkboxes
- **No Static Roles**: All hardcoded role mappings removed
- **Dynamic Control**: UI changes instantly when permissions are toggled

## Testing the System

### Manual Testing Steps
1. **Login as Admin**
   - Go to `/page-permissions/group/1/`
   - Toggle various permission checkboxes
   - Save changes

2. **Login as Regular User**
   - Navigate to different pages
   - Verify buttons/menu items appear/disappear
   - Test functionality matches permissions

3. **Specific Test Cases**
   - Uncheck "Product batch - Add" → "Add New Batch" button disappears
   - Uncheck "Product batch - Edit" → Edit buttons disappear from list
   - Uncheck "Product batch - View" → Menu item disappears
   - Uncheck "Equipment - Delete" → Delete buttons disappear

### Automated Testing
Run the test script:
```bash
python test_dynamic_permissions.py
```

## Updated Templates

The following templates now have dynamic permission controls:

### Product Management
- `templates/product_batchlist.html` - Add, Edit, Delete, Approve buttons
- `templates/productbatch_add.html` - Form access control
- `templates/product_batch_edit.html` - Edit form access

### Acceptance Tests  
- `templates/acceptance_test/list.html` - Add, Edit, Delete buttons
- `templates/acceptance_test/create.html` - Form access control

### Equipment
- `templates/equipment-list.html` - Add, Edit, Delete buttons
- `templates/equipment-add.html` - Form access control

### Navigation
- `templates/sidebar.html` - Menu item visibility
- `templates/index.html` - Base template with user context

## Permission Flow

```
User Request → Template Loads → Context Processor Runs → 
Permission Flags Generated → UI Elements Show/Hide → 
User Sees Customized Interface
```

## Key Benefits

1. **Single Source of Truth**: Permission dashboard controls everything
2. **Real-time Changes**: No server restart needed
3. **Granular Control**: Individual action-level permissions
4. **User-friendly**: Checkbox interface for admins
5. **Secure**: Backend decorators still enforce access control
6. **Maintainable**: No hardcoded role mappings

## Troubleshooting

### Common Issues

1. **Buttons Still Visible After Unchecking Permission**
   - Clear browser cache
   - Check if user is superuser (bypasses all checks)
   - Verify permission was saved in database

2. **Menu Items Not Disappearing**
   - Check sidebar.html template has permission checks
   - Verify context processor is registered in settings
   - Check permission flag naming consistency

3. **Permission Not Working**
   - Verify page name matches exactly in database
   - Check action name spelling (view, add, edit, delete, approve)
   - Ensure user is in correct group

### Debug Steps
1. Check user groups: `user.groups.all()`
2. Check permissions: `PagePermission.objects.filter(group__in=user.groups.all())`
3. Test permission function: `has_page_permission(user, 'Product batch', 'view')`
4. Verify context processor output in template: `{{ can_access_product_batch }}`

## Migration Notes

### What Changed
- Removed all static role-based dictionaries
- Updated all templates with permission checks  
- Enhanced context processor with comprehensive flags
- Added dynamic UI controls throughout application

### What Stayed the Same
- Backend view decorators (security layer)
- Database models and relationships
- User authentication system
- Basic application functionality

## Future Enhancements

1. **Permission Inheritance**: Child permissions inherit from parent
2. **Time-based Permissions**: Temporary access controls
3. **IP-based Restrictions**: Location-based permissions
4. **Audit Logging**: Track permission changes
5. **Bulk Permission Management**: Apply to multiple groups at once

---

**Last Updated**: August 30, 2025  
**Version**: 2.0  
**Status**: Production Ready
