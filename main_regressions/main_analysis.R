#
# Main analysis
#

rm(list=ls())
library(readxl)
library(readr)
library(sandwich)
library(lmtest)
library(stargazer)
library(fastDummies)

# read data
df <- read_csv("final_data.csv")
df <- df[df$Honors == 0,] # exclude honors

# factor vars
df$teacher <- as.factor(df$teacher)
df$Session <- as.factor(df$Session)
df$Year <- as.factor(df$Year)
df$Grader <- as.factor(df$Grader)

#
# Main ITT regressions for part 2 and part 3
#

reg2 <- lm(Part2Tot ~ GPTBase + GPTTutor + gpa_prev +
            teacher + Session + Grader + Year, data = df)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Part3Tot ~ GPTBase + GPTTutor + gpa_prev +
             teacher + Session + Grader + Year, data = df)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs

stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)

# 
# Regression dropping non-compliers (as reported by teachers/staff)
#

ind <- which((df$Class == "11S" & df$Session == 2) |
               (df$Class == "11S" & df$Session == 4) |
               (df$Class == "10A" & df$Session == 2) |
               (df$Class == "9J" & df$Session == 1) |
               (df$Class == "10B" & df$Session == 3))
df2 <- df[-ind,]

reg2 <- lm(Part2Tot ~ GPTBase + GPTTutor + gpa_prev + 
             teacher + Session + Grader + Year, data = df2)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Part3Tot ~ GPTBase + GPTTutor + gpa_prev + 
             teacher + Session + Grader + Year, data = df2)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs

stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)
rm(df2)


#
# Some robustness checks
#

# include survey vars (exclude chatgptuse since not collected at same time)
reg2 <- lm(Part2Tot ~ GPTBase + GPTTutor + gpa_prev + teacher + Session + Grader + Year +
            education_parent + n_household_members + n_household_children + class_enjoyment +
            class_participation_likelihood + n_weekday_study_hours + n_weekend_study_hours + math_hw_completion + 
            hw_help + private_tutorship + visit_training_center + female, data = df)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Part3Tot ~ GPTBase + GPTTutor + gpa_prev + teacher + Session + Grader + Year +
             education_parent + n_household_members + n_household_children + class_enjoyment +
             class_participation_likelihood + n_weekday_study_hours + n_weekend_study_hours + math_hw_completion + 
             hw_help + private_tutorship + visit_training_center + female, data = df)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs

stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)

# include honors students
df2 <- read_csv("final_data.csv")
df2$teacher <- as.factor(df2$teacher)
df2$Session <- as.factor(df2$Session)
df2$Year <- as.factor(df2$Year)
df2$Grader <- as.factor(df2$Grader)
reg2 <- lm(Part2Tot ~ GPTBase + GPTTutor + gpa_prev +
             teacher + Session + Grader + Year, data = df2)
se2 <- sqrt(diag(vcovCL(reg2, cluster = ~Class))) # get clustered SEs

reg3 <- lm(Part3Tot ~ GPTBase + GPTTutor + gpa_prev +
             teacher + Session + Grader + Year, data = df2)
se3 <- sqrt(diag(vcovCL(reg3, cluster = ~Class))) # get clustered SEs

stargazer(reg2, reg3, se = list(se2, se3), omit=c("teacher", "Session", "Grader", "Year", "Constant"), align = TRUE)
rm(df2)

# Pre-Registered T-tests
t.test(df[df$`Treatment arm`=="control",]$Part2Tot, df[df$`Treatment arm`=="vanilla",]$Part2Tot)
t.test(df[df$`Treatment arm`=="control",]$Part2Tot, df[df$`Treatment arm`=="augmented",]$Part2Tot)
t.test(df[df$`Treatment arm`=="vanilla",]$Part2Tot, df[df$`Treatment arm`=="augmented",]$Part2Tot)

t.test(df[df$`Treatment arm`=="control",]$Part3Tot, df[df$`Treatment arm`=="vanilla",]$Part3Tot)
t.test(df[df$`Treatment arm`=="control",]$Part3Tot, df[df$`Treatment arm`=="augmented",]$Part3Tot)
t.test(df[df$`Treatment arm`=="vanilla",]$Part3Tot, df[df$`Treatment arm`=="augmented",]$Part3Tot)


