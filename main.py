import streamlit as st
import question_paper_model
#print("HELLO")
import time

Count=0
Q="What is your name"
A='A'
Options=['A', 'Bas', 'C','D']
Explanation="THIS IS THE EXPLANATION"

def page_switcher(page):
    st.session_state.runpage = page


def main():
    # global Count
    # Count=1
    # global UserRight,UserWrong
    # UserRight=0
    # UserWrong=0
    # st.title('main')
    st.write("Welcome User1123")
    st.write("""
# HOMEPAGE
""")

    btn = st.button('Diagnostic Test', on_click=page_switcher, args=(page1,))
    btn = st.button('Practice Test', on_click=page_switcher, args=(Practice_Test,))
    btn = st.button('Visit Profile', on_click=page_switcher, args=(page_visit_profile,))
    if btn:
        st.experimental_rerun()  # rerun is needed to clear the page


def page1():
    st.title('The Diagnostic Test')
    st.write(
        'There are 20 questions from multiple topics to determine your weak and strong points so that we can cater the questions that we make to help you better')
    btn1 = st.button('Start')
    if btn1:
        st.session_state.runpage = Qpage
        st.experimental_rerun()
    btn = st.button('Back')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()


if 'count' not in st.session_state:
    st.session_state.count=1

if 'diagnostic_user_ans' not in st.session_state:
    st.session_state.diagnostic_user_ans=[]

if 'diagnostic_correct_ans' not in st.session_state:
    st.session_state.diagnostic_correct_ans=[]

if 'diagnostic_topic' not in st.session_state:
    st.session_state.diagnostic_topic=[]

if 'topic' not in st.session_state:
    st.session_state.topic=[]

if 'qid' not in st.session_state:
    st.session_state.qid=[]

if 'time' not in st.session_state:
    st.session_state.time=[]

if 'rightorwrong' not in st.session_state:
    st.session_state.rightorwrong=[]

def Qpage():
    #st.write("TOTAL RIGHT ANSWERS")
    #st.write(UserRight)
    # global Count
    # if(Count<5):
    #     question(Q, A, Options,Explanation)
    # else:
    #     st.session_state.runpage = DoneDiagnostic()
    #     st.experimental_rerun()
    dataset = question_paper_model.Question()
    paper = dataset.generatepaper(64)
    
    if(st.session_state.count<=20):
        question(paper[st.session_state.count-1],st.session_state.count)
        st.session_state.count+=1
    else:
        st.session_state.runpage = DoneDiagnostic
        st.experimental_rerun()

    btn = st.button('Back')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()

def DoneDiagnostic():
    st.title('Diagnostic Test is Over')

    l1 = st.session_state.diagnostic_user_ans
    l2 = st.session_state.diagnostic_correct_ans

    cnt =0
    for i in range(len(l1)):
        if l1[i]==l2[i]:
            cnt+=1
    
    st.write("You answered ",cnt, "questions correctly.")
    st.write("You answered ",20-cnt, "questions wrong.")

    btn = st.button('Return Home')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()  # rerun is needed to clear the page

def Practice_Test():
    st.title('Practice Test')
    st.write('This practice test will be made according to you.')

    btn = st.button('Next', on_click=page_switcher, args=(page3,))
    if btn:
        st.experimental_rerun()  # rerun is needed to clear the page

    btn = st.button('Back')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()

def choices():
    st.title('Select the Subject')
    Subject = st.radio(
        "What subject do you wanna practice",
        ('Physics', 'Mathematics', 'Chemistry'))
    if Subject == 'Chemistry':
        st.write('You selected Chemistry.')
    elif Subject == 'Mathematics':
        st.write('You selected Mathematics.')
    elif Subject == 'Physics':
        st.write('You selected Physics.')

    # Questions = st.number_input('Pick the number of questions you want to practice:',min_value=10,max_value=100,step=1)
    # st.write('You have chosen ', Questions ,'questions')
    Questions = st.slider("Pick the number of questions you would like", 0, 100, 25)
    st.write("You have chosen ", Questions, 'questions')
    options = st.multiselect(
        "Select the topics you want to do the test on ",
        ['1', '2', '3', '4','5'],
        ['1'])
    btn = st.button('Done')
    if btn:
        return Subject,Questions,options

def question(paper_que,i):
    #st.write(paper[0])
    #st.write(paper[0]['options'][0])
   
    #st.title(Question)
    start = time.time()

    Question= paper_que['question']
    if paper_que['answer'] =='a' or paper_que['answer'] =='A':
        Answer= paper_que['options'][0]
    elif paper_que['answer'] =='b' or paper_que['answer'] =='B':
        Answer= paper_que['options'][1]
    elif paper_que['answer'] =='c' or paper_que['answer'] =='C':
        Answer= paper_que['options'][2]
    else: 
        Answer= paper_que['options'][3]
        
    Explanation = paper_que['explanation']
    Options = paper_que['options']

    QuestionDisplay = st.radio(
    str(i)+"  "+Question,
    (Options))

    btn = st.button('Next Question',key=i)
    if btn:
        done = time.time()
        st.session_state.diagnostic_user_ans.append(QuestionDisplay)
        st.session_state.diagnostic_correct_ans.append(Answer)
        if QuestionDisplay == Answer:
            st.write('You are right. Move on to the next question')
            QuestionDisplay=""
            st.write(done-start)

        else:
            st.write('Wrong Answer, The Right answer is: ',Answer)
            #UserWrong+=1
            st.write("Explanation : ",Explanation)
            QuestionDisplay = ""
            st.write(done-start)



def page3():
    st.write(choices())
    #st.write('You selected:', options)
    btn = st.button('Back')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()


def page_visit_profile():
    st.header("Hello, User1123")
    st.subheader("Total Problems Solved")
    st.markdown("""---""")
    #st.bar_chart(my_dataframe)

    st.subheader("Subject-wise Problems Solved")
    phy, chem, math = st.columns(3)
    phy.write("Physics")
    chem.write("Chemistry")
    math.write("Maths")
    st.markdown("""---""")

    st.subheader("Performance Review")
    st.write("Strong areas")
    st.write("Weak areas")

    btn = st.button('Back')
    if btn:
        st.session_state.runpage = main
        st.experimental_rerun()



if __name__ == '__main__':
    if 'runpage' not in st.session_state:
        st.session_state.runpage = main
    st.session_state.runpage()

#difficulty level
#Number of questions
#topic