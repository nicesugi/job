from multiprocessing.dummy import JoinableQueue
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
        print(">>>>>", request.GET.get('skills', ''))
        print(">>>>>", request.POST.get('skills', ''))
        print(">>>>>", request.data)
        
        print("1", request.data)
        # print("3", request.query) > 안나옴 포스트맨에서 파라미터로 보내기때문
        print("4", request.query_params)
        print("5", request.query_params.getlist('skills', ''))
        skills = request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills) #skills = ['django', 'mysql']

        """
        Encapsulate filters as objects (that can then be combined logically) 
        (using`&` and `|`)
             ㅠㅠ 필터를 오브젝트로 캡슐화- > 객체지향..클ㄹㅐ스로 묶고 그걸 아래를 써서 combined 한다.?
        캡슐화란 데이터와 코드의 형태를 외부로부터 알 수 없게하고, 데이터의 구조와 역할, 기능을 하나의 캡슐형태로 만드는 방법이다.
        캡슐화의 중요한 목적은 변수를 private로 선언하여 데이터를 보호하고, 보호된 변수는 getter나 setter등의 메서드를 통해서만 간접적으로 접근을 허용하는 것 이다.
        캡슐화를 하면 불필요한 정보를 감출 수 있기 때문에, 정보은닉을 할 수 있다는 특징이 있다.
        캡슐화와 정보은닉은 동일한 개념은 아니다.
        <class 'django.db.models.query_utils.Q'> 
        print(type(Q)) #class 'type' 

        """

        query = Q()
        print(query)
        print(type(query))
        for skill in skills:
            query.add(Q(skill_set__name=skill), Q.OR)

        job_skills = JobPostSkillSet.objects.filter(query)

        job_posts = JobPost.objects.filter(
            id__in=[job_skill.job_post.id for job_skill in job_skills]
        )

        if job_posts.exists():
            serializer = JobPostSerializer(job_posts, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)



class JobView(APIView):
    """
     # request 1)
    {
        "job_type": 1,
        "company_name": "sparta1",
        "job_description": "django drf ninja sql",
        "salary": 30000000
    }
    """
    def post(self, request):
        print(f'request.data: {request.data}')
        print(type(request.data.get("job_type", None)))
        job_type = int( request.data.get("job_type", None) ) # int안써도 int..인데 음?
        company_name = request.data.get("company_name", None)
        print(type(job_type))
        print(company_name)
        job = JobType.objects.filter(id=job_type)
        company = Company.objects.filter(company_name=company_name)
        print("ㅡㅡㅡㅡㅡㅡ>", job)
        print("ㅡㅡㅡㅡㅡㅡ>", company)
        if not job.exists():
            return Response({"message": "해당하는 job_type이 존재하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)


        if not company.exists():
            company = Company(company_name=company_name).save()
            return Response({"message": "회사를 등록하여 공고 등록하였다"}, status=status.HTTP_200_OK)
        else:
            print(type(company)) # 왜 첫번째요소를 선택하는지? 
            company = company.first()
            
        # request.data.pop('job_type', None)
        job_serializer = JobPostSerializer(data=request.data)
        if job_serializer.is_valid():
            job_serializer.save(company=company, job_type=job.first())
            return Response(status=status.HTTP_200_OK)

        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    """
     # request 2)
    {
        "job_type": "permanent",
        "company_name": "sparta2",
        "job_description": "django drf ninja sql",
        "salary": 30000000
    }
    """
        

