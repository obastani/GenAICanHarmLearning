** SETUP
*ssc install regdhfe



*************************************************************************************
*
*					Classroom-level Grade Dispersion
*
*************************************************************************************	


use df_class.dta,clear 


local replace replace
foreach var in Part2Tot Part3Tot{
		reghdfe `var' GPTBase GPTTutor gpa_prev, absorb(teacher Grader Year Session) vce(cluster Class)
		quietly outreg2 using reg_hhi.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)  
		local replace
		}		
		

		
*************************************************************************************
*
*					Attendance
*
*************************************************************************************	


use df_attendance.dta, clear


tab Attendance

local replace replace
reghdfe Attendance GPTBase GPTTutor gpa_prev i.Session, absorb(teacher Grader Year) vce(cluster Class)
quietly outreg2 using reg_attendance.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev i.Session)  



		
*************************************************************************************
*
*					Student Perception
*
*************************************************************************************	


/*
## Perception questions

1.	How much do you think you learned from this whole class session?
[ ] Nothing at all [ ] A little [ ] Moderately [ ] Quite a lot [ ] A great deal

2.	How well do you think you performed in this quiz?
[ ] Very poorly [ ] Below average [ ] Average [ ] Above average [ ] Excellent

3.	How much time did it take you to solve the questions in this quiz?
[ ] 0-5 min [ ] 5-10 min [ ] 10-15 min [ ] 15-20 min [ ] 20-25 min [ ] 25-30 min

4.	How useful was the problem-solving session in the previous part (Part 2) in helping you solve the questions in this quiz?
[ ] Ineffective [ ] Somewhat ineffective [ ] Neutral [ ] Somewhat effective [ ] Effective

5.	How many minutes would you be willing to give up on this quiz to have the help of the TED-AI Training Engine (or ChatGPT-4 if you haven't used the TED-AI Training Engine)?
[ ] 0-5 min [ ] 5-10 min [ ] 10-15 min [ ] 15-20 min [ ] 20-25 min [ ] 25-30 min

*/

use df_perception.dta, clear

*Generate categorical vars for grader and teacher
encode teacher, gen(teacher_fe)
encode Grader, gen(grader_fe)

** Fix variable structures 

* Perceived Learning
gen perceived_learning_num = .
replace perceived_learning_num = 5 if perceived_learning == "A great deal"
replace perceived_learning_num = 4 if perceived_learning == "Quite a lot"
replace perceived_learning_num = 3 if perceived_learning == "Moderately"
replace perceived_learning_num = 2 if perceived_learning == "A little"
replace perceived_learning_num = 1 if perceived_learning == "Nothing at all"
* Convert to categorical variables
label define perceived_learning_labels ///
    5 "A great deal" ///
    4 "Quite a lot" ///
    3 "Moderately" ///
    2 "A little" ///
    1 "Nothing at all"
* Apply the labels
label values perceived_learning_num perceived_learning_labels
* Drop the original string variable and rename the numeric one
drop perceived_learning
rename perceived_learning_num perceived_learning


*Perceived Learning
gen perceived_performance_num = .
replace perceived_performance_num = 5 if perceived_performance == "Excellent"
replace perceived_performance_num = 4 if perceived_performance == "Above Average"
replace perceived_performance_num = 3 if perceived_performance == "Average"
replace perceived_performance_num = 2 if perceived_performance == "Below Average"
replace perceived_performance_num = 1 if perceived_performance == "Very Poorly"
* Convert to categorical variables
label define perceived_performance_labels ///
    5 "Excellent" ///
    4 "Above Average" ///
    3 "Average" ///
    2 "Below Average" ///
    1 "Very Poorly"
* Apply the labels
label values perceived_performance_num perceived_performance_labels
* Drop the original string variable
drop perceived_performance
* Rename the numeric variable to the original variable name
rename perceived_performance_num perceived_performance



*Perceived Value Practising
gen perceived_practice_num = .
replace perceived_practice_num = 5 if perceived_value_practise == "Effective"
replace perceived_practice_num = 4 if perceived_value_practise == "Somewhat effective"
replace perceived_practice_num = 3 if perceived_value_practise == "Neutral"
replace perceived_practice_num = 2 if perceived_value_practise == "Somewhat ineffective"
replace perceived_practice_num = 1 if perceived_value_practise == "Ineffective"
* Convert to categorical variables
label define perceived_value_practice_labels ///
    5 "Effective" ///
    4 "Somewhat effective" ///
    3 "Neutral" ///
    2 "Somewhat ineffective" ///
    1 "Ineffective"
* Apply the labels
label values perceived_practice_num perceived_value_practice_labels
* Drop the original string variable
drop perceived_value_practise
* Rename the numeric variable to the original variable name
rename perceived_practice_num perceived_value_practise



*Exam Duration
gen exam_dur = real(exam_duration)


*Time Trade-off
gen time_trade = real(time_tradeoff)




* Regressions
local replace replace	
	oprobit perceived_learning  GPTBase GPTTutor gpa_prev i.Session i.Year i.teacher_fe i.grader_fe, robust
	quietly outreg2 using reg_perception.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)
local replace
	oprobit perceived_performance  GPTBase GPTTutor gpa_prev i.Session i.Year i.teacher_fe i.grader_fe, robust
	quietly outreg2 using reg_perception.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)
local replace
	oprobit perceived_value_practise  GPTBase GPTTutor gpa_prev i.Session i.Year i.teacher_fe i.grader_fe, robust
	quietly outreg2 using reg_perception.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)
local replace
	reghdfe exam_dur GPTBase GPTTutor gpa_prev i.Session, absorb(teacher Grader Year) vce(cluster Class)
	quietly outreg2 using reg_perception.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)
local replace
	reghdfe time_trade GPTBase GPTTutor gpa_prev i.Session, absorb(teacher Grader Year) vce(cluster Class)
	quietly outreg2 using reg_perception.tex, `replace' ctitle("`var'") keep (GPTBase GPTTutor gpa_prev)  

	
	

*************************************************************************************
*
*					Heterogeneity: Past GPA
*
*************************************************************************************	



import delimited final_data.csv, clear
drop if honors ==1
rename gpa_prev gpa
gen gpa_prev = real(gpa)
drop gpa
drop if honors ==1



sum gpa_prev, detail
gen gpa_binary = gpa_prev> .837418 // median prev gpa


	
	
local replace replace
	
		foreach var in part2tot part3tot {   
			
			reghdfe `var' gptbase##gpa_binary gpttutor##gpa_binary gpa_prev , absorb(teacher grader session year) vce(cluster class)
			quietly outreg2 using reg_het_gpa.tex, `replace' ctitle("`var'") 
			local replace
				
}
	
	
*************************************************************************************
*
*					Heterogeneity: Private Tutoring
*
*************************************************************************************	



import delimited final_data.csv, clear
drop if honors ==1
rename gpa_prev gpa
gen gpa_prev = real(gpa)
drop gpa





local replace replace
	forval bin=0/1{
			foreach var in part2tot part3tot {   
				
				reghdfe `var' gptbase gpttutor gpa_prev if (private_tutorship == `bin'), absorb(teacher grader session year) vce(cluster class)
				quietly outreg2 using reg_het_pvttutor.tex, `replace' ctitle("`var'") keep (gptbase gpttutor gpa_prev)
				local replace
				}		
	}
	
	
local replace replace

		foreach var in part2tot part3tot {   
			
			reghdfe `var' gptbase##private_tutorship gpttutor##private_tutorship gpa_prev, absorb(teacher grader session year) vce(cluster class)
			quietly outreg2 using reg_het_pvttutor.tex, `replace' ctitle("`var'") 
			local replace
			}		
	
	
	
*************************************************************************************
*
*					Heterogeneity: Hours Spent Studying
*
*************************************************************************************	


import delimited final_data.csv, clear
drop if honors ==1
rename gpa_prev gpa
gen gpa_prev = real(gpa)
drop gpa


gen hours_spent_studying = (2*n_weekend_study_hours + 5*n_weekday_study_hours)/7
sum hours_spent_studying, detail
gen study_binary = hours_spent_studying>  1.642857   // median daily study hours


local replace replace
	forval bin=0/1{
			foreach var in part2tot part3tot {   
				
				reghdfe `var' gptbase gpttutor gpa_prev if (study_binary == `bin'), absorb(teacher grader session year) vce(cluster class)
				quietly outreg2 using reg_het_studyhrs.tex, `replace' ctitle("`var'") keep (gptbase gpttutor gpa_prev)
				local replace
				}		
	}
	

	
	
	
local replace replace
	
			foreach var in part2tot part3tot {   
				
				reghdfe `var' gptbase##study_binary gpttutor##study_binary gpa_prev, absorb(teacher grader session year) vce(cluster class)
				quietly outreg2 using reg_het_studyhrs.tex, `replace' ctitle("`var'") 
				local replace
				}		
	
	

		