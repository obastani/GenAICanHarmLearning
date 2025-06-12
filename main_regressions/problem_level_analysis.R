#
# Problem analysis
#

rm(list=ls())
library(readxl)
library(readr)
library(sandwich)
library(lmtest)
library(stargazer)
library(fastDummies)

# read in dataset
df2 <- read_csv("problem_part2.csv")
df3 <- read_csv("problem_part3.csv")

# factor vars
df2$teacher <- as.factor(df2$teacher)
df2$Session <- as.factor(df2$Session)
df2$Year <- as.factor(df2$Year)
df2$Grader <- as.factor(df2$Grader)
df3$teacher <- as.factor(df3$teacher)
df3$Session <- as.factor(df3$Session)
df3$Year <- as.factor(df3$Year)
df3$Grader <- as.factor(df3$Grader)

# drop honors
df2 <- df2[df2$Honors == 0,]
df3 <- df3[df3$Honors == 0,]

#
# Main ITT regressions for part 2 and part 3
#

reg2 <- lm(Score ~ GPTBase + GPTTutor + gpa_prev +
             teacher + Session + Grader + Year, data = df2)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Score ~ GPTBase + GPTTutor + gpa_prev +
             teacher + Session + Grader + Year, data = df3)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs

stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)


#
# Part 2 performance in each arm as a fn of GPT Base error rates
#

# add vanilla logical/arithmetic error rates
gpt <- read_csv("gpt_answers_full.csv", show_col_types=FALSE)
gpt <- gpt[c("problem", "total_correct", "logical_errors", "arithmetic_errors")]
gpt$total_correct <- gpt$total_correct/10 # normalize by # of attempts to get error rates
gpt$logical_errors <- gpt$logical_errors/10
gpt$arithmetic_errors <- gpt$arithmetic_errors/10
df2 <- merge(df2, gpt, by.x="Problem", by.y="problem")


#
# Corresponding problem Part 3 performance in each arm as a fn of Part 2 GPT Base error rates
#

# add corresponding part 3 problem (note all part 3 problems have a match but there are unmatched part 2 problems)
problem <- read_csv("problem_mapping.csv", show_col_types=FALSE)
df <- merge(problem, df3, by.x="part3", by.y="Problem", all.x=FALSE, all.y=FALSE)
df <- merge(df, df2[c("Problem", "Student ID", "logical_errors", "arithmetic_errors")], 
            by.x=c("Student ID", "part2"), by.y=c("Student ID", "Problem"), all.x=FALSE, all.y=FALSE)

# part 2 & part 3 with interaction terms
reg2 <- lm(Score ~ logical_errors * GPTBase + logical_errors * GPTTutor +
             arithmetic_errors * GPTBase + arithmetic_errors * GPTTutor +
             gpa_prev + teacher + Session + Grader + Year, data = df2)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Score ~ logical_errors * GPTBase + logical_errors * GPTTutor +
             arithmetic_errors * GPTBase + arithmetic_errors * GPTTutor +
             gpa_prev + teacher + Session + Grader + Year, data = df)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs
stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)


