from django.contrib import admin

# Register models in Django admin site

# User and Role models
from .models.user import User
from .models.role import Role
from .models.user_type import UserType
from .models.reset_password import ResetPassword

# Organizational models
from .models.division import Division
from .models.center import Center
from .models.industry import Industry

# Equipment models

from .models.equipment import EquipmentDocument
from .models.equipment import Equipment


# Raw Material models
from .models.raw_material import RawMaterial,RawMaterialDocument
from .models.raw_materialbach import RawMaterialBatch
from .models.raw_material_acceptence_test import RawMaterialAcceptanceTest

# Consumable models
from .models.consumable import Consumable,ConsumableDocument
from .models.consumablebatch import ConsumableBatch
from .models.consumable_acceptance_test import ConsumableAcceptanceTest
# from .models.consumable_document import ConsumableDocument

# Component models
from .models.component import Component,ComponentDocument
from .models.componentbatch import ComponentBatch
from .models.component_acceptance_test import ComponentAcceptanceTest
# from .models.component_document import ComponentDocument

# Product models
from .models.product import Product
from .models.product import ProductDocument
from .models.product_category import ProductCategory
from .models.product_component import ProductComponent

# Other related models
from .models.source import Sources
from .models.supplier import Suppliers
from .models.acceptance_test_result import AcceptanceTestResult
from .models.acceptance_test import AcceptanceTest
from .models.unit import Unit
from .models.test_result import TestResult
from .models.porcessing_agency import ProcessingAgency
from .models.testing_agency import TestingAgency
from .models.enduse import EndUse
from .models.process import Process, ProcessStep
from .models.grade import Grade
from .models.document_type import DocumentType


# Registering models in the admin site

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserType)
admin.site.register(ResetPassword)

# Organizational models
admin.site.register(Division)
admin.site.register(Center)
admin.site.register(Industry)

# Equipment models
admin.site.register(EquipmentDocument)
admin.site.register(Equipment)

# Raw Material models
admin.site.register(RawMaterial)
admin.site.register(RawMaterialDocument)
admin.site.register(RawMaterialBatch)
admin.site.register(RawMaterialAcceptanceTest)

# Consumable models
admin.site.register(Consumable)
admin.site.register(ConsumableDocument)
admin.site.register(ConsumableBatch)
admin.site.register(ConsumableAcceptanceTest)
# admin.site.register(ConsumableDocument)

# Component models
admin.site.register(Component)
admin.site.register(ComponentBatch)
admin.site.register(ComponentAcceptanceTest)
admin.site.register(ComponentDocument)

# Product models
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductComponent)
admin.site.register(ProductDocument)

# Other related models
admin.site.register(Sources)
admin.site.register(Suppliers)
admin.site.register(AcceptanceTest)
admin.site.register(AcceptanceTestResult)
admin.site.register(Unit)
admin.site.register(Grade)
admin.site.register(TestResult)
admin.site.register(ProcessingAgency)
admin.site.register(TestingAgency)
admin.site.register(EndUse)
admin.site.register(Process)
admin.site.register(ProcessStep)
admin.site.register(DocumentType)

