# Data and Code for "Generative AI without guardrails can harm learning: Evidence from high school mathematics"

This repo shares code and data that are used in the paper "Generative AI Without Guardrails Can Harm Learning: Evidence from High School Mathematics".

## Folders

1. `main regressions/` - Contains R scripts and some additional data files needed for the main analyses in the paper and some robustness checks.
2. `additional results/` - Contains Python and Stata scripts and some additional data files needed for analyses related to covariate balance, student perception, heterogeneous treatment effects, student performance dispersion, and student absenteeism.
3. `text analysis/` - Contains scripts and data files needed for our analysis of student messages and GPT error rates, as well as its own readme.md file.
4. `final_data.csv` - Contains the main dataset generated from our study.

## Data Dictionary

##### `final_data.csv`, `main regressions/problem_part3.csv`, `main regressions/problem_part2.csv`, and `additional results/final_data.csv`

| Column                                           | Description                                                                           |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| `Student_ID`                                     | Unique identifier for each student                                                    |
| `Class`                                          | Class identifier                                                                      |
| `Year`                                           | Academic year                                                                         |
| `Session`                                        | The experiment session identifier                                                     |
| `Grader`                                         | Grader identifier                                                                     |
| `Part2Tot`                                       | Part 2 student score                                                                  |
| `Part3Tot`                                       | Part 3 student score                                                                  |
| `Survey_Q1`–`Survey_Q5`                          | Responses to survey questions                                                         |
| `gpa_prev`                                       | Previous GPA of the student                                                           |
| `GPTBase`, `GPTTutor`                            | Indicators for treatment assignment                                                   |
| `teacher`                                        | Teacher identifier                                                                    |
| `n_household_members`                            | Number of members in the household                                                    |
| `class_enjoyment`                                | Self-reported student sentiment                                                       |
| `class_participation_likelihood`                 | Self-reported student participation                                                   |
| `n_weekday_study_hours`, `n_weekend_study_hours` | Self-Reported study hours on weekdays and weekends                                    |
| `math_hw_completion`                             | Homework completion                                                                   |
| `hw_help`                                        | Indicator of whether the student receives help for homework                           |
| `private_tutorship`, `visit_training_center`     | Indicator of whether the student receives private tutorship or visits training center |
| `chatgpt_use`                                    | Self-reported indicator of whether the student has previous experience with ChatGPT   |
| `Treatment_arm`                                  | Treatment assignment                                                                  |
| `female`                                         | Gender indicator                                                                      |
| `education_parent`                               | Parental education                                                                    |
| `n_household_children`                           | Number of children in household                                                       |
| `Honors`                                         | Honors class participation indicator                                                  |

##### `main regressions/problem_mapping.csv`

| Column         | Description                            |
| -------------- | -------------------------------------- |
| `part2, part3` | Mappings of Part 2 and Part 3 problems |

##### `main regressions/gpt_answers_full.csv`

| Column              | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `problem`           | Problem identifier                                    |
| `0–9`               | Ten GPT responses to the same problem                 |
| `g0–g9`             | Correctness labels of the corresponding GPT responses |
| `total_correct`     | Number of correct answers                             |
| `logical_errors`    | Number of answers that make logic errors              |
| `arithmetic_errors` | Number of answers that make arithmetic errors         |

##### `text analysis/data/raw/valid_student_data.csv` and `text analysis/data/raw/valid_student_data_w_time_stamp.csv`

| Column            | Description                                 |
| ----------------- | ------------------------------------------- |
| `role`            | Role of the message sender (student or GPT) |
| `message`         | Actual message content                      |
| `conversation_id` | Unique identifier for conversation          |
| `username`        | Student identifier                          |
| `grade`           | Grade                                       |
| `problem_id`      | Problem identifier                          |
| `session_id`      | Experiment session identifier               |
| `time_stamp`      | Timestamp of the message                    |
| `treatment`       | Treatment assignment                        |

##### `text analysis/data/raw/question_list.csv`

| Column       | Description        |
| ------------ | ------------------ |
| `session`    | Experiment session |
| `grade`      | Grade              |
| `problem_id` | Problem identifier |
| `question`   | Problem text       |
| `answers`    | Empty              |

##### `additional results/df_attendance.dta`

| Column                           | Description                                         |
| -------------------------------- | --------------------------------------------------- |
| `Student_ID`                     | Unique identifier for each student                  |
| `Session`                        | Experiment session                                  |
| `Class`                          | Class                                               |
| `Year`                           | Academic year                                       |
| `Grader`                         | Grader identifier                                   |
| `Part2Tot`                       | Part 2 score                                        |
| `Part3Tot`                       | Part 3 score                                        |
| `Survey_Q1` to `Survey_Q5`       | Survey responses (Q1–Q5)                            |
| `gpa_prev`                       | Previous GPA                                        |
| `GPTBase`, `GPTTutor`            | Treatment assignment                                |
| `teacher`                        | Teacher identifier                                  |
| `n_household_members`            | Number of household members                         |
| `class_enjoyment`                | Self-reported class enjoyment                       |
| `class_participation_likelihood` | Self-reported class participation                   |
| `n_weekday_study_hours`          | Weekday study hours                                 |
| `n_weekend_study_hours`          | Weekend study hours                                 |
| `math_hw_completion`             | Math homework completion indicator                  |
| `hw_help`                        | Help with homework indicator                        |
| `private_tutorship`              | Private tutoring indicator                          |
| `visit_training_center`          | Visits to training center indicator                 |
| `chatgpt_use`                    | Indicator of previous use of ChatGPT                |
| `Treatment_arm`                  | Treatment assignment, same as `GPTBase`, `GPTTutor` |
| `female`                         | Gender indicator                                    |
| `education_parent`               | Parent education level                              |
| `n_household_children`           | Number of children in household                     |
| `Honors`                         | Honors student indicator                            |
| `Attendance`                     | Attendance record                                   |
| `Session_class`                  | Combined session-class identifier                   |

##### `additional results/df_class.dta`

| Column     | Description                |
| ---------- | -------------------------- |
| `Class`    | Class identifier           |
| `Session`  | Session number             |
| `Part2Tot` | Average Part 2 total score |
| `Part3Tot` | Average Part 3 total score |
| `GPTBase`  | Average GPT base score     |
| `GPTTutor` | Average GPT tutor score    |
| `gpa_prev` | Average previous GPA       |
| `teacher`  | Teacher identifier         |
| `Grader`   | Grader identifier          |
| `Year`     | Academic year              |

##### `additional results/df_perception.dta`

| Column                           | Description                                             |
| -------------------------------- | ------------------------------------------------------- |
| `Student_ID`                     | Unique identifier for each student                      |
| `Class`                          | Class identifier                                        |
| `Year`                           | Academic year                                           |
| `Session`                        | Experiment session                                      |
| `Grader`                         | Grader identifier                                       |
| `Part2Tot`                       | Part 2 score                                            |
| `Part3Tot`                       | Part 3 score                                            |
| `perceived_learning`             | Student's perceived learning                            |
| `perceived_performance`          | Student's perceived performance                         |
| `exam_duration`                  | Total exam duration                                     |
| `perceived_value_practise`       | Perceived value of the practice                         |
| `time_tradeoff`                  | Time trade-off                                          |
| `gpa_prev`                       | Previous GPA                                            |
| `GPTBase`, `GPTTutor`            | Treatment assignment                                    |
| `teacher`                        | Teacher identifier                                      |
| `n_household_members`            | Number of household members                             |
| `class_enjoyment`                | Self-reported class enjoyment level                     |
| `class_participation_likelihood` | Self-reported class participation                       |
| `n_weekday_study_hours`          | Weekday study hours                                     |
| `n_weekend_study_hours`          | Weekend study hours                                     |
| `math_hw_completion`             | Math homework completion                                |
| `hw_help`                        | Help with homework indicator                            |
| `private_tutorship`              | Private tutoring indicator                              |
| `visit_training_center`          | Visits to training center indicator                     |
| `chatgpt_use`                    | Indicator of previous ChatGPT use                       |
| `Treatment_arm`                  | Treatment assignment. The same as `GPTBase`, `GPTTutor` |
| `female`                         | Gender indicator                                        |
| `education_parent`               | Parent education level                                  |
| `n_household_children`           | Number of children in household                         |
| `Honors`                         | Honors student indicator                                |


## Other Potential Use

The data could be used to train or benchmark educational AI models. It provides a basis for understanding how student interactions with AI systems correlate with learning outcomes, aiding in the design of more effective educational AI.


## Citing Our Work

If you use our scripts or data, please cite the our paper.

```
@article{bastani2025generative,
  title={Generative AI without guardrails can harm learning: Evidence from high school mathematics},
  author={Bastani, Hamsa and Bastani, Osbert and Sungu, Alp and Ge, Haosen and Kabakc{\i}, Ozge and Mariman, Rei},
  journal={PNAS},
 year={(Forthcoming)}
}
```
