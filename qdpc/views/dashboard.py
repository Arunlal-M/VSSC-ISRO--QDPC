from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.consumable import Consumable
from product.serializers.activity_serializer import  ActivityLogSerializer



class DashboardSummaryAPI(APIView):
    """API for dashboard summary cards"""
    def get(self, request):
        print("Card called")
        data = {
            "component": {
                "count": Component.objects.count(),
                
            },
            "raw_materials": {
                "count": RawMaterial.objects.count(),
               
            },
            "consumables": {
                "count": Consumable.objects.count(),
               
            },
            "products": {
                "count": Product.objects.count(),
               
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class ResourceStatusAPI(APIView):
    """API for resource status bars"""
    def get(self, request):
        total_component = Component.objects.count()
        in_use_component = Component.objects.count()
        total_raw_material = RawMaterial.objects.count()
        in_raw_material = RawMaterial.objects.count()
        total_consumable = Consumable.objects.count()
        in_consumable = Consumable.objects.count()
        
        data = [
            {
                "label": "Component in use",
                "value": in_use_component,
                "total": total_component,
                "percentage": (in_use_component / total_component) * 100 if total_component else 0,
                "status": "active"
            },
            {
                "label": "Raw materials in use",
                "value": RawMaterial.objects.count(),
                "total": total_raw_material,
                "percentage": (in_raw_material / total_raw_material) * 100 if total_raw_material else 0,
                "status": "active"
            },
            {
                "label": "Consumable in use",
                "value": Consumable.objects.count(),
                "total": total_consumable,
                "percentage": (in_consumable / total_consumable) * 100 if total_consumable else 0,
                "status": "active"
            }
        ]
        return Response(data, status=status.HTTP_200_OK)



class InventoryTrendsAPI(APIView):
    """API for line chart data (last 12 months)"""
    def get(self, request):
        # Get current month and year
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        
        # Generate labels for all 12 months (Jan-Dec)
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Initialize data structure
        data = {
            "labels": month_names,
            "datasets": []
        }

        # Helper function to get monthly counts
        def get_monthly_counts(model):
            counts = [0] * 12  # Initialize with zeros for all months
            
            # Query for records created in the current year
            records = model.objects.filter(
                created_at__year=current_year
            ).values_list('created_at', flat=True)
            
            # Count records per month
            for date in records:
                month_index = date.month - 1  # Convert to 0-based index
                counts[month_index] += 1
                
            return counts

        # Get data for each inventory type
        data["datasets"] = [
            {
                "label": "Component",
                "data": get_monthly_counts(Component),
                "borderColor": "#4e73df",
                "backgroundColor": "rgba(78, 115, 223, 0.05)"
            },
            {
                "label": "Consumables",
                "data": get_monthly_counts(Consumable),
                "borderColor": "#36b9cc",
                "backgroundColor": "rgba(54, 185, 204, 0.05)"
            },
           
        ]

        return Response(data, status=status.HTTP_200_OK)



class InventoryDistributionAPI(APIView):
    """API for pie chart data"""
    def get(self, request):
        data = {
            "labels": ["Component", "Raw Materials", "Consumables", "Products"],
            "datasets": [{
                "data": [
                    Component.objects.count(),
                    RawMaterial.objects.count(),
                    Consumable.objects.count(),
                    Product.objects.count()
                ]
            }]
        }
        return Response(data, status=status.HTTP_200_OK)

from product.serializers.activity_serializer import ActivitySerializer
from  qdpc_core_models.models.activity import  Activity


class RecentActivityAPI(APIView):
    """API for recent activity logs"""
    def get(self, request):
        # Get activities from last 7 days by default
        recent_date = timezone.now() - timedelta(days=7)
        queryset = Activity.objects.select_related('user', 'content_type')[:50]  # Show last 50
        serializer = ActivitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

