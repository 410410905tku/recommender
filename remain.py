import mysql.connector
import pandas as pd
import gui
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyQt6.QtCore import pyqtSignal
import re

def send_result_to_gui(result):
    gui.display_result(result)

def start_processing():
    try:
        # MySQL 連接設定
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Miles19900907@",
            database="recommender"
        )

        # 教授歷史課程記錄
        query = "SELECT * FROM merged_data"
        professor_history = pd.read_sql(query, conn)

        # 轉換文本為數值表示
        vectorizer = TfidfVectorizer(stop_words='english')  
        tfidf_matrix = vectorizer.fit_transform(professor_history['Sub_Name'])

        # 調整 TF-IDF 權重
        # 創建一個字典來記錄每個課程的出現次數
        course_counts = {}
        for course in professor_history['Sub_Name']:
            course_counts[course] = course_counts.get(course, 0) + 1
    
        # 根據出現次數調整 TF-IDF 權重
        for i, course in enumerate(vectorizer.get_feature_names_out()):
            if course in course_counts:
                # 如果課程出現多次，將其 TF-IDF 權重除以其出現次數的平方根
                tfidf_matrix[:, i] /= course_counts[course] ** 0.5

        # 輸入指定教授姓名
        target_professor_chinese_name = gui.input_text

        # 使用正則表達式找到符合輸入中文姓名的教授記錄
        target_professor_pattern = re.escape(target_professor_chinese_name)
        target_records = professor_history[professor_history['Teacher'].str.contains(target_professor_pattern)]

        if not target_records.empty:
            target_index = target_records.index[0]
        
            similarity_matrix = cosine_similarity(tfidf_matrix, dense_output=False)

            similarity_scores = similarity_matrix[:, target_index].toarray().flatten()
            sorted_indices = similarity_scores.argsort()[::-1]

            # 紀錄課程(出現過的)
            recommended_courses = set()

            # 紀錄前五名相似度最高的教授名稱
            similar_professors = []

            for index in sorted_indices:
                professor_name = professor_history.iloc[index]['Teacher']
                if professor_name not in similar_professors:
                    similar_professors.append(professor_name)
                    courses_by_professor = professor_history[professor_history['Teacher'] == professor_name]['Sub_Name']
                
                    #加入並排除目標教授已經教授過的課程
                    for course in courses_by_professor:
                        if course not in professor_history.loc[target_index, 'Sub_Name']:
                            recommended_courses.add(course)

                    #如果相似教授名稱已經達到5個，則停止迴圈
                    if len(similar_professors) >= 5:
                        break

            print(f"Top 5 similar professors for professor {target_professor_chinese_name}:")
            for i, professor in enumerate(similar_professors, 1):
                print(f"{i}. {professor}")

            print(f"\nTop recommended courses for professor {target_professor_chinese_name}:")
        
            # 計算目標教授與推薦課程的相似度並排序
            target_courses_tfidf = tfidf_matrix[target_index]
            course_similarity_scores = cosine_similarity(tfidf_matrix, target_courses_tfidf)
            sorted_course_indices = course_similarity_scores.flatten().argsort()[::-1]

            # 限制前10個
            output_count = 0
            recommended_professors = set()  
            recommended_courses_chinese= []
            recommended_courses_english= []
            result_matrix = []
            for index in sorted_course_indices:
                if output_count >= 10:
                    break
                course_name = professor_history.iloc[index]['Sub_Name']
                professor_name = professor_history.iloc[index]['Teacher']
                if course_name in recommended_courses and professor_name not in recommended_professors:
                    chinese, english = course_name.split('\n')
                    recommended_courses_chinese.append(chinese)
                    recommended_courses_english.append(english)
                    result_matrix.append(recommended_courses_chinese)
                    print(recommended_courses_chinese) 
                    result_matrix.append(recommended_courses_english)
                    print(recommended_courses_english)
                    recommended_courses_chinese= []
                    recommended_courses_english= [] 
                    recommended_courses.remove(course_name) 
                    recommended_professors.add(professor_name)
                    output_count += 1
            gui.display_result(result_matrix)    
        else:
            print(f"找不到教授 {target_professor_chinese_name} 的歷史記錄")
            gui.show_error_message1(target_professor_chinese_name)

    except Exception as e:
        print("發生錯誤：", e)
        gui.show_error_message2(e)

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
