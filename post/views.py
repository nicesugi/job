from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company
)
from post.serializers import JobPostSerializer
from django.db.models.query_utils import Q


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)

        return Response(status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )
        company_name = request.data.get("company_name", None)
        job_serializer = JobPostSerializer(data=request.data)
        
        if job_serializer.is_valid():
            job_instance = get_object_or_404(JobType, id=request.data['job_type'])
            print(job_instance)
            company_instance = get_object_or_404(Company, id=request.data['company_name'])
            print(company_instance)
            job_serializer.save(job_type=job_instance, company_name=company_instance) #ValueError: Cannot assign "1": "JobPost.job_type" must be a "JobType" instance.
            print(job_serializer)
            return Response(job_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

