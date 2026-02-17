from io import StringIO

import numpy as np
import streamlit as st
from pandas import read_pickle
import streamlit.components.v1 as components
from pandas.io.formats import string
import json
import question_paper_model
import fileReader as fr
import time
from csv import writer
from datetime import datetime
import userBase as ub
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cosine_ranking as cr
if 'key' not in st.session_state:
    st.session_state.key = 0
#Sent as Time-QID-Explanation-RightAnswer-ChosenAnswer
Name=""
FileName=""
def page_switcher(page):
    st.session_state.runpage = page
def User_Login():

    title = st.text_input('Enter Username',"")
    #st.write('The current movie title is', title)
    global Name
    Name=title
    global FileName
    FileName=Name+".csv"
    FileName="userData/csvs/"+FileName
    # df = pd.read_csv(FileName)  # or pd.read_excel(filename) for xls file
    # if(df.empty):

    btn = st.button('Login', on_click=page_switcher, args=(page_homepage,))
# -----HOMEPAGE----
def page_homepage():
    if(st.session_state.key == 1):
        ub.readfiles()
        st.session_state.key=3

    st.session_state.count = 0
    st.title("JEE-T")
    st.subheader("Automated Practice Paper Generator System for the JEE")
    st.markdown("---")

    st.subheader("Welcome "+Name+",")
    st.write("Help us understand what you know")
    btn = st.button('Take the Diagnostic Test', on_click=page_switcher, args=(page_diagnostic_test,))
    st.text("")

    st.write("Time to apply what you've been learning?")
    btn = st.button('Take the Practice Test', on_click=page_switcher, args=(page_practice_test,))
    st.write("\n")

    st.write("Want to look at your journey so far?")
    btn = st.button('Visit Profile', on_click=page_switcher, args=(page_visit_profile,))

    if btn:
        st.experimental_rerun()  # rerun is needed to clear the page


# # -----TAKE THE DIAGNOSTIC TEST----
# if 'diagnostic_user_ans' not in st.session_state:
#     st.session_state.diagnostic_user_ans = []
#
# if 'diagnostic_correct_ans' not in st.session_state:
#     st.session_state.diagnostic_correct_ans = []
#
# if 'diagnostic_topic' not in st.session_state:
#     st.session_state.diagnostic_topic = []
#
# if 'topic' not in st.session_state:
#     st.session_state.topic = []
#
# if 'qid' not in st.session_state:
#     st.session_state.qid = []
#
# if 'time' not in st.session_state:
#     st.session_state.time = []


def page_diagnostic_test():
    home_btn = st.button('Home')
    if home_btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()

    st.title('The Diagnostic Test')
    st.write(
        'There are 30 questions from multiple topics to determine your weak and strong points so that we can cater the questions that we make to help you better.')

    btn1 = st.button('Start the test')

    if btn1:
        temp=[]

        start = datetime.now()
        temp.append(start)
        temp.append("---")
        temp.append("---")
        temp.append("---")
        temp.append("---")
        with open(FileName, 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer objectc
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(temp)

            # Close the file object
            f_object.close()
        st.session_state.runpage = page_diagnostic_test_questions
        st.experimental_rerun()

    st.session_state.count = 0  # everytime you come to the homepage the count is reset to 0


def page_diagnostic_test_questions():
    home_btn = st.button('Home')
    if home_btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()

    st.title('The Diagnostic Test')

    dataset = question_paper_model.Question()
    paper = dataset.practice_paper('easy',30)
    # st.write(paper)
    if (st.session_state.count < 30):
        print(paper)
        printQuestion(paper[st.session_state.count], st.session_state.count)
        st.session_state.count += 1
    else:
        st.session_state.runpage = page_done_diagnostic_test
        st.experimental_rerun()


def printQuestion(problem, i):
    start = datetime.now()
    List = []
    #List.append(Name)
    List.append(start)
    question = problem['question']
    if problem['answer'] == 'a' or problem['answer'] == 'A':
        answer = problem['options'][0]
    elif problem['answer'] == 'b' or problem['answer'] == 'B':
        answer = problem['options'][1]
    elif problem['answer'] == 'c' or problem['answer'] == 'C':
        answer = problem['options'][2]
    else:
        answer = problem['options'][3]

    #explanation = problem['explanation']
    options = problem['options']
    List.append(problem['ID'])
    print(problem)
    List.append(problem['domain'])
    List.append(problem['subdomain'])
    List.append(problem['explanation'])
    #st.write(problem['explanation'])
    List.append(problem['answer'])
    # List.append()
    st.write("#### Question " + str(i + 1))
    #st.markdown(question)
    #st.components.v1.html(question)

    # for i in options:
    #     st.components.v1.html(i)
    count=len(options)
    alpha = 'A'
    optionAlpha=[]
    for i in range(0, count):
        optionAlpha.append(alpha)
        alpha = chr(ord(alpha) + 1)

    temp=""
    temp=temp+question+"<br>"
    for i in range(len(options)):
        temp=temp+optionAlpha[i]+": "+str(options[i])+"<br>"
    st.components.v1.html(temp)
    QuestionDisplay = st.radio("",optionAlpha)
    # List=[6,'William',5532,1,'UAE']
    # List
    # Open our existing CSV file in append mode
    # Create a file object for this file

    btn = st.button('Next Question', key=i, on_click=tocsv(List, QuestionDisplay,problem))


def tocsv(List, QuestionDisplay,problem):
    #List.append(QuestionDisplay)
    if QuestionDisplay=='A':
        List.append('a')
    elif QuestionDisplay=='B':
        List.append('b')
    elif QuestionDisplay=='C':
        List.append('c')
    elif QuestionDisplay=='D':
        List.append('d')

    with open(FileName, 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer objectc
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()


def readFile(filename):
    file = open(filename)
    temp = file.read()
    testlist = temp.split('END')
    #print(testlist)
    # Removing last entry that is blank
    #testlist.pop()

    cols = ['time', 'qid', 'domain', 'subdomain', 'qtext', 'correct', 'chosen','options']
    colstring = ''
    for i in cols:
        colstring += i + ','
    colstring += '\n'

    for i in range(len(testlist)):
        data = testlist[i]
        dfstring = colstring + data
        dfdata = StringIO(dfstring)
        df = pd.DataFrame()
        df = pd.read_csv(dfdata, sep=',')
        df = df.drop(df.columns[-1], axis=1)
        #st = df['time'][0]
        #df.drop(0, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # preprocess each test df
        testlist[i] = preprocess(df)
    fulldata = pd.concat(testlist)
    #print("HERE")
    #print(fulldata)
    fulldata.reset_index(drop=True, inplace=True)

    return fulldata

def preprocess(df):

    acc = []
    for i in range(df.shape[0]):
        if (df.loc[i]['correct'] == df.iloc[i]['chosen']):
            acc.append(1)
        else:
            acc.append(0)
    df['accuracy'] = acc

    diff = np.zeros(len(df))
    return df

def page_done_diagnostic_test():
    st.session_state.key = 1
    with open(FileName, 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object

        # Pass the list as an argument into
        # the writerow()
        f_object.write("END\n")

        # Close the file object
        f_object.close()

    st.title('Diagnostic Test is Over')
    df=readFile(FileName)
    #print(df)
    df2=df[df['accuracy']!=0]
    st.write("You answered ", len(df2), "questions correctly.")
    st.write("You answered ", 30-len(df2), "questions wrong.")
    #st.write("Your wrong answers were : ")
    df2 = df[df['accuracy'] == 0]

    #print(df2)
    # df2['qtext']
    # df2['correct']
    df = pd.read_csv('IRdata2.csv').drop(['imageURL'], axis=1)
    df["QID"] = "CH" + df["QID"].map(str)

    st.subheader("Questions you answered wrong")
    #st.write(df2)
    #st.write(df)
    temp = df.loc[df['QID'] == df2.iloc[1]['qid']]
    #st.write(temp)
    for i in range(len(df2)):
        if(df2.iloc[i]['qid']!="---"):
            temp = df.loc[df['QID'] == df2.iloc[i]['qid']]
            #st.write(temp)
            #st.write(temp['question'])
            Question = "Question: " + temp['question'].values[0]
            #st.write(Question)
            ind = ord(df2.iloc[i]['correct']) - 97
            temp2 = temp['options'].values.tolist()[0].strip('][').split(', ')
            temp2 = temp2[ind].replace("'", "")
            #st.write(temp2)
            answer = "Answer: " + temp2
            #st.write(answer)
            explanation = "Explanation: " + temp['explaination'].values.tolist()[0]
            #st.write(explanation)
            st.components.v1.html(Question + "<br>" +"<br>" + answer + "<br>" + "<br>" + explanation)

    btn = st.button('Return Home')
    if btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()  # rerun is needed to clear the page

def page_done_practice_test():
    ub.readfiles()
    with open(FileName, 'a') as f_object:

        f_object.write("END\n")

        # Close the file object
        f_object.close()

    st.title('Practice Test is Over')

    file1 = open('LevelAndQuestions.txt', 'r')
    line = file1.readline()
    file1.close()
    x = line.split("-")
    Questions=int(x[1])


    temp = fr.reader()
    temp.read(FileName)
    df = temp.fulldf
    print(df)
    df = df.tail(Questions)
    #st.write("NON PICKLED")
    #st.write(df)

    df2 = df[df['accuracy'] == 0]

    right = df[df['accuracy'] == 1]

    st.write("You answered ", len(right), "questions correctly.")
    st.write("You answered ", Questions-len(right), "questions wrong.")

    df = pd.read_csv('IRdata2.csv').drop(['imageURL'], axis=1)
    df["QID"] = "CH" + df["QID"].map(str)

    #df = read_pickle('current.pkl')
    # df = pd.read_csv("current.csv")
    #paper=df.to_dict('records')

    #st.write(paper)
    #st.write("PICKLED")
    temp2=[]
    for x in df2:
        if(x=='qid'):
            temp2=df2[x].values

    #st.write(temp2)
    print(temp2)
    properlist=[]
    for i in temp2:
        #st.write(i)
        properlist.append(i)
    #print(properlist)
    final=""
    st.subheader("Questions that you have answered wrongly")
    st.subheader("---")
    for i in range(len(df)):
        if(df.iloc[i]['QID'] in properlist):
            print("GOING IN ")

            #st.write(paper[i]['ID'])
            temp = df.iloc[i]
            st.subheader("Question:")
            Question =temp['question']
            qtn=temp['question']
            dmn=temp['domain']
            sdmn=temp['subdomain']

            query=qtn+" "+dmn+" "+sdmn
            #function(query)

            ind = ord(temp['answer']) - 97
            #st.write("hello")
            #st.write(temp)
            temp2 = temp['options'].strip('][').split(', ')
            #st.write(temp2)
            temp2 = temp2[ind].replace("'", "")
            #st.write(temp2)
            #st.write(temp2)

            dr = cr.documentRetriever()
            dr.retrieve(query, 3)

                #st.markdown("Relevant [link](%s)" % url)
        # st.write(temp2)
            answer = "Answer: " + temp2
            explanation = "Explanation: " + temp['explaination']
            final=Question + "<br>" + answer + "<br>" + "<br>" + explanation
            st.components.v1.html(final)
            st.subheader("Materials that might help with the question ")
            a,b,c=st.columns(3)
            a.write("1st")
            b.write("2nd")
            c.write("3rd")
            count=1
            for i in dr.newdf['link']:
                url=i
                if(count==1):
                    a.markdown("Relevant [link](%s)" % url)
                if (count == 2):
                    b.markdown("Relevant [link](%s)" % url)
                if (count == 1):
                    c.markdown("Relevant [link](%s)" % url)
                count+=1
            #call function
    btn = st.button('Return Home')
    if btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()  # rerun is needed to clear the page
# -----TAKE THE PRACTICE TEST----

def page_practice_test():
    st.title('Practice Test')
    st.write('This practice test will be made according to you.')

    btn = st.button('Next', on_click=page_switcher, args=(page3,))
    if btn:
        st.experimental_rerun()  # rerun is needed to clear the page

    btn = st.button('Back')
    if btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()


def choices():
    st.title('Select the Subject')
    Subject = st.radio(
        "What subject do you wanna practice",
        ('Chemistry', 'Mathematics', 'Physics'))
    if Subject == 'Chemistry':
        st.write('You selected Chemistry.')
    elif Subject == 'Mathematics':
        st.write('You selected Mathematics.')
    elif Subject == 'Physics':
        st.write('You selected Physics.')

    # Questions = st.number_input('Pick the number of questions you want to practice:',min_value=10,max_value=100,step=1)
    # st.write('You have chosen ', Questions ,'questions')
    Questions = st.slider("Pick the number of questions you would like", 20, 60, 20)
    #Questions=40

    st.write("You have chosen ", Questions, 'questions')
    Level = st.radio(
        "What level of questions do you wanna practice",
        ('easy', 'medium', 'hard'))
    #st.write("You have chosen ", Level, 'questions')
    # options = st.multiselect(
    #     "Select the topics you want to do the test on ",
    #     ['1', '2', '3', '4', '5'],
    #     ['1'])

    if st.button('Start'):
        start = datetime.now()
        temp=[]
        temp.append(start)
        temp.append("---")
        temp.append("---")
        temp.append("---")
        temp.append("---")
        with open(FileName, 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer objectc
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(temp)

            # Close the file object
            f_object.close()
        with open('LevelAndQuestions.txt', 'w') as f:
            f.write(Level)
            f.write('-')
            f.write(str(Questions))
            f.close()
        print("Crashing Here")
        paper = question_paper_model.make_paper(Level, Questions, Name)
        print("Crashing Heressssss")
        #print(paper)
        df=pd.DataFrame(paper)
        # df.to_csv('current.csv', index=False)
        df.to_pickle('current.pkl')
        #print("CALLING PRACTICE TEST")
        st.session_state.runpage = page_practice_test_questions
        st.experimental_rerun()




def page_practice_test_questions():
    #print("STARTED")
    home_btn = st.button('Home')
    if home_btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()

    file1 = open('LevelAndQuestions.txt', 'r')
    line = file1.readline()
    file1.close()
    x = line.split("-")
    Level=x[0]
    Questions=int(x[1])
    st.title('The Practice Test')
    # with open('LevelAndQuestions.txt', 'r') as f:
    #dataset = question_paper_model.Question()
    #print("REQUESTING")
    df = read_pickle('current.pkl')
    # df = pd.read_csv("current.csv")
    paper=df.to_dict('records')
    #print(paper)
    #print(paper)
    # paper = question_paper_model.make_paper(Level,Questions,Name)
    # print(paper)
    # st.write(paper)
    #print(paper)
    #print(st.session_state.count)
    if (st.session_state.count < Questions):
        printQuestion(paper[st.session_state.count], st.session_state.count)
        #print("UPDATING STATE COUNT")
        st.session_state.count += 1
    else:
        st.session_state.runpage = page_done_practice_test
        st.experimental_rerun()




def page3():
    st.write(choices())
    # st.write('You selected:', options)
    btn = st.button('Back')
    if btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()


# -----VISIT PROFILE----
def page_visit_profile():
    #Time taken in each question
    #Correct
    #Wrong

    st.header("Hello, "+Name)

    temp=fr.reader()
    temp.read(FileName)
    df=temp.fulldf
    print(df)

    #Time=[]


    df2 = df[df['accuracy'] != 0]
    fig1, ax1 = plt.subplots()
    y = np.array([len(df2), len(df) - len(df2)])
    mexplode = (0, 0.3)
    ax1.pie(y, labels=['Correct','Wrong'],explode=mexplode,shadow = True)

    #ax1.axis('equal')
    # plt.pie(y)
    # plt.show()

    #plt.pie(y)
    st.subheader("Total Questions")
    st.pyplot(fig1)
    # st.pyplot(fig)



    #st.area_chart(data)

    #st.area_chart(df2)
    #prin(df)
    wrong,right = st.columns(2)

    #print(len(df))
    wrong.write("Wrong")
    right.write("Correct")
    wrong.subheader(len(df)-len(df2))
    #st.write("Right")
    right.subheader(len(df2))
    # st.bar_chart(my_dataframe)


    df2=df[['time']]
    #st.write(df2)
    st.subheader("Time taken per Question")
    st.write("Time in Seconds per Question")
    #st.area_chart(df2)
    data=pd.DataFrame(df2,np.arange(len(df2)))
    # st.bar_chart(data)
    # st.line_chart(data)
    #st.write("THIS IS DATAAA")
    #print("HASDKLASD")
    #print(data)
    #st.write(data)
    st.area_chart(data)
    #st.line_chart(data)
    a, b, c = st.columns(3)
    b.write("Question Number")


    st.subheader("Subject-wise Problems Solved")
    phy, chem, math = st.columns(3)
    phy.write("**Physics**")
    phy.subheader(0)
    phy.subheader(0)
    chem.write("**Chemistry**")
    #st.markdown("""Wrong""")
    df2 = df[df['accuracy'] != 0]
    chem.subheader(len(df)-len(df2))
    #st.write("Right")
    chem.subheader(len(df2))
    math.write("**Maths**")
    math.subheader(0)
    math.subheader(0)

    df=pd.read_csv('userData/users/users.csv')
    df2=df[df.username == Name]
    st.subheader("Performance Review")
    strong, weak = st.columns(2)
    strong.write("***Strong areas***")
    for i in df2.strong_areas:
        j=i.split("'")
        for a in j:
            if(a=='[' or a==']' or a=="'" or a==", "):
                continue
            else:
                strong.write(a)



        #st.write(i)

    weak.write("***Weak areas***")
    for i in df2.weak_areas:

        j = i.split("'")
        for a in j:
            if (a == '[' or a == ']' or a == "'" or a==", "):
                continue
            else:
                #print(a)
                weak.write(a)
    f = open('userData/jsons/'+Name+'.json')

    data = json.load(f)
    print("JSON")
    print(data)
    # Iterating through the json
    # list
    st.subheader("Subdomain classification :")
    #st.write("Subdomain classification : ")
    easy, medium, hard = st.columns(3)
    easy.write("Easy")
    medium.write("Medium")
    hard.write("Hard")
    for i in data['easy']:
        easy.write(i[1])
    for i in data['medium']:
        medium.write(i[1])
    for i in data['hard']:
        hard.write(i[1])

    # Closing file
    f.close()
    btn = st.button('Back')
    if btn:
        st.session_state.runpage = page_homepage
        st.experimental_rerun()


if __name__ == '__main__':
    if 'runpage' not in st.session_state:
        st.session_state.runpage = User_Login
    st.session_state.runpage()

# difficulty level
# Number of questions
# topic
