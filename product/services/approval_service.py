from django.contrib.auth.models import Group
from django.db import transaction
from qdpc.models.page_permission import PagePermission
from qdpc_core_models.models.productBatch import ProductBatchs
from django.utils import timezone


class ProductBatchApprovalService:
    """Service class for handling product batch approvals based on VSSC role permissions"""
    
    @staticmethod
    def can_approve_product_batch(user, batch):
        """
        Check if user can approve a specific product batch based on:
        1. User's role permissions
        2. Batch status
        3. User's role hierarchy
        """
        if not user.is_authenticated:
            return False, "User not authenticated"
        
        if batch.status != 'pending':
            return False, f"Batch status is {batch.status}, only pending batches can be approved"
        
        # Check if user has approval permission for Product Batch page using unified system
        from product.services.permission_service import ProductBatchPermissionService
        has_approval_permission = ProductBatchPermissionService.check_user_permission(user, 'approve')
        
        if not has_approval_permission and not user.is_superuser:
            return False, "User does not have approval permission for Product Batch"
        
        # Check role-specific approval logic using unified permission system
        user_groups = [group.name for group in user.groups.all()]
        
        # If user has approval permission from dashboard, check role-specific logic
        if has_approval_permission:
            # QA Roles - can approve QA-related batches
            if any('QA' in group for group in user_groups):
                return ProductBatchApprovalService._can_qa_approve(user_groups, batch)
            
            # QC Roles - can approve QC-related batches
            elif any('QC' in group for group in user_groups):
                return ProductBatchApprovalService._can_qc_approve(user_groups, batch)
            
            # Testing Agency Roles
            elif any('Testing agency' in group for group in user_groups):
                return ProductBatchApprovalService._can_testing_agency_approve(user_groups, batch)
            
            # Industry Roles
            elif any('industry' in group for group in user_groups):
                return ProductBatchApprovalService._can_industry_approve(user_groups, batch)
            
            # GOCO Roles
            elif any('GOCO' in group for group in user_groups):
                return ProductBatchApprovalService._can_goco_approve(user_groups, batch)
            
            # System Administrators
            elif any('Admin' in group or 'Super Admin' in group for group in user_groups) or user.is_superuser:
                return True, "System Administrator has full approval rights"
            
            # Default approval for users with dashboard permission
            return True, "User has approval permission from dashboard"
        
        return False, "User does not have approval permission from dashboard"
    

    
    @staticmethod
    def _can_qa_approve(user_groups, batch):
        """Check if QA user can approve based on role hierarchy"""
        if 'Division Head QA' in user_groups:
            return True, "Division Head QA can approve all QA submissions"
        elif 'Section Head QA' in user_groups:
            # Section Head QA can approve submissions from lower-level QA roles
            if batch.submitted_by_role and any(role in batch.submitted_by_role for role in ['Engineer QA', 'Technical/Scientific staff QA']):
                return True, "Section Head QA can approve lower-level QA submissions"
            return False, "Section Head QA can only approve lower-level QA submissions"
        else:
            return False, "Lower-level QA roles cannot approve batches"
    
    @staticmethod
    def _can_qc_approve(user_groups, batch):
        """Check if QC user can approve based on role hierarchy"""
        if 'Division Head QC' in user_groups:
            return True, "Division Head QC can approve all QC submissions"
        elif 'Section Head QC' in user_groups:
            # Section Head QC can approve submissions from lower-level QC roles
            if batch.submitted_by_role and any(role in batch.submitted_by_role for role in ['Engineer QC', 'Technical/Scientific staff QC']):
                return True, "Section Head QC can approve lower-level QC submissions"
            return False, "Section Head QC can only approve lower-level QC submissions"
        else:
            return False, "Lower-level QC roles cannot approve batches"
    
    @staticmethod
    def _can_testing_agency_approve(user_groups, batch):
        """Check if Testing Agency user can approve based on role hierarchy"""
        if 'Division Head Testing agency' in user_groups:
            return True, "Division Head Testing agency can approve all testing submissions"
        elif 'Section Head Testing agency' in user_groups:
            # Section Head can approve submissions from lower-level testing roles
            if batch.submitted_by_role and any(role in batch.submitted_by_role for role in ['Engineer Testing agency', 'Technical/Scientific staff Testing agency']):
                return True, "Section Head Testing agency can approve lower-level testing submissions"
            return False, "Section Head Testing agency can only approve lower-level testing submissions"
        else:
            return False, "Lower-level Testing agency roles cannot approve batches"
    
    @staticmethod
    def _can_industry_approve(user_groups, batch):
        """Check if Industry user can approve based on role hierarchy"""
        if any(role in user_groups for role in ['QC Manager industry', 'QA Manager industry']):
            return True, "Industry Manager can approve industry submissions"
        elif 'Process Manager industry' in user_groups:
            return False, "Process Manager cannot approve batches"
        else:
            return False, "Industry operator/technician roles cannot approve batches"
    
    @staticmethod
    def _can_goco_approve(user_groups, batch):
        """Check if GOCO user can approve based on role hierarchy"""
        if 'GOCO supervisor' in user_groups:
            return True, "GOCO supervisor can approve GOCO submissions"
        else:
            return False, "GOCO operator cannot approve batches"
    
    @staticmethod
    def approve_batch(user, batch, approval_remarks=None):
        """
        Approve a product batch with proper role-based validation
        """
        can_approve, message = ProductBatchApprovalService.can_approve_product_batch(user, batch)
        
        if not can_approve:
            return False, message
        
        try:
            with transaction.atomic():
                # Update batch status
                batch.status = 'approved'
                batch.qa_approval_date = timezone.now()
                batch.qa_approved_by = user
                
                # Store approval remarks
                if approval_remarks:
                    batch.approval_remarks = approval_remarks
                
                batch.save()
                
                return True, "Batch approved successfully"
                
        except Exception as e:
            return False, f"Error approving batch: {str(e)}"
    
    @staticmethod
    def reject_batch(user, batch, rejection_reason):
        """
        Reject a product batch with proper role-based validation
        """
        can_approve, message = ProductBatchApprovalService.can_approve_product_batch(user, batch)
        
        if not can_approve:
            return False, message
        
        try:
            with transaction.atomic():
                # Update batch status
                batch.status = 'rejected'
                batch.rejection_reason = rejection_reason
                batch.qa_approval_date = timezone.now()
                batch.qa_approved_by = user
                
                batch.save()
                
                return True, "Batch rejected successfully"
                
        except Exception as e:
            return False, f"Error rejecting batch: {str(e)}"
    
    @staticmethod
    def get_user_approval_permissions(user):
        """
        Get comprehensive approval permissions for a user using unified permission system
        """
        if not user.is_authenticated:
            return {}
        
        # Use the unified permission service
        from product.services.permission_service import ProductBatchPermissionService
        
        permissions = {
            'can_approve_product_batch': ProductBatchPermissionService.check_user_permission(user, 'approve'),
            'can_reject_product_batch': ProductBatchPermissionService.check_user_permission(user, 'approve'),  # Same permission for reject
            'user_roles': [group.name for group in user.groups.all()],
            'approval_level': 'none',
            'explanation': ''
        }
        
        # Determine approval level based on permissions
        if user.is_superuser:
            permissions['approval_level'] = 'system_admin'
            permissions['explanation'] = 'System Administrator has full approval rights'
        elif permissions['can_approve_product_batch']:
            permissions['approval_level'] = 'has_approval_permission'
            permissions['explanation'] = 'User has approval permission from dashboard'
        else:
            permissions['approval_level'] = 'no_approval'
            permissions['explanation'] = 'User does not have approval permission from dashboard'
        
        return permissions
