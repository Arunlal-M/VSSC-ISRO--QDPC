# VSSC Role-Based Permission System Setup

This document explains how to set up and use the default authentication group permissions for different user roles in the VSSC application, as per the official VSSC requirements.

## Overview

The system provides role-based access control with specific page permissions for different user groups. Each role has predefined permissions for specific pages as defined in the VSSC role permissions table.

## Page Structure (1-25)

### Product Data Management
- **Page 1**: Dashboard
- **Page 2**: Equipments
- **Page 3**: Acceptance Test
- **Page 4**: Rawmaterial
- **Page 5**: Rawmaterial Batch
- **Page 6**: Consumable
- **Page 7**: Consumable Batch
- **Page 8**: Component
- **Page 9**: Component Batch
- **Page 10**: Process
- **Page 11**: Product
- **Page 12**: Product batch

### Miscellaneous Data Management
- **Page 13**: Units
- **Page 14**: Grade
- **Page 15**: Enduse
- **Page 16**: Document Type
- **Page 17**: Center
- **Page 18**: Division
- **Page 19**: Source
- **Page 20**: Supplier

### User Management
- **Page 21**: Users

### Report Generation
- **Page 22**: Process Log-Sheet
- **Page 23**: Stage Clearance
- **Page 24**: Q.A.R-Report

### Roles Management
- **Page 25**: Groups

## User Roles and Permissions

### Guest Roles (Dashboard Access Only)
- **Guest**: Page 1 (Dashboard) - Read-only access
- **Roles- In house process**: Page 1 (Dashboard) - Read-only access
- **DPD Project**: Page 1 (Dashboard) - Read-only access
- **Engineer Project**: Page 1 (Dashboard) - Read-only access

### SDA Roles (Full Access to Pages 1,5,7,9,12,22)
- **Division Head SDA**: Can add new batches, approve/reject submissions, send for QA review after approval
- **Section Head SDA**: Can add new batches, approve/reject submissions, submit to Division Head SDA
- **Engineer SDA**: Can add new batches, submit to Section head SDA
- **Technical/Scientific staff SDA**: Can add new batches, submit to Section head SDA
- **Operator/Technicians SDA**: Can add new batches, submit to Section head SDA

### QA Roles (Access to Pages 1,12,23,24)
- **Division Head QA**: Approve/reject the Section head QA/Engineer QA submissions
- **Section Head QA**: Submit to Division head QA/ Reject Engineer QA/Technical/Scientific staff QA submissions
- **Engineer QA**: Submit to Section head QA
- **Technical/Scientific staff QA**: Submit to Section head QA

### QC Roles (Access to Pages 1,12)
- **Division Head QC**: Approve/reject the Section head QC/Engineer QC submissions
- **Section Head QC**: Submit to Division head QC/ Reject Engineer QC/Technical/Scientific staff QC submissions
- **Engineer QC**: Submit to Section head QC
- **Technical/Scientific staff QC**: Submit to Section head QC

### Testing Agency Roles (Access to Pages 1,5,7,9,12)
- **Division Head Testing agency**: Approve/reject the Section head Testing agency/Engineer Testing agency submissions
- **Section Head Testing agency**: Submit to Division head Testing agency/ Reject Engineer Testing agency/Technical/Scientific staff Testing agency submissions
- **Engineer Testing agency**: Submit to Section head Testing agency
- **Technical/Scientific staff Testing agency**: Submit to Section head Testing agency

### LSC Roles (Guest Access - Will be added in next updates)
- **Member secretary, LSC**: Page 1 (Dashboard) - Read-only access
- **Chairman, LSC**: Page 1 (Dashboard) - Read-only access

### NCRB Roles (Guest Access - Will be added in next updates)
- **Member secretary, NCRB**: Page 1 (Dashboard) - Read-only access
- **Chairman, NCRB**: Page 1 (Dashboard) - Read-only access

### Industry Process Roles (Access to Pages 1,5,7,9,12)
- **Roles- Industry process**: Full access to industry processes
- **Operator/Technician industry**: Basic access to industry processes
- **Process Manager industry**: Full access to industry processes
- **QC Manager industry**: Full access to QC industry processes
- **QA Manager industry**: Full access to QA industry processes

### GOCO Roles (Access to Pages 1,5,7,9,12)
- **Roles- GOCO**: Full access to GOCO processes
- **GOCO operator**: Basic access to GOCO processes
- **GOCO supervisor**: Full access to GOCO processes

### System Administrator Roles (Full Access to All Pages 1-25)
- **Roles- System administrator**: All Pages, Can assign other admins, Can approve roles
- **Master Admin/Super Admin**: All Pages, Can assign other admins, Can approve roles
- **System Administrator-1**: All Pages
- **System Administrator-2**: All Pages
- **System Administrator-3**: All Pages

## Permission Types

Each role can have the following permission types for their assigned pages:

- **view**: Can view the page/content
- **add**: Can add new items
- **edit**: Can edit existing items
- **delete**: Can delete items (restricted for most roles)
- **approve**: Can approve/reject submissions

## Setup Instructions

### Automatic Setup (Recommended)

The permissions are automatically set up when you run Django migrations:

```bash
python manage.py migrate
```

This will automatically run the `setup_default_role_permissions` command.

### Manual Setup

If you need to set up permissions manually or update existing ones:

```bash
# Set up permissions for all roles
python manage.py setup_default_role_permissions

# Dry run to see what would be done
python manage.py setup_default_role_permissions --dry-run

# Force recreation of permissions
python manage.py setup_default_role_permissions --force
```

### Command Options

- `--dry-run`: Show what would be done without making changes
- `--force`: Force recreation of permissions even if they exist

## Database Structure

The system uses your existing page-based permission system:

- **Page**: Stores available pages in the system (1-25)
- **PagePermission**: Links groups to pages with specific permission types
- **auth_group**: Stores user groups/roles

## Content Type Mapping

Permissions are mapped to specific pages in your system:

- **Dashboard** → Page 1
- **Raw Material Batch** → Page 5
- **Consumable Batch** → Page 7
- **Component Batch** → Page 9
- **Product Batch** → Page 12
- **Process Log-Sheet** → Page 22
- **Stage Clearance** → Page 23
- **Q.A.R-Report** → Page 24
- **All other pages** → Pages 2-4, 6, 8, 10-11, 13-21, 25

## Troubleshooting

### Common Issues

1. **Permission not found errors**: Ensure the pages exist and have been created
2. **Group not found errors**: Run the command with `--force` to recreate groups
3. **Page errors**: Check that all required pages are in the Page model

### Verification

To verify permissions are set up correctly:

```bash
# Check group permissions
python manage.py shell
>>> from qdpc.models.page_permission import PagePermission
>>> from django.contrib.auth.models import Group
>>> group = Group.objects.get(name='Division Head SDA')
>>> perms = PagePermission.objects.filter(group=group)
>>> print(f"Permissions: {perms.count()}")
>>> for perm in perms[:5]:
...     print(f"- {perm.page_name}: {perm.permission_type}")
```

### Logs

The command provides detailed output showing:
- Which groups were created
- Which pages were created/updated
- Which permissions were assigned
- Any errors or warnings

## Customization

To modify permissions for specific roles:

1. Edit the `role_permissions` dictionary in `setup_default_role_permissions.py`
2. Run the command with `--force` to apply changes
3. Or create a new migration for permanent changes

## Security Notes

- Most roles do not have delete permissions for safety
- System administrators have full access to all pages
- Guest users have minimal read-only access to dashboard only
- All changes are logged and can be audited
- Page permissions are checked by default in the roles and permissions dashboard

## Support

For issues or questions about the permission system:
1. Check the command output for error messages
2. Verify database connectivity and page existence
3. Review the VSSC role permissions table
4. Contact the development team for complex issues

## VSSC Compliance

This implementation follows the exact VSSC requirements:
- ✅ All 25 pages are created with proper sections
- ✅ Role permissions match the official VSSC table
- ✅ Page access patterns are implemented exactly as specified
- ✅ Permission types align with VSSC workflow requirements
- ✅ System administrator roles have full access to all pages
