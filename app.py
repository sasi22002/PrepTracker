from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
from dbhelper import interview_db, company_db, question_db, study_db, status_state_db

app = Flask(__name__)

from plot_gen import plot_interview_status

# Routes
@app.route('/')
def home():
    interviews = interview_db.get_all_interviews()
    plot = plot_interview_status()
    
    return render_template('home.html', interviews=interviews, plot_url=f'data:image/png;base64,{plot}')

@app.route('/show-questions/')
def show_questions():
    questions = study_db.get_all_study_materials()
    return render_template('show_questions.html', questions=questions)

@app.route('/show-questions/update-study_questions', methods=['PUT', 'POST', 'DELETE'])
def update_study_questions():
    if request.method == 'PUT':
        try:
            data = request.get_json()
            question = study_db.get_study_material_by_id(data['id'])
            if question:
                study_db.update_study_material(data['id'], data['answer'])
                return jsonify({'status': True, 'message': 'Question updated successfully!'})
            else:
                return jsonify({'status': 'error', 'message': 'Question not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400
            
            if study_db.study_material_exists(data['question']):
                return jsonify({'status': 'error', 'message': 'Question already exist'}), 400

            study_db.create_study_material(
                question=data['question'],
                answer=data['answer'],
                belongs_to=data['type']
            )
                
            return jsonify({'status': True, 'message': 'Question created successfully!'})
        except Exception as e:
            print(f"Error in POST study material: {str(e)}")
            return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 400
    
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            question = study_db.get_study_material_by_id(data['id'])
            if question:
                study_db.delete_study_material(data['id'])
                return jsonify({'status': True, 'message': 'Question deleted successfully!'})
            else:
                return jsonify({'status': 'error', 'message': 'Question not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

@app.route('/add_interview')
def add_interview_web():
    status_options = status_state_db.get_all_status_options()
    state_options = status_state_db.get_all_state_options()
    return render_template('add_interview.html', status_options=status_options, state_options=state_options)

@app.route('/view/<int:id>/')
def view_interview_web(id):
    interview = interview_db.get_interview_with_questions(id)
    if not interview:
        return render_template('error.html'), 404
    
    return render_template('view_interview.html', interview=interview)

@app.route('/add_question', methods=['GET', 'POST', 'DELETE'])
def add_question_web():
    if request.method == 'GET':
        questions = question_db.get_all_questions()
        interviews = interview_db.get_all_interviews()
        companies = company_db.get_all_companies()
        
        context = {
            'questions': questions,
            'interviews': interviews,
            'companies': companies,
        }
        return render_template('view_question.html', **context)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if question_db.question_exists(data['question'], int(data['interview'])):
                return jsonify({'status': 'error', 'message': 'Question already exist'}), 400

            question_db.create_question(
                question=data['question'],
                answer=data['answer'],
                interview_id=int(data['interview']),
                question_type=data['question_type'],
                company_id=int(data['company'])
            )

            return jsonify({'status': 'success', 'message': 'Question added successfully!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400
    
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            question = question_db.get_question_by_id(data['id'])
            if question:
                question_db.delete_question(data['id'])
                return jsonify({'status': 'success', 'message': 'Question deleted successfully!'})
            else:
                return jsonify({'status': 'error', 'message': 'Question not found'}), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/add_question/view/<int:id>/')
def view_single_question(id):
    question = question_db.get_question_by_id(id)
    if not question:
        return render_template('error.html'), 404
    return render_template('view_singlequestion.html', question=[question])

@app.route('/edit_question/view/<int:id>/', methods=['GET', 'PUT'])
def edit_single_question(id):
    question = question_db.get_question_by_id(id)
    if not question:
        return render_template('error.html'), 404
    
    if request.method == 'GET':
        return render_template('edit_question.html', question=[question])
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            question_db.update_question(id, data['question'], data['answer'], data['question_type'])
            return jsonify({'status': 'success', 'message': 'Question updated successfully!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/api/companies')
def list_company():
    companies = company_db.get_all_companies()
    return jsonify({'data': companies})

@app.route('/api/add_company', methods=['POST'])
def add_company():
    try:
        data = request.get_json()
        
        if company_db.company_exists(data['company_name']):
            return jsonify({'status': 'error', 'message': 'Company already exists'}), 400
        
        company_db.create_company(data['company_name'])
        
        return jsonify({'status': 'success', 'message': 'Company created successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'error'}), 500

@app.route('/api/add_interview', methods=['POST'])
def save_interview():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400
        
        # Validate required fields
        required_fields = ['company_name', 'date', 'status', 'state']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        if interview_db.interview_exists(data['company_name'], data['date']):
            return jsonify({'status': 'error', 'message': 'Interview already added'}), 400
        
        interview_db.create_interview(
            company_name=data['company_name'],
            date=data['date'],
            status=data['status'],
            state=data['state'],
            description=data.get('description')
        )
                    
        return jsonify({'status': 'success', 'message': 'Interview added successfully'}), 201
    except Exception as e:
        print(f"Error in save_interview: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 500

@app.route('/edit_interview/<int:id>/')
def edit_interview_web(id):
    interview = interview_db.get_interview_by_id(id)
    if not interview:
        return jsonify({'status': 'error', 'message': 'Interview not found'}), 404
    
    status_options = status_state_db.get_all_status_options()
    state_options = status_state_db.get_all_state_options()
    return render_template('edit_interview.html', interview=interview, status_options=status_options, state_options=state_options)

@app.route('/api/edit_interview', methods=['PUT'])
def edit_interview():
    try:
        data = request.get_json()
        
        if interview_db.update_interview(data['id'], data['date'], data['status'], data['state'], data['description']):
            return jsonify({'status': 'success', 'message': 'Interview updated successfully'}), 201
        else:
            return jsonify({'status': 'Failed', 'message': 'Interview not found'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'error'}), 500

@app.route('/api/delete_interview/<int:id>', methods=['DELETE'])
def delete_interview(id):
    try:
        if interview_db.delete_interview(id):
            return jsonify({'status': 'success', 'message': 'Interview deleted successfully'}), 201
        else:
            return jsonify({'status': 'Failed', 'message': 'Interview not found'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
