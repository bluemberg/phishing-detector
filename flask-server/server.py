# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def main():
#     print("Hello world!")

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify

import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import feature_extractor as fe

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse_text():
    data = request.get_json()
    text = data['text']
   
    df = pd.read_csv('dataset_phishing.csv')
    df.drop(['url', 'status', 'nb_or', 'ratio_nullHyperlinks', 'ratio_intRedirection', 'ratio_intErrors', "ratio_extRedirection", "ratio_extErrors", 'submit_email', 'sfh', "random_domain", "whois_registered_domain", "domain_registration_length", "domain_age", "web_traffic", "google_index"], axis = 1, inplace = True)

    website = text
    # print("--------------------------")
    # print("--------------------------")
    # print("--------------------------")
    state, iurl, page = fe.is_URL_accessible(website)

    if state:
        print("Connect: OK")
        y = fe.extract_features(website)

        df.iloc[0] = y

        columns = df.columns.to_list()
        scaler = StandardScaler()
        for column in columns:
            df[[column]] = scaler.fit_transform(df[[column]])

        with open("svm_tuned.pkl", "rb") as f:
            clf  = pickle.load(f)

        y = df.iloc[0]
        preds = clf.predict([y])
        # print("--------------------------")
        # print("--------------------------")
        # print("--------------------------")
        return jsonify({'result': preds[0]})
    else:
        return jsonify({'result': "The website is not accessible. Please check the URL."})

if __name__ == '__main__':
    app.run()