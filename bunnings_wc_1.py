from flask import Flask, render_template, request, send_file
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from textblob import TextBlob

app = Flask(__name__)

def summarize_tb(text):
    blob = TextBlob(text)
    keywords = blob.noun_phrases
    summary = ' '.join(keywords[:2])
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        sheet_name='Q10'

        # Save the file to disk
        filename = file.filename
        file.save(os.path.join('./uploads', filename))

        # Load the Excel file
        df = pd.read_excel(os.path.join('uploads', filename), sheet_name=sheet_name)

        txt_2 = df[sheet_name].astype(str)

        df['summary_tb'] = txt_2.apply(summarize_tb)

        # Join the text columns into a single string
        summary_text = ' '.join(df['summary_tb'])

        #text = ' '.join(df['text'])

        # Generate a word cloud from the text
        wordcloud = WordCloud().generate(summary_text)


        # Save the word cloud to a file
        wordcloud_filename = os.path.join('./static', 'wordcloud.png')
        wordcloud.to_file(wordcloud_filename)

        # Render the word cloud in a template
        #return render_template('index.html', wordcloud=wordcloud_filename)
        return send_file(wordcloud_filename, mimetype='image/png')

    # Render the upload form
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)