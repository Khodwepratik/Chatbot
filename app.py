#Chatbot Code which takes .json and .pdf data as input and answer the relevent text

from flask import Flask, render_template, request, jsonify
import json
import fitz
import spacy

app = Flask(__name__)

# Importing the NLP Language Model Loading
nlp = spacy.load("en_core_web_sm")

# Load data from a JSON file 
with open('data.json', 'r') as file:      #Replace with the path of your json file
    json_data = json.load(file)

# Search Function for above PDF
def search_pdf(query, pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
    return text.lower().find(query.lower()) != -1

#function for token seperation from the user query
def analyze_user_input(user_input):
    doc = nlp(user_input)
    entities = [ent.text for ent in doc.ents]
    tokens = [token.text for token in doc]
    return entities, tokens

#searching for synonyms in the code
def get_synonyms(word):
    synonyms = set()
    for syn in word.synonyms:
        synonyms.add(syn.text)
    for child in word.children:
        synonyms.update(get_synonyms(child))
    return synonyms

#Searching entity 
def enhance_search(query, json_item, entities, tokens):
    for entity in entities:
        if entity.lower() in json_item['question'].lower():
            return json_item['answer']
        for token in tokens:
            if token.lower() in json_item['question'].lower():
                return json_item['answer']
    return "Sorry, I don't understand that."

#optimized searching from the pdf
def search_pdf_optimized(query, pdf_path):
    with fitz.open(pdf_path) as doc:
        text = " ".join(page.get_text() for page in doc)
    return text.lower().find(query.lower()) != -1

#search answer in the json data 
def get_bot_response(user_input, entities, tokens):
    for item in json_data['questions']:
        if any(entity.lower() in item['question'].lower() for entity in entities) or any(
                token.lower() in item['question'].lower() for token in tokens
        ):
            return item['answer']
        
    pdf_path = 'java.pdf'                #Replace with the path to your PDF file
    pdf_answer = get_pdf_answer(user_input, pdf_path)
    if pdf_answer:
        return pdf_answer
    return "Sorry, I don't understand that."

#searching in pdf for answer/ relevant data 
def get_pdf_answer(query, pdf_path):
    with fitz.open(pdf_path) as doc:
        relevant_text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text = page.get_text()
            if query.lower() in text.lower():
                relevant_text += text

        if relevant_text:
            return relevant_text
        else:
            return None

@app.route('/')
def index():
    return render_template('index.html')  #UI for query and response

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    entities, tokens = analyze_user_input(user_input)
    response = get_bot_response(user_input, entities, tokens)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
