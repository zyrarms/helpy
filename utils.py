import pickle
import sklearn
from sanitybot.models import 

with open(r'sanitybot\pickles\ppd_decisiontree.pkl', 'rb') as f:
    decisionTree_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_naiveBayes.pkl', 'rb') as f:
    naiveBayes_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_svm.pkl', 'rb') as f:
    svm_model = pickle.load(f)

def pdd_prediction(list):
  pred_result = svm_model.predict([list])[0]
  #TODO save data in the database

  if pred_result == 0:
    ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “None or Minimal Postpartum Depression” or the depression itself is not likely detectable. That's good news for you. Please continue to support and take care of yourself to have a more positive life after you give birth."""
  elif pred_result == 1:
    ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Mild Postpartum Depression” or some postpartum depression is slightly present. Mild depression involves more than just feeling blue temporarily. These symptoms can go on for days and are noticeable enough to interfere with your usual activities."""
  elif pred_result == 2:
    ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Moderate Postpartum Depression” or more symptoms are noticeable. Moderate and mild depression share similar symptoms, the greatest difference is that the symptoms of moderate depression are severe enough to cause problems at home and work."""
  elif pred_result == 3:
    ppd = """Thankyou for answering my initial assessment. Based on your answers, you have “Severe Postpartum Depression” or most of the postpartum depression symptoms are obviously noticeable. Severe (major) depression is classified as having the symptoms of mild to moderate depression, but the symptoms are severe and noticeable, even to your loved ones. Episodes of major depression last an average of six months or longer. Diagnosis is especially crucial in severe depression, and it may even be time-sensitive."""
  else :
    ppd = 'None'

  return ppd