import pickle
import sklearn

with open(r'sanitybot\pickles\ppd_decisiontree.pkl', 'rb') as f:
    decisionTree_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_naiveBayes.pkl', 'rb') as f:
    naiveBayes_model = pickle.load(f)
with open(r'sanitybot\pickles\ppd_svm.pkl', 'rb') as f:
    svm_model = pickle.load(f)

def pdd_prediction(list):
  pred_result = svm_model.predict([list])[0]

  if pred_result == 0:
    ppd = 'Based on you assessment you have None or Minimal Depression'
  elif pred_result == 1:
    ppd = 'Based on you assessment you have Mild Depression'
  elif pred_result == 2:
    ppd = 'Based on you assessment you have Moderate Depression'
  elif pred_result == 3:
    ppd = 'Based on you assessment you have Severe Depression'
  else :
    ppd = 'None'

  return ppd