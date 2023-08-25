import streamlit as st
import pandas as pd
def calculate_gpa(data, search_term):
    data.dropna(inplace=True)
    data = data[data['Subname'] != 'ENVIRONMENTAL SCIENCE']
    
    column_name = 'Htno'
    search_results = data[data[column_name].str.contains(search_term)]

    grade_map = {'A+': 10.0, 'A': 9.0, 'B': 8.0, 'C': 7.0, 'D': 6.0, 'E': 5.0, 'F': 0.0}
    
    new_data = search_results
    new_data.loc[:, 'Numeric_Grade'] = new_data['Grade'].map(grade_map)
    backlog=0
    for F in new_data['Grade'].values:
        if F == 'F':  # Increment backlog count if grade is 'F'
            backlog += 1

    data1 = new_data.copy()
    data1['Total'] = data1['Credits'] * data1['Numeric_Grade']
    data2 = data1.copy()
    sum_credits_x_grade = data2['Total'].sum()
    total_credits = data2['Credits'].sum()
    gpa = None
    if backlog == 0:
        gpa = sum_credits_x_grade / total_credits
        gpa = round(gpa, 2)
        st.write("Your GPA is:", gpa)
    else:
        gpa = None
        st.write("You have a backlog")
        st.write("baclogs :",backlog)
        st.write(" Work hard YOU CAN DO IT! ")
    return gpa, search_results
st.title('GPA Calculator')
st.write('Please upload the file with the grades data')
cgpa_data = []
uploaded_file = st.file_uploader('Choose a file', key="fileUploader")
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    search_term = st.text_input('Enter a search term')
    if st.button('Calculate GPA'):
        gpa, search_results = calculate_gpa(data, search_term)
        if gpa is not None:
            cgpa_data.append(gpa)
            st.write('Search results:')
            st.write(search_results)
            st.write('GPA:', gpa)
            st.write('CGPA:', round(sum(cgpa_data) / len(cgpa_data), 2))
        else:
            st.write(search_results)
    if st.button('Clear Data'):
        cgpa_data = []
        st.write('CGPA Data Cleared')