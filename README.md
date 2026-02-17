# JEE-T : Automated Practice Paper Generator System for the JEE

## Problem Statement

JEE aspirants waste a lot of time deciding which questions to solve from the vast number of resources they use for preparation. If the questions are not selected carefully, they may not be able to give the weaker areas more attention and repeat questions. It is also challenging and time consuming to find relevant information to learn the concepts used in the question they attempted incorrectly.

## Files

1. IRdata2.csv - Dataset File containing features - QID, domain, subdomain, question, imageURL, options, answer and explanation.
2. IRdata_Resource.csv - Dataset file containing relevant resources to study chemistry concepts
3. IRdata_classifier - Dataset containing text from NCERT Chemistry class 12 textbook
4. app.py - code file for our StreamLit Application.
5. question_paper_model.py - code file for our question paper model.
6. userBase.py - code file for user analysis model.
7. difficulty.py - model for deciding difficulty of domain/question.

## How to use the app

1. Clone the repo

```
git clone https://github.com/samikshamodi/JEE-T.git
```

2. Go the directory
3. Create a virtual env

```
python -m venv streamlit-env
```

4. Activate virtual env
   - Mac
   ```
   source streamlit-env/bin/activate
   ```

   - Windows
   ```
   streamlit-env\Scripts\activate
   ```
5. Install the requirements

```
pip install requirements.txt
```

6. Run the app

```
streamlit run app.py
```
