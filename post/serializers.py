from rest_framework import serializers

# from post.models import SkillSet as SkillSetModel
from post.models import JobPostSkillSet as JobPostSkillSetModel
# from post.models import JobType as JobTypeModel
from post.models import JobPost as JobPostModel
from post.models import Company as CompanyModel
# from post.models import CompanyBusinessArea as CompanyBusinessAreaModel
# from post.models import BusinessArea as BusinessAreaModel

        

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = ["id", "company_name"]
        


class JobPostSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    position_type = serializers.SerializerMethodField()
    skill_sets = serializers.SerializerMethodField()
    
    
    def get_position_type(self, obj):
        return obj.job_type.job_type
    
    
    def get_skill_sets(self, obj):
        # print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ>>ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(obj.jobpostskillset_set.all()) # jobpostskillset or skillset 둘다 사용 가능
        # print(type(obj.jobpostskillset_set.all()))        
        # print([i.skill_set.name for i in obj.jobpostskillset_set.all()])
        # print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ<<ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        return [i.skill_set.name for i in obj.jobpostskillset_set.all()]
    class Meta:
        model = JobPostModel
        fields = ["id", "position_type", "company", "job_description", "salary", "skill_sets"]
            
            
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer(read_only=True) #안에 skill_set내용도 있기 때문에 따로 작성안함
    
    class Meta:
        model = JobPostSkillSetModel
        fields = ["id", "skill_set", "job_post"]