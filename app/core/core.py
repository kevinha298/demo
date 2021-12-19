from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 

class MemberList(APIView):
    def get(self, request):
        model = Member.objects.all()
        serializer = MemberSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberDetail(APIView):
    def get_user(self, mrn):
        try:
            model = Member.objects.get(id=mrn)
            return model
        except Member.DoesNotExist:
            return

    def get(self, request, mrn):
        if not self.get_user(mrn):
            return Response(f'User with ID: {mrn} is not found in database.', status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(self.get_user(mrn))
        return Response(serializer.data)

    def put(self, request, mrn):
        if not self.get_user(mrn):
            return Response(f'User with ID: {mrn} is not found in database.', status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(self.get_user(mrn), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mrn):
        if not self.get_user(mrn):
            return Response(f'User with ID: {mrn} is not found in database.', status=status.HTTP_404_NOT_FOUND)
        model = self.get_user(mrn)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)