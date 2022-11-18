import numpy as np
import pandas as pd
#from sklearn.linear_model import LogisticRegression
import pickle

def predict_patient_showup(appointment_id):
    return "Hello World !"


    # Load the model
    with open('final_model.sav', 'rb') as f:
        model = pickle.load(f)
    
    classes = {0:'No',1:'Yes'}
    
    # return prediction as well as class probabilities
    preds = model.predict_proba([arr])[0]
    return (classes[np.argmax(preds)], preds)


# import streamlit as st
# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# from model_methods import predict

# classes = {0:'setosa',1:'versicolor',2:'virginica'}
# class_labels = list(classes.values())
# st.title("Classification of Iris Species")
# st.markdown('**Objective** : Given details about the flower we try to predict the species.')
# st.markdown('The model can predict if it belongs to the following three Categories : **setosa, versicolor, virginica** ')
# def predict_class():
#     data = list(map(float,[sepal_length,sepal_width,petal_length, petal_width]))
#     result, probs = predict(data)
#     st.write("The predicted class is ",result)
#     probs = [np.round(x,6) for x in probs]
#     ax = sns.barplot(probs ,class_labels, palette="winter", orient='h')
#     ax.set_yticklabels(class_labels,rotation=0)
#     plt.title("Probabilities of the Data belonging to each class")
#     for index, value in enumerate(probs):
#         plt.text(value, index,str(value))
#     st.pyplot()
# st.markdown("**Please enter the details of the flower in the form of 4 floating point values separated by commas**")
# sepal_length = st.text_input('Enter sepal_length', '')
# sepal_width = st.text_input('Enter sepal_width', '')
# petal_length = st.text_input('Enter petal_length', '')
# petal_width = st.text_input('Enter petal_width', '')
# if st.button("Predict"):
#     predict_class()
