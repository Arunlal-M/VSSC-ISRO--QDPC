# Role-Based Permission System

## Overview
This system manages user access to different pages based on their role/group membership. Instead of using Django's built-in permissions, it uses a custom role-based approach that maps specific roles to allowed pages.

## How It Works

### 1. Role Definition
Roles are defined in the `ROLE_PAGE_ACCESS` dictionary in `qdpc/core/permissions.py`:

```python
ROLE_PAGE_ACCESS = {
    'Division Head SDA': [
        'dashboard',           # 1. Dashboard
        'rawmaterial',         # 5. Rawmaterial
        'consumable',          # 7. Consumable
        'component',           # 9. Component
        'product',             # 12. Product
        'reports',             # 22. Process Log-Sheet
    ],
    'Engineer Project': [
        'dashboard',
        'equipment',
        'rawmaterial',
        'consumable',
        'component',
        'process',
        'product',
        'reports',
        'stage_clearance',
    ],
    'QA': [
        'dashboard',
        'equipment',
        'rawmaterial',
        'consumable',
        'component',
        'process',
        'product',
        'acceptance_test',
        'reports',
        'stage_clearance',
    ],
    'Super Admin': [
        'ALL'  # Access to everything
    ]
}
```

### 2. Page Mapping
Pages are mapped using the `PAGE_CODES` constant:

```python
PAGE_CODES = {
    'DASHBOARD': 'dashboard',           # 1
    'EQUIPMENT': 'equipment',           # 2
    'ACCEPTANCE_TEST': 'acceptance_test', # 3
    'RAW_MATERIAL': 'rawmaterial',      # 4, 5
    'CONSUMABLE': 'consumable',         # 6, 7
    'COMPONENT': 'component',           # 8, 9
    'PROCESS': 'process',               # 10
    'PRODUCT': 'product',               # 11, 12
    'REPORTS': 'reports',               # 22, 23, 24
    # ... other pages
}
```

### 3. Permission Checking
The system provides several functions to check permissions:

- `get_role_based_page_access(user)`: Returns list of pages user can access
- `has_role_based_page_access(user, page_code)`: Checks if user can access specific page
- `get_user_accessible_pages_by_role(user)`: Returns human-readable page names

### 4. Context Processor Integration
The `user_permissions` context processor automatically provides permission variables to all templates:

```django
{% if can_access_dashboard %}
    <!-- Dashboard content -->
{% endif %}

{% if can_access_raw_material %}
    <!-- Raw material content -->
{% endif %}
```

## Division Head SDA Role

### Allowed Pages (Based on Document)
1. **Dashboard** - `can_access_dashboard`
5. **Rawmaterial** - `can_access_raw_material`
7. **Consumable** - `can_access_consumable`
9. **Component** - `can_access_component`
12. **Product** - `can_access_product`
22. **Process Log-Sheet** - `can_access_reports`

### Implementation
```python
'Division Head SDA': [
    'dashboard',           # 1. Dashboard
    'rawmaterial',         # 5. Rawmaterial
    'consumable',          # 7. Consumable
    'component',           # 9. Component
    'product',             # 12. Product
    'reports',             # 22. Process Log-Sheet
],
```

## Usage Examples

### In Views
```python
from qdpc.core.permissions import has_role_based_page_access

@login_required
def some_view(request):
    if not has_role_based_page_access(request.user, 'rawmaterial'):
        return HttpResponseForbidden("Access denied")
    # ... view logic
```

### In Templates
```django
{% if can_access_raw_material %}
    <a href="{% url 'raw-material' %}">Raw Material</a>
{% endif %}

{% if can_access_reports %}
    <a href="{% url 'process-log-sheet' %}">Process Log-Sheet</a>
{% endif %}
```

### In Sidebar
The sidebar automatically shows/hides menu items based on user permissions:

```django
{% if can_access_raw_material %}
<li>
    <a href="{% url 'raw-material' %}">
        <i data-feather="grid"></i><span>Rawmaterial</span>
    </a>
</li>
{% endif %}
```

## Adding New Roles

1. **Define the role** in `ROLE_PAGE_ACCESS`:
```python
'New Role Name': [
    'dashboard',
    'equipment',
    # ... other allowed pages
],
```

2. **Add new page codes** to `PAGE_CODES` if needed:
```python
'NEW_PAGE': 'new_page',
```

3. **Add permission checks** to context processor:
```python
'can_access_new_page': has_role_based_page_access(request.user, 'new_page'),
```

## Debug and Testing

Visit `/debug/role/` to see:
- Current user role and groups
- Allowed pages for current role
- Page access testing results
- Available roles in the system

## Benefits

1. **Simple Management**: Easy to add/remove roles and pages
2. **Template Integration**: Automatic permission checking in templates
3. **Flexible**: Can easily modify role permissions without code changes
4. **Debug Friendly**: Clear visibility into what each role can access
5. **Performance**: No database queries for permission checking

## Security Notes

- Superusers always have access to everything
- Users without matching roles get only dashboard access
- Role names must exactly match Django group names
- All permission checks happen server-side
