from appraisal.models import Appraisal
import math
from django.db.models.aggregates import StdDev, Avg

def standardized_score(employee_id):
    queryset = Appraisal.objects.filter(fk_employee = employee_id) #get all the appraisals of an employee
    total_appraisers = 0
    total_score=0
    for query in queryset:
        #for an appraiser get average of the total_percentage_scores that appraiser gave to all the employees
        mean = Appraisal.objects.filter(fk_appraiser=query.fk_appraiser.id).aggregate(Avg('total_score_percentage'))['total_score_percentage__avg']
        #for an appraiser get standard deviation the total_percentage_scores that appraiser gave to all the employees
        std_dev = Appraisal.objects.filter(fk_appraiser=query.fk_appraiser.id).aggregate(StdDev('total_score_percentage'))['total_score_percentage__stddev']
        #standardized_score for that appraisal
        z_score = (query.total_score_percentage - mean)/std_dev
        #z_score to points out of 5
        standardised_score = .5 * (math.erf(z_score / 2 ** .5) + 1)*10/2
        
        total_appraisers+=1
        total_score+=standardised_score
        
        print(query.fk_appraiser.id, mean, std_dev, z_score)
    print(round(total_score/total_appraisers))



# def generate_raise(lb, ub, divisions, pay_grade_raise_ratio, performance_raise_ratio):
#     queryset = AppraisalResult.objects.all()
#       x = queryset.filter(compa_ratio__level__lte = , gte, standa_avg=)
#       for i in x:
#           i.current_salary*
#     for pay_grade in pay_grade_raise_ratio: