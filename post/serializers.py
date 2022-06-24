from rest_framework import serializers
from post.models import Company as CompanyModel
from post.models import JobPost as JobPostModel
from post.models import JobPostSkillSet as JobPostSkillSetModel
from post.models import BusinessArea as BusinessAreaModel



class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = ["company_name", "business_area"]
        


class JobPostSerializer(serializers.ModelSerializer):
    job_type = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    
    def get_jobtype(self, obj):
        return obj.job_type.job_type
    
    def get_company(self, obj):
        return obj.company_name.company_name
    
    class Meta:
        model = JobPostModel
        fields = ["job_type", "company_name", "job_description", "salary", "created_at"]
            
            
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    skill_sets = serializers.SerializerMethodField(read_only=True)
    job_post = serializers.SerializerMethodField(read_only=True)
    # (read_only=True)
    
    def get_skill_set(self, obj):
        return obj.skill_set.name
    
    def get_job_post(self, obj):
        return obj.job_post.job_type
    
    class Meta:
        model = JobPostSkillSetModel
        fields = ["skill_set", "job_post"]