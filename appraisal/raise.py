'''
{
    market_salary: float
    current_salary: float
    fk_emp: id
    standard_score: z-score average
    compa-ratio: curent_salary/market_salary

}
'''



import math

def percentage_of_area_under_std_normal_curve_from_zcore(z_score):
    return .5 * (math.erf(z_score / 2 ** .5) + 1)*10/2

print(percentage_of_area_under_std_normal_curve_from_zcore(0))