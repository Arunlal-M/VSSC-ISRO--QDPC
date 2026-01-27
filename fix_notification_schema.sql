-- SQL script to add missing columns to notification table
-- Run this script in your MySQL/database console to fix the schema

-- Check if columns exist before adding them
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'title' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN title VARCHAR(200) DEFAULT "Notification"',
    'SELECT "Column title already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'notification_type' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN notification_type VARCHAR(20) DEFAULT "create"',
    'SELECT "Column notification_type already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'entity_type' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_type VARCHAR(50) DEFAULT "product_batch"',
    'SELECT "Column entity_type already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'entity_id' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_id INTEGER NULL',
    'SELECT "Column entity_id already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'entity_name' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_name VARCHAR(200) DEFAULT ""',
    'SELECT "Column entity_name already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'created_by_id' 
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD COLUMN created_by_id INTEGER NULL',
    'SELECT "Column created_by_id already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Modify message column to TEXT
ALTER TABLE qdpc_core_models_notification MODIFY COLUMN message TEXT;

-- Add foreign key constraint for created_by_id if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
     WHERE table_name = 'qdpc_core_models_notification' 
     AND column_name = 'created_by_id' 
     AND constraint_name LIKE '%fk%'
     AND table_schema = DATABASE()) = 0,
    'ALTER TABLE qdpc_core_models_notification ADD CONSTRAINT fk_notification_created_by FOREIGN KEY (created_by_id) REFERENCES qdpc_core_models_user(id) ON DELETE SET NULL',
    'SELECT "Foreign key constraint already exists"'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
