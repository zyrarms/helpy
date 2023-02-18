import pickle
import sklearn
from sanitybot.models import User_health
from flask_login import login_required, current_user
from sanitybot import db
from sanitybot.models import User
from datetime import datetime
from docx import Document
import docx
from io import BytesIO
from datetime import datetime

with open(r'sanitybot\pickles\ppd_decisiontree.pkl', 'rb') as f:
    decisionTree_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_naiveBayes.pkl', 'rb') as f:
    naiveBayes_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_svm.pkl', 'rb') as f:
    svm_model = pickle.load(f)


def pdd_prediction(input_list):
    pred_result = svm_model.predict([input_list])[0]
    print(pred_result)

    user = current_user
    user = User.query.filter_by(id=user.id).first()
    user.epds_score = int(pred_result)
    user.date_submitted = datetime.now()
    # health = User_health(firstname=user.firstname, middlename=user.middlename,
    #                      lastname=user.lastname, address=user.address, contact=user.contact, condition=int(pred_result))
    # db.session.add(health)
    ppd = ""
    epds_class = ""
    if (pred_result) == 0:
        ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Depression not likely” or the depression itself is not likely detectable. That's good news for you. Please continue to support and take care of yourself to have a more positive life after you give birth."""
        epds_class = "Depression not likely"
    elif (pred_result) == 1:
        ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Depression possible” or some postpartum depression is slightly present. Mild depression involves more than just feeling blue temporarily. These symptoms can go on for days and are noticeable enough to interfere with your usual activities."""
        epds_class = "Depression possible"
    elif (pred_result) == 2:
        ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Fairly high possibility of depression” or more symptoms are noticeable. Moderate and mild depression share similar symptoms, the greatest difference is that the symptoms of moderate depression are severe enough to cause problems at home and work."""
        epds_class = "Fairly high possibility of depression"
    elif (pred_result) == 3:
        ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Probable depression” or most of the postpartum depression symptoms are obviously noticeable. Severe (major) depression is classified as having the symptoms of mild to moderate depression, but the symptoms are severe and noticeable, even to your loved ones. Episodes of major depression last an average of six months or longer. Diagnosis is especially crucial in severe depression, and it may even be time-sensitive."""
        epds_class = "Probable depression"
    else:
        ppd = 'Nothing'

    data = {
        "id": str(user.id),
        "firstname": f"{user.firstname} {user.middlename} {user.lastname}",
        "email": user.email,
        "address": user.address,
        "date_submitted": str(user.date_submitted), 
        "epds_score": epds_class,
        "questions": ["QUESTIONS", "Have you been able to laugh and see the funny side of things?", "Have you looked forward with enjoyment to things?", "Do you blame yourself unnecessarily when things go wrong?", "Have you been anxious or worried for no good reason?", "Have you felt scared or panicky for no very good reason?", "Have things been getting on top of you?", "Have you been so unhappy that you have had difficulty sleeping?", "Have you felt sad or miserable?", "Have you been so unhappy that you have been crying?", "Has the thought of harming yourself occurred to you?", "EPDS Score"],
        "message": ppd.replace("Thankyou for answering my initial assessment. ", "")
    }

    table = ["Have you been able to laugh and see the funny side of things?", "Have you looked forward with enjoyment to things?", "Do you blame yourself unnecessarily when things go wrong?", "Have you been anxious or worried for no good reason?", "Have you felt scared or panicky for no very good reason?",
             "Have things been getting on top of you?", "Have you been so unhappy that you have had difficulty sleeping?", "Have you felt sad or miserable?", "Have you been so unhappy that you have been crying?", "Has the thought of harming yourself occurred to you?"]

    epds = [
        {
            "ANSWER": "",
            0: "As much as I always could",
            1: "Not quite so much now",
            2: "Definitely not so much now",
            3: "Hardly at all",
        },
        {
            "question": "Have you been able to laugh and see the funny side of things?",
            0: "As much as I always could",
            1: "Not quite so much now",
            2: "Definitely not so much now",
            3: "Hardly at all",
        },
        {
            "question": "Have you looked forward with enjoyment to things?",
            0: "As much as I ever did",
            1: "Rather less than I used to",
            2: "Definitely less than I used to",
            3: "Hardly at all",
        },
        {
            "question": "Do you blame yourself unnecessarily when things go wrong?",
            3: "Yes, most of the time",
            2: "Yes, some of the time",
            1: "Not very often",
            0: "No, Never",
        },
        {
            "question": "Have you been anxious or worried for no good reason?",
            0: "No, not at all",
            1: "Hardly ever",
            2: "Yes, sometimes",
            3: "Yes, very often",
        },
        {
            "question": "Have you felt scared or panicky for no very good reason?",
            3: "Yes, quite a lot",
            2: "Yes, sometimes",
            1: "No, not much",
            0: "No, not at all",
        },
        {
            "question": "Have things been getting on top of you?",
            3: "Yes, most of the time I haven't been able to cope",
            2: "Yes, sometimes I haven't been coping as well as usual",
            1: "No, most of the time I have coped quite well",
            0: "No, I have been coping as well as ever",
        },
        {
            "question": "Have you been so unhappy that you have had difficulty sleeping?",
            3: "Yes, most of the time",
            2: "Yes, sometimes",
            1: "Not very often",
            0: "No, not at all",
        },
        {
            "question": "Have you felt sad or miserable?",
            3: "Yes, most of the time",
            2: "Yes, quite often",
            1: "Not very often",
            0: "No, not at all",
        },
        {
            "question": "Have you been so unhappy that you have been crying?",
            3: "Yes, most of the time",
            2: "Yes, quite often",
            1: "Only occasionally",
            0: "No, never",
        },
        {
            "question": "Has the thought of harming yourself occurred to you?",
            3: "Yes, quite often",
            2: "Sometimes",
            1: "Hardly ever",
            0: "Never",
        },
        {
            "question": "Has the thought of harming yourself occurred to you?",
            3: "Yes, quite often",
            2: "Sometimes",
            1: "Hardly ever",
            0: "Never",
        },
    ]

    document = Document()

    table = document.add_table(rows=2, cols=3)
    table.style = 'Table Grid'

    datas = ["id", "firstname", "email",
             "address", "date_submitted", "epds_score"]

    table.cell(0, 0).text = data['id']
    table.cell(0, 1).text = data['firstname']
    table.cell(0, 2).text = data["email"]
    table.cell(1, 0).text = data["address"]
    table.cell(1, 1).text = data["date_submitted"]
    table.cell(1, 2).text = data["epds_score"]

    document.add_paragraph()

    # Add a table to the document with 2 columns
    table = document.add_table(rows=len(data['questions']), cols=2)
    table.style = 'Table Grid'

    # Access the cells of the first row
    input_list.insert(0, "ANSWER")
    for index, value in enumerate(data['questions']):
        cell_1 = table.cell(index, 0)
        cell_2 = table.cell(index, 1)

        # Add text to the cells
        cell_1.text = value
        cell_2.text = f"({input_list[index]}) {epds[index][input_list[index] if input_list[index] in [0,1,2,3,4] else 0]}"
        if index==0:
          cell_2.text = "ANSWER"
        elif index==11:
          cell_2.text = f"{input_list[index]}"

    # table.paragraph_format.space_after = 1

    p = document.add_paragraph(data["message"])
    p.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.JUSTIFY


    table = document.add_table(rows=6, cols=3)
    table.style = 'Table Grid'
    table.cell(0, 0).text = "EPDS Score"
    table.cell(0, 1).text = "Interpretation"
    table.cell(0, 2).text = "Action"

    table.cell(1, 0).text = "0–6"
    table.cell(1, 1).text = "Depression not likely"
    table.cell(1, 2).text = "Continue support"
    table.cell(2, 0).text = "7–13"
    table.cell(2, 1).text = "Depression possible"
    table.cell(2, 2).text = "Support, re-screen in 2–4 weeks. Consider referral to primary care provide(PCP)."
    table.cell(3, 0).text = "14–19"
    table.cell(3, 1).text = "Fairly high possibility of depression"
    table.cell(3, 2).text = "Monitor, support and offer education. Refer to PCP."
    table.cell(4, 0).text = "19–30"
    table.cell(4, 1).text = "Probable depression"
    table.cell(4, 2).text = "Diagnostic assessment and treatment by PCP and/or specialist."
    table.cell(5, 0).text = "Positive score (1, 2 or 3) on question 10 (suicidality risk)"
    table.cell(5, 1).text = ""
    table.cell(5, 2).text = "Immediate referral is necessary for assessment of suicidal ideation. This is to ensure proper intervention and to consider factors such as plan, history, symptoms, and potential harm."

    # temp_file = BytesIO()
    # document.save(temp_file)
    # temp_file.seek(0)

    new_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.docx"
    # user.file = Content(temp_file.read(), save=True)
    # user.file = temp_file
    # user.file.url

    document.save('demo.docx')
    db.session.commit()

    response = {}

    return ppd
