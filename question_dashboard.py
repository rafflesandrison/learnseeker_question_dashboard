import json
from re import sub
import numpy as np
import pandas as pd

data_breakdown_file = open('math_breakdown.json')
data_breakdown = json.load(data_breakdown_file)

uuids_with_issues = []

p1_whole_numbers_easy_uuids = ""
p1_whole_numbers_normal_uuids = ""

with open('math_new.txt', 'r', encoding='utf-8') as math_questions:
    questions = json.load(math_questions)["data"]["questions"]
    
    count = 0
    for question in questions:
        uuid = question["uuid"]
        question_type = question["type"]
        subject = question["subject"][0]
        specialisation = question["specialisation"][0] if len(question["specialisation"]) > 0 else "None"
        level = question["level"][0]
        topic_name = question["topics"][0]
        subtopic_name = question["subtopics"][0] if len(question["subtopics"]) > 0 else ""
        difficultyLevel = question["difficultyLevel"][0] if len(question["difficultyLevel"]) > 0 else ""

        mcqs = data_breakdown[question_type]

        # Incrementing count
        if (level == "Primary 1" or level == "Primary 2" or level == "Primary 3" or level == "Primary 4" or level == "Primary 5" or level == "Primary 6"):
            mcq_topics = mcqs[level]["specialisation"][specialisation]["topics"]
            
            try:
                if len(topic_name) > 0 and topic_name in mcq_topics:
                    mcq_topics[topic_name]["question_count"] = mcq_topics[topic_name]["question_count"] + 1
                    mcq_topics[topic_name]["difficulty_1"] = mcq_topics[topic_name]["difficulty_1"] + 1 if difficultyLevel == "1" else mcq_topics[topic_name]["difficulty_1"]
                    mcq_topics[topic_name]["difficulty_2"] = mcq_topics[topic_name]["difficulty_2"] + 1 if difficultyLevel == "2" else mcq_topics[topic_name]["difficulty_2"]
                    mcq_topics[topic_name]["difficulty_3"] = mcq_topics[topic_name]["difficulty_3"] + 1 if difficultyLevel == "3" else mcq_topics[topic_name]["difficulty_3"]
                
                if len(subtopic_name) > 0 and topic_name in mcq_topics and subtopic_name in mcq_topics[topic_name]["subtopics"]:
                    print(topic_name)
                    print(subtopic_name)
                    mcq_topics[topic_name]["subtopics"][subtopic_name]["question_count"] = mcq_topics[topic_name]["subtopics"][subtopic_name]["question_count"] + 1
                    mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_1"] = mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_1"] + 1 if difficultyLevel == "1" else mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_1"]
                    mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_2"] = mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_2"] + 1 if difficultyLevel == "2" else mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_2"]
                    mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_3"] = mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_3"] + 1 if difficultyLevel == "3" else mcq_topics[topic_name]["subtopics"][subtopic_name]["difficulty_3"]
            except:
                uuids_with_issues.append("UUID = " + uuid + " ;\tlevel = " + level + " ;\ttopic=" + topic_name + " ;\tsubtopic = " + subtopic_name + " ;\tdifficultyLevel = " + difficultyLevel)

for uuid in uuids_with_issues:
    print(uuid)

## Topic Breakdown for all levels
df_master = pd.DataFrame()

academic_level_list = []
specialisation_list = []
topic_list = []
topic_question_count_list = []
topic_difficulty_1_question_count_list = []
topic_difficulty_2_question_count_list = []
topic_difficulty_3_question_count_list = []

subtopic_list = []
subtopic_question_count_list = []
subtopic_difficulty_1_question_count_list = []
subtopic_difficulty_2_question_count_list = []
subtopic_difficulty_3_question_count_list = []

for academic_level in data_breakdown["MCQ"].keys():
    for specialisation_name in data_breakdown["MCQ"][academic_level]["specialisation"].keys():
        for topic_name in data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"].keys():
        
            topic_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["question_count"]
            topic_difficulty_1_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["difficulty_1"]
            topic_difficulty_2_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["difficulty_2"]
            topic_difficulty_3_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["difficulty_3"]
            
            for subtopic_name in data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["subtopics"]:
                subtopic_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["subtopics"][subtopic_name]["question_count"]
                subtopic_difficulty_1_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["subtopics"][subtopic_name]["difficulty_1"]
                subtopic_difficulty_2_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["subtopics"][subtopic_name]["difficulty_2"]
                subtopic_difficulty_3_question_count = data_breakdown["MCQ"][academic_level]["specialisation"][specialisation_name]["topics"][topic_name]["subtopics"][subtopic_name]["difficulty_3"]

                # TODO: Create a data-frame here that comprise of all topic and subtopics
                academic_level_list.append(academic_level)
                specialisation_list.append(specialisation_name)

                topic_list.append(topic_name)
                topic_question_count_list.append(topic_question_count)
                topic_difficulty_1_question_count_list.append(topic_difficulty_1_question_count)
                topic_difficulty_2_question_count_list.append(topic_difficulty_2_question_count)
                topic_difficulty_3_question_count_list.append(topic_difficulty_3_question_count)

                subtopic_list.append(subtopic_name)
                subtopic_question_count_list.append(subtopic_question_count)
                subtopic_difficulty_1_question_count_list.append(subtopic_difficulty_1_question_count)
                subtopic_difficulty_2_question_count_list.append(subtopic_difficulty_2_question_count)
                subtopic_difficulty_3_question_count_list.append(subtopic_difficulty_3_question_count)

df_master["Academic Level"] = academic_level_list
df_master["Specialisation"] = specialisation_list
df_master["Topic"] = topic_list
df_master["Topic Question Count"] = topic_question_count_list
df_master["Topic Difficulty 1 Question Count"] = topic_difficulty_1_question_count_list
df_master["Topic Difficulty 2 Question Count"] = topic_difficulty_2_question_count_list
df_master["Topic Difficulty 3 Question Count"] = topic_difficulty_3_question_count_list

df_master["Subtopic"] = subtopic_list
df_master["Subtopic Question Count"] = subtopic_question_count_list
df_master["Subtopic Difficulty 1 Question Count"] = subtopic_difficulty_1_question_count_list
df_master["Subtopic Difficulty 2 Question Count"] = subtopic_difficulty_2_question_count_list
df_master["Subtopic Difficulty 3 Question Count"] = subtopic_difficulty_3_question_count_list

print(df_master)
df_master.to_excel('math_content_breakdown.xlsx', sheet_name='Master')

data_breakdown_file.close()