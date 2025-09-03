# Setup Guide for Roles and Permissions System

## 🚨 **IMPORTANT: Fresh Migration System Applied**

The system has been completely reset with a fresh migration approach:

1. **Removed all old migrations** after 0018
2. **Created single comprehensive migration** (0019) for the entire roles and permissions system
3. **SQLite-optimized** with proper field definitions and indexes
4. **Clean database schema** without conflicts

## 📋 **Setup Steps**

### 1. **Reset Migration State (if needed)**
If you're still having issues, you may need to reset the migration state:

```bash
# Remove any failed migration records
python manage.py migrate qdpc_core_models 0018 --fake

# Or if you need to start fresh (WARNING: This will reset your database)
python manage.py migrate qdpc_core_models zero
```

### 2. **Run the New Migration**
```bash
python manage.py migrate
```

### 3. **Clean Up Existing Roles (if you get duplicate key errors)**
If you encounter "Duplicate entry" errors, run the cleanup command:

```bash
# Basic cleanup
python manage.py cleanup_roles

# Force cleanup (removes orphaned data)
python manage.py cleanup_roles --force
```

### 4. **Initialize the System**
```bash
# Normal initialization
python manage.py init_roles_permissions

# Force recreation (if you want to start fresh)
python manage.py init_roles_permissions --force
```

### 5. **Create a Superuser (if needed)**
```bash
python manage.py createsuperuser
```

## 🔧 **Troubleshooting**

### **SQLite Database Issues**
If you encounter SQLite-specific issues:

#### **Option 1: Check SQLite Version**
Ensure you're using SQLite 3.8.0 or higher:
```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

#### **Option 2: Reset Database (Development Only)**
If you're in development and can lose data:
```bash
# Remove the database file
rm db.sqlite3

# Run migrations to recreate it
python manage.py migrate
```

#### **Option 3: Check File Permissions**
Ensure the SQLite database file is writable:
```bash
# On Windows, check file properties
# On Linux/Mac, check permissions
ls -la db.sqlite3
```

### **Duplicate Key Error (Role Already Exists)**
If you get "Duplicate entry" errors:

1. **Run the cleanup command first:**
   ```bash
   python manage.py cleanup_roles
   ```

2. **Then initialize with force mode:**
   ```bash
   python manage.py init_roles_permissions --force
   ```

3. **Or manually check existing roles:**
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import Group
   from qdpc_core_models.models import Role
   
   # Check existing groups
   print("Existing Django Groups:")
   for group in Group.objects.all():
       print(f"  - {group.name} (ID: {group.id})")
   
   # Check existing roles
   print("\nExisting Roles:")
   for role in Role.objects.all():
       print(f"  - {role.name} (ID: {role.id})")
   ```

## 📊 **What the System Provides**

### **Models Created:**
- ✅ **CustomPermission**: Granular permissions organized by modules
- ✅ **RolePermission**: Links roles to custom permissions
- ✅ **Enhanced Role**: Extended Django Group model with custom fields

### **Views Available:**
- ✅ **Role Management**: `/groups/`
- ✅ **Permission Assignment**: `/permissions/role/<id>/`
- ✅ **Permission Overview**: `/permissions/`
- ✅ **Permission Admin**: `/permissions/manage/`

### **Default Roles:**
- ✅ **GUEST**: Basic read access
- ✅ **INDUSTRY**: Limited access + reports
- ✅ **QA**: Quality assurance access
- ✅ **QC**: Quality control access
- ✅ **SDA**: Extended access + export
- ✅ **ADMIN**: Management access
- ✅ **SUPER ADMIN**: Full system access
- ✅ **MASTER ADMIN**: Complete access

## 🧪 **Testing the System**

### **Run the Test Script:**
```bash
python test_permissions.py
```

### **Manual Testing:**
1. Visit `/groups/` to see roles
2. Click "Manage Permissions" on any role
3. Assign/remove permissions
4. Check user access based on roles

## 🚀 **Next Steps**

1. **Customize Permissions**: Modify the default permissions in the management command
2. **Add Role Checks**: Use the permission mixins in your views
3. **Integrate with Existing Views**: Add permission checks to your current views
4. **Test Thoroughly**: Ensure all permission checks work as expected

## 📞 **Need Help?**

If you encounter any issues:

1. **Check the logs** for specific error messages
2. **Verify SQLite version** and database file permissions
3. **Ensure all migrations** are applied successfully
4. **Run cleanup commands** if you have role conflicts
5. **Check the README** for detailed documentation

## 🔒 **Security Notes**

- **Default roles are protected** and cannot be deleted
- **Permission assignments are audited** (who granted what, when)
- **Role-based access control** is enforced at the view level
- **Mixins and decorators** provide easy permission checking

## 🆘 **Emergency Recovery**

If everything goes wrong and you need to start over:

```bash
# 1. Reset migrations
python manage.py migrate qdpc_core_models zero

# 2. Remove problematic migration files
# (Delete any migration files after 0018)

# 3. Run migrations again
python manage.py migrate

# 4. Clean up and initialize
python manage.py cleanup_roles --force
python manage.py init_roles_permissions --force
```

## 💾 **SQLite Best Practices**

- **Regular backups**: Copy `db.sqlite3` file regularly
- **Avoid concurrent writes**: SQLite doesn't handle multiple writers well
- **Use transactions**: Wrap multiple operations in transactions
- **Monitor file size**: Large databases can become slow

## 🆕 **Migration Structure**

### **Current Migration Files:**
- `0001_initial.py` - Initial models
- `0002_productbatchs_productbatchrawmaterial_and_more.py` - Product batch models
- `0003_alter_productbatchs_batch_id_and_more.py` - Product batch alterations
- `0004_alter_productbatchs_batch_id_and_more.py` - More product batch alterations
- `0005_rawmaterialacceptencetest.py` - Raw material acceptance test
- `0006_alter_productbatchacceptancetest_result.py` - Acceptance test alterations
- `0007_alter_productbatchrawmaterial_batch.py` - Raw material batch alterations
- `0008_alter_equipmentdocument_equipment.py` - Equipment document alterations
- `0009_rename_document_equipmentdocument_documentfile.py` - Document renaming
- `0010_remove_user_role_id.py` - User role ID removal
- `0011_user_role_id.py` - User role ID addition
- `0012_remove_user_role_id_remove_user_role_user_role.py` - User role cleanup
- `0013_alter_user_is_active_alter_user_is_approved_and_more.py` - User field alterations
- `0014_alter_sources_email_alter_suppliers_email.py` - Email field alterations
- `0015_create_superadmin.py` - Super admin creation
- `0016_rolemeta_page_codes_and_seed_roles.py` - Role metadata and seeding
- `0017_seed_additional_roles.py` - Additional role seeding
- `0018_set_all_roles_full_access.py` - Role access setup
- `0019_roles_and_permissions_system.py` - **NEW: Complete roles and permissions system**

---

**The system is now ready to use with SQLite and a clean migration structure!** 🎉
