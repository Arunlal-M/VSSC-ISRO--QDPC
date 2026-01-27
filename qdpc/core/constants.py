LOGIN_FAILED = "Please enter a valid username or password."
LOGIN_SUCCESS = "Successfully Login."
USERNAME_PASSWORD_REQUIRED = "Username and password are required"
USERNAME_PASSWORD_EMPTY="username password required"
USERNAME_SENT_SUCCESS = "Username has been sent to your registered email!"
RESET_EMAIL_FAILED = "Email address not recognized. Please check and try again"
SIGNUP_FAILED = "Signup failed"
SIGNUP_SUCCESS = "Signup Success"
RESET_KEY_GENERATED_SUCCESS = "Reset key generated check your email"

CURRENT_PASSWORD = "You used this password recently." \
                   " Please choose a different one."

PASSWORD_RESET_SUCCESS = "Password reset sucess"
LOGIN_NOT_APPROVED_OR_INACTIVE = "Login Falied or Inactive User."
RETRIVED_USER_SUCCESS = "Retrived User Sucessfully"
USER_FETCH_FAILED = "User Fetch Failed"

RAW_MATERIAL_FETCH_FAILED="Raw material fetch failed"
USER_NOT_FOUND_IN_GROUP="No users found for the specified group"
APPROVED_SUCESS = "Sucessfully approved"
USER_UPDATE_FAILED = "User update failed"
USER_REJECT_SUCCESSFULLY = "User Reject Sucessfully"

USER_UPDATE_SUCCESS = "User updated Sucessfully"
RAW_MATERIAL_FETCH_FAILED="Raw material fetch failed"

RAW_MATERIAL_BACTCH_ADDED="Raw matrial Batch added"
RAW_MATERIAL_BATCH_FAILD="Raw matrial batch add faild"
RAW_MATERIAL_BATCH_DELETE_SUCCESSFULLY="Raw Material Batch Deleted Successfully"

ACCEPTANCETEST_DELETE_SUCCESSFULLY="Acceptance test deleted sucessfully"

SOURCE_CREATION_FAILED="Source creation failed due to invalid data."
SOURCE_CREATION_SUCESSFULLY="Source created successfully."
SOURCE_DELETE_SUCCESSFULLY="Source deleted sucessfully"

SUPPLIER_CREATION_FAILED="Supplier creation failed due to invalid data."
SUPPLIER_CREATION_SUCESSFULLY="Supplier created successfully."
SUPPLIER_DELETE_SUCCESSFULLY="Supplier deleted sucessfully"

DIVISION_CREATION_FAILED="Division creation failed due to invalid data."
DIVISION_CREATION_SUCESSFULLY="Division created successfully."
DIVISION_DELETE_SUCCESSFULLY="Division deleted sucessfully"

CENTER_CREATION_FAILED="Center creation failed due to invalid data."
CENTER_CREATION_SUCESSFULLY="Center created successfully."
CENTER_DELETE_SUCCESSFULLY="Center deleted sucessfully"

EQUIPMENT_CREATION_FAILED="Equipment creation failed due to invalid data."
EQUIPMENT_CREATION_SUCESSFULLY="Equipment created successfully."
EQUIPMENT_DELETE_SUCCESSFULLY="Equipment deleted sucessfully"

PRODUCT_DELETE_SUCCESSFULLY="Product deleted sucessfully"
PRODUCT_STATUS_UPDATE_SUCCESSFULLY="Product status updated sucessfully"

UNIT_CREATION_FAILED="Unit creation failed due to invalid data."
UNIT_CREATION_SUCESSFULLY="Unit created successfully."
UNIT_DELETE_SUCCESSFULLY="Unit deleted sucessfully"

RAWMATERIAL_DELETE_SUCCESSFULLY="Raw Material deleted sucessfully"
RAWMATERIAL_STATUS_UPDATE_SUCCESSFULLY="Raw Material status updated sucessfully"

GRADE_CREATION_FAILED="Grade creation failed due to invalid data."
GRADE_CREATION_SUCESSFULLY="Grade created successfully."
GRADE_DELETE_SUCCESSFULLY="Grade deleted sucessfully"

ENDUSE_CREATION_FAILED="Enduse creation failed due to invalid data."
ENDUSE_CREATION_SUCESSFULLY="Enduse created successfully."
ENDUSE_DELETE_SUCCESSFULLY="Enduse deleted sucessfully"

PRODUCT_CATEGORY_CREATION_FAILED="Product Category creation failed due to invalid data."
PRODUCT_CATEGORY_CREATION_SUCESSFULLY="Product Category created successfully."
PRODUCT_CATEGORY_DELETE_SUCCESSFULLY="Product Category deleted sucessfully"


CONSUMABLE_FETCH_FAILED="Consumable Fetch Failed"
CONSUMABLE_BATCH_FAILD="Consumable batch Failed"
CONSUMABLE_DELETE_SUCCESSFULLY="Consumable  Deleted Successfully"
CONSUMABLE_BATCH_DELETE_SUCCESSFULLY="Consumable Batch Deleted Successfully"

COMPONENT_FETCH_FAILED="Component Fetch Failed"
COMPONENT_BATCH_FAILED="Component batch Failed"
COMPONENT_DELETE_SUCCESSFULLY="Component  Deleted Successfully"
COMPONENT_BATCH_DELETE_SUCCESSFULLY="Component Batch Deleted Successfully"

PROCESS_STEP_DELETE_SUCCESSFULLY="Process Step deleted sucessfully"

DOCUMENT_CREATION_FAILED="Document creation failed due to invalid data."
DOCUMENT_CREATION_SUCESSFULLY="Document created successfully."
DOCUMENT_DELETE_SUCCESSFULLY="Document deleted sucessfully"

# Default Django auth groups to seed on fresh installs
DEFAULT_AUTH_GROUPS = [
   # Guest role
                'Guest',

                # In-house/Project roles
                'Roles- In house process',
                'DPD Project',
                'Engineer Project',

                # SDA roles
                'Division Head SDA',
                'Section Head SDA',
                'Engineer SDA',
                'Technical/Scientific staff SDA',
                'Operator/Technicians SDA',

                # QA roles
                'Division Head QA',
                'Section Head QA',
                'Engineer QA',
                'Technical/Scientific staff QA',

                # QC roles
                'Division Head QC',
                'Section Head QC',
                'Engineer QC',
                'Technical/Scientific staff QC',

                # Testing agency roles
                'Division Head Testing agency',
                'Section Head Testing agency',
                'Engineer Testing agency',
                'Technical/Scientific staff Testing agency',

                # LSC roles
                'Member secretary, LSC',
                'Chairman, LSC',

                # NCRB roles
                'Member secretary, NCRB',
                'Chairman, NCRB',

                # Industry process roles
                'Roles- Industry process',
                'Operator/Technician industry',
                'Process Manager industry',
                'QC Manager industry',
                'QA Manager industry',

                # GOCO roles
                'Roles- GOCO',
                'GOCO operator',
                'GOCO supervisor',

                # System administrator roles
                'Roles- System administrator',
                'Master Admin/Super Admin',
                'System Administrator-1',
                'System Administrator-2',
                'System Administrator-3'
]