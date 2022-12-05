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
    ppd = 'Based on you assessment None or Minimal Depression'
  elif pred_result == 1:
    ppd = 'Based on you assessment Mild Depression'
  elif pred_result == 2:
    ppd = 'Based on you assessment Moderate Depression'
  elif pred_result == 3:
    ppd = 'Based on you assessment Severe Depression'
  else :
    ppd = 'None'

  return ppd