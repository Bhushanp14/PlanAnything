from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerializer

@api_view(['GET'])
def get_all_plans(request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)
