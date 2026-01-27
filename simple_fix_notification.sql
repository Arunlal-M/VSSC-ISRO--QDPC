-- Simple SQL script to fix notification table schema
-- Execute these commands one by one in your database console

ALTER TABLE qdpc_core_models_notification ADD COLUMN title VARCHAR(200) DEFAULT 'Notification';
ALTER TABLE qdpc_core_models_notification ADD COLUMN notification_type VARCHAR(20) DEFAULT 'create';
ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_type VARCHAR(50) DEFAULT 'product_batch';
ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_id INTEGER NULL;
ALTER TABLE qdpc_core_models_notification ADD COLUMN entity_name VARCHAR(200) DEFAULT '';
ALTER TABLE qdpc_core_models_notification ADD COLUMN created_by_id INTEGER NULL;
ALTER TABLE qdpc_core_models_notification MODIFY COLUMN message TEXT;
