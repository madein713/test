from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PersonIIN
from .serializers import PersonIINSerializer


class SnippetList(APIView):
    def get(self, request, iin=None):
        if iin is not None:
            queryset = PersonIIN.objects.get(iin=iin)
            serializer = PersonIINSerializer(queryset)
        else:
            queryset = PersonIIN.objects.all()
            serializer = PersonIINSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, iin=None):
        serializer = PersonIINSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
