from rest_framework import serializers
from qdpc_core_models.models.equipment import Equipment
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class EquipmentSerializer(serializers.ModelSerializer):
    # This field will be read-only since it is auto-calculated
    calibration_due_date = serializers.DateField(read_only=True)

    class Meta:
        model = Equipment
        fields = ['id','name','equipment_owner', 'serial_no', 'make', 'last_calibration_date', 
                  'calibration_validity_duration_type', 'calibration_validity_duration_value', 
                  'calibration_due_date', 'calibration_certificate',
                 ]

    def validate(self, data):
        # Ensure that the calibration validity duration value is positive
        if data['calibration_validity_duration_value'] <= 0:
            raise serializers.ValidationError("Calibration validity duration must be a positive value.")
        
        # Ensure validity type is either 'days' or 'months'
        if data['calibration_validity_duration_type'] not in ['days', 'months','years']:
            raise serializers.ValidationError("Invalid calibration validity duration type. Must be 'days' or 'months' or 'years'.")
        
        return data

    def create(self, validated_data):
        # Calculate calibration due date before saving
        last_calibration_date = validated_data['last_calibration_date']
        validity_type = validated_data['calibration_validity_duration_type']
        validity_value = validated_data['calibration_validity_duration_value']

        # Calculate due date based on validity type
        if validity_type == 'days':
            due_date = last_calibration_date + timedelta(days=validity_value)
        elif validity_type == 'months':
            due_date = last_calibration_date + relativedelta(months=validity_value)
        elif validity_type == 'years':
            due_date = last_calibration_date + relativedelta(years=validity_value)
        else:
            raise serializers.ValidationError("Invalid calibration validity duration type.")  # Fallback safeguard

        # Create the Equipment instance with the calculated due date
        equipment = Equipment.objects.create(
            calibration_due_date=due_date,
            **validated_data
        )
        return equipment
