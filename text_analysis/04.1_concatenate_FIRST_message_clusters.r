library(tidyverse)
library(testit)
library(openxlsx)
library(quanteda)

# Set your root directory
setwd() # set your root directory here

# Load data
clean_unreadable_code = function(input, list_of_unreadable_patterns){
  for (pattern in list_of_unreadable_patterns){
    input = gsub(pattern,
                 '',
                 input)
  }
  return(input)
}

# Get first message clusters
file_list = list.files('data/first_message_cluster_by_arm_grade')
# Create a empty excel workbook
list_of_unreadable_patterns = c('nuffdn',
                                'uffdn',
                                'nufffdn',
                                'ufffdn',
                                '&quot;',
                                'nn',
                                'u2005',
                                'u200a',
                                "\\’,")

total_tab = list()


for (filename in file_list){
  
  data = read.csv(paste0("data/first_message_cluster_by_arm_grade/", filename))
  
  # ===================================================
  # Create topic - representative_doc mapping
  # ===================================================
  # Note the desired column is repdoc, not Representative_Docs
  topic_repdoc = data[,c('Topic', 'most_rep_doc')] %>% unique()
  # Parse the representative doc string
  repdoc_list = strsplit(topic_repdoc$most_rep_doc, split = "', '")
  # Choose the longest representative doc
  longest_rep_doc = unlist(lapply(repdoc_list, 
                                  function(a) a[1]))
  longest_rep_doc = gsub("\\[", '', longest_rep_doc)
  longest_rep_doc = gsub("\\]", '', longest_rep_doc)
  
  assert(length(longest_rep_doc) == nrow(topic_repdoc))
  
  topic_repdoc$repdoc = longest_rep_doc
  topic_repdoc$Topic = as.character(topic_repdoc$Topic)
  
  # ===================================================
  # Create topic - count  mapping
  # ===================================================
  
  topic_count = data.frame(table(data$Topic))
  colnames(topic_count) = c('topic', 'count')
  topic_count$topic = as.character(topic_count$topic)
  
  # =============
  # Merge
  # =============
  topic_count_repdoc = topic_count %>% inner_join(
    topic_repdoc, by = c('topic' = 'Topic'))
  
  # ==========
  # Summarize
  # ==========
  # Step 1: delete -1
  no_indetermined = topic_count_repdoc %>% filter(topic != -1)
  # Step 2: calculate %
  no_indetermined$prop = round(
    no_indetermined$count / sum(no_indetermined$count), 2)
  
  result = no_indetermined[,c('count', 'prop', 'repdoc')]
  
  # sort
  result = result %>% arrange(desc(prop))
  
  result$repdoc = clean_unreadable_code(result$repdoc,
                                        list_of_unreadable_patterns)
  
  # Write excel by sheet
  # Add sheets to the workbook
  not_needed = substring(filename, 1, 28)
  sheet_name = gsub('.csv', '',
      gsub(not_needed, '', filename))
  # print(paste(sheet_name, filename))

  # Save a 'total' tab
  group_info = unlist(strsplit(sheet_name, '_'))
  
  result$treatment = group_info[1]
  result$session_id = group_info[2]
  #print(paste(group_info[2], filename))
  result$grade = group_info[3]
  result$question_id = group_info[4]
  result$topic = seq(1, nrow(result))
  
  # convert to lowercase
  result$repdoc = tolower(result$repdoc)

  # Delete topic with count == 0
  result_clean = result %>% filter(count != 0)
  
  # Add an empty line for better visualization
  result_clean = rbind(result_clean, NA)  
  
  total_tab[[filename]] = result_clean
  
}

# Final Clean
total_df = do.call(rbind, lapply(total_tab, as.data.frame))
rownames(total_df) = NULL
total_df = total_df[, c('treatment', 
                        'session_id',
                        'grade',
                        'question_id',
                        'topic', 
                        'count', 
                        'prop', 
                        'repdoc'
                        #'included_topic'
                        )] %>% 
  arrange('treatment', 
            'session_id', 
            'grade', 
            'question_id', 
            'topic')

# Save
write.csv(total_df, file = "results/top_messages_by_arm_question_s1_4_first_messages_final.csv")
