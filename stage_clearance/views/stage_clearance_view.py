from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings

class StageClearance(BaseModelViewSet):
    template_name = 'stageclearance.html'

    def get(self, request):
        return render(request, self.template_name)
