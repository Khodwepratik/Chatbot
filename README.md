# Chatbot
The above code is for a chatbot in Python

## Clone the repository
      git clone https://github.com/Khodwepratik/Chatbot.git

# Install the dependencies for executing the code 
      
    ## Install the following packages using pip install 
      Flask==2.0.2
      PyMuPDF==1.19.13
      spacy==3.2.1

## Download the Spycy language model
    python -m spacy download en_core_web_sm


# Run the flask application 
     python app.py    

 1. Open Your Browser and Navigate to http://127.0.0.1:5000    
 2. Enter your query in the input box and submit the form.
 3. The application will search the dataset and PDF document for relevant information and display the answer.
    
## Dependencies
      1. Flask
      2. PyMuPDF (fitz)
      3. spaCy

##Notes
1. The dataset is loaded from a JSON file (data.json). Which is having the basic format questions.
2. The PDF document is loaded using PyMuPDF (fitz).
3. Ensure the paths of the code correctly
4. The application uses spaCy for natural language processing tasks such as tokenization and entity recognition.
