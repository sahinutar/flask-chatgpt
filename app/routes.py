import os
from flask import Blueprint, flash, redirect, render_template, request, jsonify, session, url_for
from app.chatbot import generate_response, index_pdf_documents
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET'])
def index():
    session['conversation'] = []  # Initialize the conversation history
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    print("USER INPUT from routespy:", user_input) 
    session['conversation'].append((user_input, "user"))  # Add user input to the conversation history

    response = generate_response(session['conversation'])
    session['conversation'].append((response, "assistant"))  # Add AI response to the conversation history

    return jsonify(response=response)

# @main.route('/datachat', methods=['POST'])
# def datachat():
#     user_data_input = request.form['user_data_input']
#     print("USER INPUT from routespy:", user_data_input) 
#     session['conversation'].append((user_data_input, "user"))  # Add user input to the conversation history

#     response = generate_data_response(session['conversation'])
#     session['conversation'].append((response, "assistant"))  # Add AI response to the conversation history

#     return jsonify(response=response)


@main.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully')
            index_pdf_documents()
            return render_template('upload.html')  
    return render_template('upload.html')