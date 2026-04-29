from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
from dbhelper import interview_db, company_db, question_db, study_db, status_state_db, statistics_db

app = Flask(__name__)

from plot_gen import plot_interview_status, plot_status_pie_chart, plot_monthly_trend, plot_company_distribution
from graph_cache import graph_cache, background_generator
from coding_db import coding_db

# Routes
@app.route('/')
def home():
    # Load statistics immediately (fast operation)
    interviews = interview_db.get_all_interviews()
    stats = statistics_db.get_interview_statistics()
    
    # Try to get cached plot, but don't block if not available
    plot = graph_cache.get_cached_graph('interview_status')
    plot_url = f'data:image/png;base64,{plot}' if plot else None
    
    # Start background generation if plot is not cached
    if not plot:
        background_generator.generate_graph_async('interview_status', plot_interview_status)
    
    return render_template('home.html', interviews=interviews, plot_url=plot_url, stats=stats)

@app.route('/dashboard')
def dashboard():
    # Load statistics immediately (fast operation)
    interview_stats = statistics_db.get_interview_statistics()
    study_stats = statistics_db.get_study_materials_statistics()
    question_stats = statistics_db.get_questions_statistics()
    
    # Try to get cached charts, but don't block if not available
    status_pie = graph_cache.get_cached_graph('status_pie')
    monthly_trend = graph_cache.get_cached_graph('monthly_trend')
    company_dist = graph_cache.get_cached_graph('company_distribution')
    
    charts = {
        'status_pie': f'data:image/png;base64,{status_pie}' if status_pie else None,
        'monthly_trend': f'data:image/png;base64,{monthly_trend}' if monthly_trend else None,
        'company_distribution': f'data:image/png;base64,{company_dist}' if company_dist else None
    }
    
    # Start background generation for any missing charts
    if not status_pie:
        background_generator.generate_graph_async('status_pie', plot_status_pie_chart)
    if not monthly_trend:
        background_generator.generate_graph_async('monthly_trend', plot_monthly_trend)
    if not company_dist:
        background_generator.generate_graph_async('company_distribution', plot_company_distribution)
    
    return render_template('dashboard.html', 
                         interview_stats=interview_stats, 
                         study_stats=study_stats, 
                         question_stats=question_stats, 
                         charts=charts)

@app.route('/show-questions/')
def show_questions():
    questions = study_db.get_all_study_materials()
    return render_template('show_questions_final.html', questions=questions)

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

            # Determine question type based on checkbox or content analysis
            question_type = 'coding' if data.get('is_coding', False) else 'theory'
            
            study_db.create_study_material(
                question=data['question'],
                answer=data['answer'],
                belongs_to=data['type'],
                question_type=question_type
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

@app.route('/show-questions/reclassify', methods=['POST'])
def reclassify_question():
    """Reclassify a question as coding or theory"""
    try:
        data = request.get_json()
        question_id = data.get('id')
        new_type = data.get('type', 'theory')  # Default to theory
        
        if not question_id:
            return jsonify({'status': False, 'message': 'Missing question ID'}), 400
        
        success = study_db.reclassify_question_type(question_id, new_type)
        if success:
            return jsonify({
                'status': True, 
                'message': f'Question reclassified as {new_type} successfully'
            })
        else:
            return jsonify({'status': False, 'message': 'Failed to reclassify question'}), 500
            
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)}), 500

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

@app.route('/api/interviews/category/<category>')
def get_interviews_by_category(category):
    """Get interviews filtered by status category (positive, negative, neutral)"""
    try:
        if category not in ['positive', 'negative', 'neutral', 'recent']:
            return jsonify({'status': 'error', 'message': 'Invalid category'}), 400
        
        if category == 'recent':
            interviews = statistics_db.get_recent_interviews(30)
        else:
            interviews = statistics_db.get_interviews_by_category(category)
        
        return jsonify({
            'status': 'success',
            'data': interviews,
            'count': len(interviews),
            'category': category
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/interviews/status/<status>')
def get_interviews_by_status(status):
    """Get interviews filtered by specific status"""
    try:
        interviews = statistics_db.get_interviews_by_status(status)
        
        return jsonify({
            'status': 'success',
            'data': interviews,
            'count': len(interviews),
            'status_filter': status
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/interviews/recent')
def get_recent_interviews():
    """Get recent interviews"""
    try:
        days = request.args.get('days', 30, type=int)
        interviews = statistics_db.get_recent_interviews(days)
        
        return jsonify({
            'status': 'success',
            'data': interviews,
            'count': len(interviews),
            'days': days
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Graph loading endpoints
@app.route('/api/graph/<graph_type>')
def get_graph(graph_type):
    """Get graph data via AJAX"""
    try:
        # Try to get from cache first
        graph_data = graph_cache.get_cached_graph(graph_type)
        
        if graph_data:
            return jsonify({
                'status': 'success',
                'data': f'data:image/png;base64,{graph_data}',
                'cached': True
            })
        
        # If not cached, check if it's being generated
        is_generating = background_generator.is_generating(graph_type)
        
        if is_generating:
            return jsonify({
                'status': 'generating',
                'message': 'Graph is being generated in background'
            })
        
        # Start background generation
        generator_functions = {
            'interview_status': plot_interview_status,
            'status_pie': plot_status_pie_chart,
            'monthly_trend': plot_monthly_trend,
            'company_distribution': plot_company_distribution
        }
        
        if graph_type in generator_functions:
            background_generator.generate_graph_async(graph_type, generator_functions[graph_type])
            return jsonify({
                'status': 'generating',
                'message': 'Graph generation started'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unknown graph type'
            }), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/graph/status/<graph_type>')
def check_graph_status(graph_type):
    """Check if graph is ready or being generated"""
    try:
        # Check cache
        graph_data = graph_cache.get_cached_graph(graph_type)
        if graph_data:
            return jsonify({
                'status': 'ready',
                'data': f'data:image/png;base64,{graph_data}'
            })
        
        # Check if being generated
        is_generating = background_generator.is_generating(graph_type)
        return jsonify({
            'status': 'generating' if is_generating else 'not_started',
            'message': 'Graph is being generated' if is_generating else 'Graph generation not started'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Coding Questions API Routes
@app.route('/api/coding-questions', methods=['GET'])
def get_coding_questions():
    """Get all coding questions"""
    try:
        questions = coding_db.get_all_coding_questions()
        return jsonify({
            'status': 'success',
            'questions': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/coding-questions', methods=['POST'])
def add_coding_question():
    """Add a new coding question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        answer = data.get('answer', '')
        category = data.get('category', '')
        is_coding = data.get('is_coding', False)
        
        if not question or not answer or not category:
            return jsonify({'status': False, 'message': 'Missing required fields'}), 400
        
        success = coding_db.add_coding_question(question, answer, category)
        if success:
            return jsonify({'status': True, 'message': 'Coding question added successfully'})
        else:
            return jsonify({'status': False, 'message': 'Failed to add coding question'}), 500
            
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)}), 500

@app.route('/api/coding-questions', methods=['PUT'])
def update_coding_question():
    """Update an existing coding question"""
    try:
        data = request.get_json()
        question_id = data.get('id')
        question = data.get('question', '')
        answer = data.get('answer', '')
        category = data.get('category', '')
        
        if not question_id:
            return jsonify({'status': False, 'message': 'Missing question ID'}), 400
        
        success = coding_db.update_coding_question(question_id, question, answer, category)
        if success:
            return jsonify({'status': True, 'message': 'Coding question updated successfully'})
        else:
            return jsonify({'status': False, 'message': 'Failed to update coding question'}), 500
            
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)}), 500

@app.route('/api/coding-questions', methods=['DELETE'])
def delete_coding_question():
    """Delete a coding question"""
    try:
        data = request.get_json()
        question_id = data.get('id')
        
        if not question_id:
            return jsonify({'status': False, 'message': 'Missing question ID'}), 400
        
        success = coding_db.delete_coding_question(question_id)
        if success:
            return jsonify({'status': True, 'message': 'Coding question deleted successfully'})
        else:
            return jsonify({'status': False, 'message': 'Failed to delete coding question'}), 500
            
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)}), 500

@app.route('/api/coding-questions/search')
def search_coding_questions():
    """Search coding questions"""
    try:
        search_query = request.args.get('q', '')
        questions = coding_db.search_coding_questions(search_query)
        return jsonify({
            'status': 'success',
            'questions': questions,
            'count': len(questions),
            'query': search_query
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
