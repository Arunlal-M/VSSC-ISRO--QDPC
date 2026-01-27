# VSSC Role-Based Permission System Guide

## Overview
The VSSC (Vendor Support and Service Center) system implements a comprehensive role-based permission system that controls access to different pages and functionalities based on user roles. This system ensures that users can only access features appropriate to their responsibilities and authority level.

## Page Structure
The system consists of 25 pages organized into functional areas:

### 1. Core Pages
- **Dashboard (1)**: Main system overview and navigation
- **Groups (25)**: Role and permission management

### 2. Product Data Management
- **Equipments (2)**: Equipment management
- **Acceptance Test (3)**: Test management
- **Rawmaterial (4)**: Raw material management
- **Rawmaterial Batch (5)**: Raw material batch processing
- **Consumable (6)**: Consumable management
- **Consumable Batch (7)**: Consumable batch processing
- **Component (8)**: Component management
- **Component Batch (9)**: Component batch processing
- **Process (10)**: Process management
- **Product (11)**: Product management
- **Product Batch (12)**: Product batch processing

### 3. Miscellaneous Data Management
- **Units (13)**: Unit definitions
- **Grade (14)**: Quality grades
- **Enduse (15)**: End use applications
- **Document Type (16)**: Document categorization
- **Center (17)**: Center management
- **Division (18)**: Division management
- **Source (19)**: Source management
- **Supplier (20)**: Supplier management

### 4. User Management
- **Users (21)**: User account management

### 5. Report Generation
- **Process Log-Sheet (22)**: Process logging and reporting
- **Stage Clearance (23)**: Stage clearance management
- **Q.A.R-Report (24)**: Quality Assurance Report

## Role Categories and Permissions

### SDA (System Development and Administration) Roles

#### Division Head SDA
- **Pages**: 1, 5, 7, 9, 12, 22
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**: 
  - Can add new batches
  - Approve/reject Section Head SDA and Engineer SDA submissions
  - Send approved items to QA review
  - Full administrative control over assigned pages

#### Section Head SDA
- **Pages**: 1, 5, 7, 9, 12, 22
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Can add new batches
  - Approve/reject Engineer SDA, Technical/Scientific staff SDA, and Operator/Technicians SDA submissions
  - Submit approved items to Division Head SDA
  - Full administrative control over assigned pages

#### Engineer SDA
- **Pages**: 1, 5, 7, 9, 12, 22
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Can add new batches
  - Submit items to Section Head SDA for approval
  - Cannot approve or delete items

#### Technical/Scientific staff SDA
- **Pages**: 1, 5, 7, 9, 12, 22
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Can add new batches
  - Submit items to Section Head SDA for approval
  - Cannot approve or delete items

#### Operator/Technicians SDA
- **Pages**: 1, 5, 7, 9, 12, 22
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Can add new batches
  - Submit items to Section Head SDA for approval
  - Cannot approve or delete items

### QA (Quality Assurance) Roles

#### Division Head QA
- **Pages**: 1, 12, 23, 24
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Approve/reject Section Head QA and Engineer QA submissions
  - Final QA authority for assigned pages

#### Section Head QA
- **Pages**: 1, 12, 23, 24
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Submit items to Division Head QA
  - Reject Engineer QA and Technical/Scientific staff QA submissions
  - Cannot approve final submissions

#### Engineer QA
- **Pages**: 1, 12, 23, 24
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head QA
  - Cannot approve or delete items

#### Technical/Scientific staff QA
- **Pages**: 1, 12, 23, 24
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head QA
  - Cannot approve or delete items

### QC (Quality Control) Roles

#### Division Head QC
- **Pages**: 1, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Approve/reject Section Head QC and Engineer QC submissions
  - Final QC authority for assigned pages

#### Section Head QC
- **Pages**: 1, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Submit items to Division Head QC
  - Reject Engineer QC and Technical/Scientific staff QC submissions
  - Cannot approve final submissions

#### Engineer QC
- **Pages**: 1, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head QC
  - Cannot approve or delete items

#### Technical/Scientific staff QC
- **Pages**: 1, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head QC
  - Cannot approve or delete items

### Testing Agency Roles

#### Division Head Testing agency
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Approve/reject Section Head Testing agency and Engineer Testing agency submissions
  - Final authority for testing agency operations

#### Section Head Testing agency
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Submit items to Division Head Testing agency
  - Reject Engineer Testing agency and Technical/Scientific staff Testing agency submissions

#### Engineer Testing agency
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head Testing agency
  - Cannot approve or delete items

#### Technical/Scientific staff Testing agency
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Submit items to Section Head Testing agency
  - Cannot approve or delete items

### Industry Roles

#### Operator/Technician industry
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Basic operational access
  - Cannot approve or delete items

#### Process Manager industry
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete
- **Responsibilities**:
  - Process management capabilities
  - Cannot approve items

#### QC Manager industry
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Quality control management
  - Approval authority for industry operations

#### QA Manager industry
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Quality assurance management
  - Approval authority for industry operations

### GOCO (Government Owned, Contractor Operated) Roles

#### GOCO operator
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit
- **Responsibilities**:
  - Basic operational access
  - Cannot approve or delete items

#### GOCO supervisor
- **Pages**: 1, 5, 7, 9, 12
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Supervisory control
  - Approval authority for GOCO operations

### System Administrator Roles

#### Master Admin/Super Admin
- **Pages**: All (1-25)
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Full system access
  - Can assign other admins
  - Can approve roles
  - Complete administrative control

#### System Administrator-1, 2, 3
- **Pages**: All (1-25)
- **Permissions**: View, Add, Edit, Delete, Approve
- **Responsibilities**:
  - Full system access
  - Complete administrative control

## Permission Types

### View
- Basic access to view page content
- Required for all functional access

### Add
- Ability to create new records/entries
- Required for batch creation and data entry

### Edit
- Ability to modify existing records
- Required for data updates and corrections

### Delete
- Ability to remove records
- Restricted to supervisory and administrative roles

### Approve
- Ability to approve/reject submissions
- Highest level of authority
- Required for workflow progression

## Workflow Patterns

### SDA Workflow
1. **Operator/Technician/Engineer/Technical Staff** → Create batches
2. **Section Head** → Review and approve/reject
3. **Division Head** → Final review and approval
4. **QA Review** → Quality assurance check

### QA Workflow
1. **Engineer/Technical Staff** → Submit for QA review
2. **Section Head QA** → Initial QA review
3. **Division Head QA** → Final QA approval

### QC Workflow
1. **Engineer/Technical Staff** → Submit for QC review
2. **Section Head QC** → Initial QC review
3. **Division Head QC** → Final QC approval

## Security Features

- **Role-based Access Control**: Users can only access features appropriate to their role
- **Hierarchical Approval**: Multi-level approval process ensures proper oversight
- **Audit Trail**: All actions are logged for compliance and security
- **Permission Inheritance**: Higher-level roles inherit lower-level permissions
- **Granular Control**: Fine-grained permission control at page and function level

## Implementation Notes

- All permissions are managed through the Django permission system
- Page permissions are stored in the `PagePermission` model
- User roles are managed through Django's built-in `Group` system
- The system automatically enforces permissions at the view level
- Permission changes take effect immediately without system restart

## Best Practices

1. **Principle of Least Privilege**: Users should have only the minimum permissions necessary
2. **Regular Review**: Periodically review and update role permissions
3. **Documentation**: Keep role descriptions and responsibilities up to date
4. **Testing**: Test permission changes in a development environment first
5. **Backup**: Maintain backup of permission configurations

## Troubleshooting

### Common Issues
- **User cannot access expected pages**: Check group membership and page permissions
- **Approval buttons not showing**: Verify user has 'approve' permission for the page
- **Permission changes not taking effect**: Ensure user is logged out and back in

### Debug Steps
1. Check user's group membership
2. Verify page permissions for the user's groups
3. Check Django permission cache
4. Review permission enforcement in views
5. Check database for permission records

## Support

For technical support or questions about the permission system:
- Review this documentation
- Check the permission dashboard for current settings
- Contact system administrators for role changes
- Use the debug tools in the permission management interface
