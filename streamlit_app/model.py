import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle

def onehot_encode(X, cols):
    # Treat new categories as a new 'unknown' category (all onehot columns are 0)
    onehot_enc = OneHotEncoder(handle_unknown='ignore')
    # Fit encoder on training data
    onehot_enc.fit(X[cols])
    # Get the names of the new columns created
    colnames = list(onehot_enc.get_feature_names(input_features=cols))
    # Transform the data
    onehot_vals = onehot_enc.transform(X[cols]).toarray()
    # Put transformed data into dataframe
    enc_df = pd.DataFrame(onehot_vals,columns=colnames,index=X.index)
    # Add onehot columns back onto original dataframe and drop the original columns
    X = pd.concat([X,enc_df],axis=1).drop(cols,axis=1)
    return X,onehot_enc


def predict_patient_showup(appointment_id, df):
    # Load the model
    with open('finalized_model.sav', 'rb') as f:
        model = pickle.load(f)
    
    data_for_pred = df.copy()
    
    ## Ordinal encoder for features
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    ## Fit encoder on train and apply to test data as well
    data_for_pred[["gender"]] = enc.fit_transform(data_for_pred[["gender"]])

    ## One hot encode the train data
    cols = ["appointment_day_of_week"]
    data_for_pred, onehot_enc = onehot_encode(data_for_pred, cols)

    data_for_pred = data_for_pred[data_for_pred["appointmentid"] == int(appointment_id)].copy()
    data_for_pred.drop(columns=["age_group", "neighbourhood", "patientid", "appointmentid",
                    "scheduledday", "appointmentday", "showed", "no_show"] , inplace=True)
    
    ## predict class
    y_pred_class = model.predict(data_for_pred)

    return y_pred_class[0]
    
    # # calculate prediction as well as class probabilities
    # preds = model.predict_proba([arr])[0]
    # return (classes[np.argmax(preds)], preds)

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
