import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle

def onehot_encode(X, cols):
    """
    This function one hot encodes the features

    Agrs:
    X -> Dataframe which we want to one hot encode
    cols -> List of column names you want to one hot encode

    Returns:
    X -> One hot encoded dataframe
    onehot_enc -> the encoder object used to one hot encode
    """
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
    """
    This function predicts the patient no show

    Args:
    appointment_id -> appointment for which we want to predict show / no show
    df -> the primary dataset

    Returns:
    the predicted class 0 or 1
    """
    # Load the model
    with open('./streamlit_app/data/finalized_model.sav', 'rb') as f:
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