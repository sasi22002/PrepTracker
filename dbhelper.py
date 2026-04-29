import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any

class DBHelper:
    def __init__(self, db_path: str = 'instance/prod.sqlite3'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Make rows dictionary-like
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            result = [dict(row) for row in cursor.fetchall()]
            return result
        finally:
            conn.close()
    
    def execute_write(self, query: str, params: tuple = ()) -> int:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Make rows dictionary-like
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Make rows dictionary-like
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

class CompanyDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_companies(self) -> List[Dict[str, Any]]:
        query = "SELECT id, company_name FROM company_data"
        return self.db.execute_query(query)
    
    def get_company_by_name(self, company_name: str) -> Optional[Dict[str, Any]]:
        query = "SELECT id, company_name FROM company_data WHERE company_name = ?"
        result = self.db.execute_query(query, (company_name,))
        return result[0] if result else None
    
    def create_company(self, company_name: str) -> int:
        query = "INSERT INTO company_data (company_name) VALUES (?)"
        return self.db.execute_write(query, (company_name,))
    
    def company_exists(self, company_name: str) -> bool:
        query = "SELECT COUNT(*) as count FROM company_data WHERE company_name = ?"
        result = self.db.execute_query(query, (company_name,))
        return result[0]['count'] > 0

class InterviewDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_interviews(self) -> List[Dict[str, Any]]:
        query = """
        SELECT i.sno, i.date, i.status, i.state, i.is_deleted, i.is_attended, 
               i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.is_deleted = 0
        ORDER BY i.date DESC
        """
        return self.db.execute_query(query)
    
    def get_interview_by_id(self, sno: int) -> Optional[Dict[str, Any]]:
        query = """
        SELECT i.sno, i.date, i.status, i.state, i.is_deleted, i.is_attended, 
               i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.sno = ? AND i.is_deleted = 0
        """
        result = self.db.execute_query(query, (sno,))
        return result[0] if result else None
    
    def get_interview_with_questions(self, sno: int) -> Optional[Dict[str, Any]]:
        interview_query = """
        SELECT i.sno, i.date, i.status, i.state, i.is_deleted, i.is_attended, 
               i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.sno = ? AND i.is_deleted = 0
        """
        
        questions_query = """
        SELECT question, answer
        FROM question_master
        WHERE interview_id = ? AND is_deleted = 0
        """
        
        interview_result = self.db.execute_query(interview_query, (sno,))
        if not interview_result:
            return None
        
        interview = interview_result[0]
        questions = self.db.execute_query(questions_query, (sno,))
        interview['questions'] = questions
        
        return interview
    
    def create_interview(self, company_name: str, date: str, status: str, state: str, description: str = None) -> int:
        # Get or create company
        company_helper = CompanyDBHelper(self.db)
        company = company_helper.get_company_by_name(company_name)
        if not company:
            company_id = company_helper.create_company(company_name)
        else:
            company_id = company['id']
        
        query = """
        INSERT INTO interview_master (company_name_id, date, status, state, description, is_deleted, is_attended)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_write(query, (company_id, date, status, state, description, 0, 0))
    
    def update_interview(self, sno: int, date: str, status: str, state: str, description: str = None) -> int:
        query = """
        UPDATE interview_master 
        SET date = ?, status = ?, state = ?, description = ?
        WHERE sno = ?
        """
        return self.db.execute_update(query, (date, status, state, description, sno))
    
    def delete_interview(self, sno: int) -> int:
        query = "UPDATE interview_master SET is_deleted = 1 WHERE sno = ?"
        return self.db.execute_update(query, (sno,))
    
    def interview_exists(self, company_name: str, date: str) -> bool:
        query = """
        SELECT COUNT(*) as count
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE c.company_name = ? AND i.date = ?
        """
        result = self.db.execute_query(query, (company_name, date))
        return result[0]['count'] > 0

class QuestionAnswerDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        query = """
        SELECT qa.id, qa.question, qa.answer, qa.question_type, qa.interview_id,
               qa.company_question_id, c.company_name, i.sno as interview_sno
        FROM question_master qa
        JOIN company_data c ON qa.company_question_id = c.id
        JOIN interview_master i ON qa.interview_id = i.sno
        WHERE qa.is_deleted = 0
        """
        return self.db.execute_query(query)
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        query = """
        SELECT qa.id, qa.question, qa.answer, qa.question_type, qa.interview_id,
               qa.company_question_id, c.company_name, i.sno as interview_sno
        FROM question_master qa
        JOIN company_data c ON qa.company_question_id = c.id
        JOIN interview_master i ON qa.interview_id = i.sno
        WHERE qa.id = ? AND qa.is_deleted = 0
        """
        result = self.db.execute_query(query, (question_id,))
        return result[0] if result else None
    
    def create_question(self, question: str, answer: str, interview_id: int, 
                       question_type: str, company_id: int) -> int:
        query = """
        INSERT INTO question_master (question, answer, interview_id, question_type, company_question_id)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_write(query, (question, answer, interview_id, question_type, company_id))
    
    def update_question(self, question_id: int, question: str, answer: str, question_type: str) -> int:
        query = """
        UPDATE question_master 
        SET question = ?, answer = ?, question_type = ?
        WHERE id = ?
        """
        return self.db.execute_update(query, (question, answer, question_type, question_id))
    
    def delete_question(self, question_id: int) -> int:
        query = "UPDATE question_master SET is_deleted = 1 WHERE id = ?"
        return self.db.execute_update(query, (question_id,))
    
    def question_exists(self, question: str, interview_id: int) -> bool:
        query = "SELECT COUNT(*) as count FROM question_master WHERE question = ? AND interview_id = ? AND is_deleted = 0"
        result = self.db.execute_query(query, (question, interview_id))
        return result[0]['count'] > 0

class StudyMaterialDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_study_materials(self) -> List[Dict[str, Any]]:
        query = "SELECT id, question, answer, belongs_to, repeat_count, question_type FROM preparation_master WHERE is_deleted = 0"
        return self.db.execute_query(query)
    
    def get_study_material_by_id(self, material_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT id, question, answer, belongs_to, repeat_count, question_type FROM preparation_master WHERE id = ? AND is_deleted = 0"
        result = self.db.execute_query(query, (material_id,))
        return result[0] if result else None
    
    def create_study_material(self, question: str, answer: str, belongs_to: str, question_type: str = 'theory') -> int:
        query = "INSERT INTO preparation_master (question, answer, belongs_to, repeat_count, is_deleted, question_type) VALUES (?, ?, ?, ?, ?, ?)"
        return self.db.execute_write(query, (question, answer, belongs_to, 0, 0, question_type))
    
    def update_study_material(self, material_id: int, answer: str) -> int:
        query = "UPDATE preparation_master SET answer = ? WHERE id = ?"
        return self.db.execute_update(query, (answer, material_id))
    
    def delete_study_material(self, material_id: int) -> int:
        query = "UPDATE preparation_master SET is_deleted = 1 WHERE id = ?"
        return self.db.execute_update(query, (material_id,))
    
    def study_material_exists(self, question: str) -> bool:
        query = "SELECT COUNT(*) as count FROM preparation_master WHERE question = ? AND is_deleted = 0"
        result = self.db.execute_query(query, (question,))
        return result[0]['count'] > 0
    
    def reclassify_question_type(self, material_id: int, question_type: str) -> int:
        """Reclassify a question as coding or theory"""
        query = "UPDATE preparation_master SET question_type = ? WHERE id = ?"
        return self.db.execute_update(query, (question_type, material_id))

class StatusStateDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_status_options(self) -> List[Dict[str, Any]]:
        query = "SELECT id, status_name FROM status_options WHERE is_active = 1 ORDER BY status_name"
        return self.db.execute_query(query)
    
    def get_all_state_options(self) -> List[Dict[str, Any]]:
        query = "SELECT id, state_name FROM state_options WHERE is_active = 1 ORDER BY state_name"
        return self.db.execute_query(query)

class StatisticsDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def normalize_status(self, status: str) -> str:
        """Normalize status to consistent format"""
        if not status:
            return 'Unknown'
        
        status_lower = status.lower().strip()
        
        # Map similar statuses to normalized values
        status_mapping = {
            'offered': 'Offered',
            'passed': 'Passed', 
            'selected': 'Selected',
            'joined': 'Joined',
            'rejected': 'Rejected',
            'failed': 'Failed',
            'pending': 'Pending',
            'in progress': 'In Progress',
            'waiting for response': 'Waiting',
            'on hold': 'On Hold',
            'withdrawn': 'Withdrawn'
        }
        
        return status_mapping.get(status_lower, status.title())
    
    def get_status_category(self, status: str) -> str:
        """Categorize status as positive, negative, or neutral"""
        normalized = self.normalize_status(status)
        
        positive_statuses = ['Offered', 'Passed', 'Selected', 'Joined']
        negative_statuses = ['Rejected', 'Failed', 'Withdrawn']
        neutral_statuses = ['Pending', 'In Progress', 'Waiting', 'On Hold', 'Unknown']
        
        if normalized in positive_statuses:
            return 'positive'
        elif normalized in negative_statuses:
            return 'negative'
        else:
            return 'neutral'
    
    def get_interview_statistics(self) -> Dict[str, Any]:
        """Get comprehensive interview statistics with normalized values"""
        stats = {}
        
        # Total interviews
        total_query = "SELECT COUNT(*) as total FROM interview_master WHERE is_deleted = 0"
        total_result = self.db.execute_query(total_query)
        stats['total_interviews'] = total_result[0]['total']
        
        # Status breakdown with normalization
        status_query = """
        SELECT status, COUNT(*) as count 
        FROM interview_master 
        WHERE is_deleted = 0 
        GROUP BY status
        """
        status_result = self.db.execute_query(status_query)
        
        # Normalize and group statuses
        normalized_status_breakdown = {}
        status_categories = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for row in status_result:
            normalized_status = self.normalize_status(row['status'])
            category = self.get_status_category(row['status'])
            
            # Add to normalized breakdown
            if normalized_status in normalized_status_breakdown:
                normalized_status_breakdown[normalized_status] += row['count']
            else:
                normalized_status_breakdown[normalized_status] = row['count']
            
            # Add to category totals
            status_categories[category] += row['count']

        
        stats['status_breakdown'] = normalized_status_breakdown
        stats['status_categories'] = status_categories
        
        # State breakdown with normalization
        state_query = """
        SELECT state, COUNT(*) as count 
        FROM interview_master 
        WHERE is_deleted = 0 
        GROUP BY state
        """
        state_result = self.db.execute_query(state_query)
        
        # Normalize states
        normalized_state_breakdown = {}
        for row in state_result:
            normalized_state = row['state'].title().strip() if row['state'] else 'Unknown'
            if normalized_state in normalized_state_breakdown:
                normalized_state_breakdown[normalized_state] += row['count']
            else:
                normalized_state_breakdown[normalized_state] = row['count']
        
        stats['state_breakdown'] = normalized_state_breakdown
        
        # Attended vs not attended
        attended_query = """
        SELECT is_attended, COUNT(*) as count 
        FROM interview_master 
        WHERE is_deleted = 0 
        GROUP BY is_attended
        """
        attended_result = self.db.execute_query(attended_query)
        stats['attended_breakdown'] = {row['is_attended']: row['count'] for row in attended_result}
        
        # Company breakdown
        company_query = """
        SELECT c.company_name, COUNT(*) as count 
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.is_deleted = 0 
        GROUP BY c.company_name
        ORDER BY count DESC
        """
        company_result = self.db.execute_query(company_query)
        stats['company_breakdown'] = {row['company_name']: row['count'] for row in company_result}
        
        # Monthly statistics
        monthly_query = """
        SELECT strftime('%Y-%m', date) as month, COUNT(*) as count 
        FROM interview_master 
        WHERE is_deleted = 0 
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
        """
        monthly_result = self.db.execute_query(monthly_query)
        stats['monthly_breakdown'] = {row['month']: row['count'] for row in monthly_result}
        
        # Recent interviews (last 30 days)
        recent_query = """
        SELECT COUNT(*) as count 
        FROM interview_master 
        WHERE is_deleted = 0 AND date >= date('now', '-30 days')
        """
        recent_result = self.db.execute_query(recent_query)
        stats['recent_interviews'] = recent_result[0]['count']
        
        return stats
    
    def get_interviews_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get interviews filtered by status category (positive, negative, neutral)"""
        query = """
        SELECT i.sno, i.date, i.status, i.state, i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.is_deleted = 0
        """
        
        result = self.db.execute_query(query)
        
        # Filter by category
        filtered_interviews = []
        for interview in result:
            if self.get_status_category(interview['status']) == category:
                # Normalize status for display
                interview['normalized_status'] = self.normalize_status(interview['status'])
                interview['normalized_state'] = interview['state'].title().strip() if interview['state'] else 'Unknown'
                filtered_interviews.append(interview)
        
        return filtered_interviews
    
    def get_interviews_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get interviews filtered by specific status"""
        normalized_target = self.normalize_status(status)
        
        query = """
        SELECT i.sno, i.date, i.status, i.state, i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.is_deleted = 0
        """
        
        result = self.db.execute_query(query)
        
        # Filter by normalized status
        filtered_interviews = []
        for interview in result:
            if self.normalize_status(interview['status']) == normalized_target:
                interview['normalized_status'] = self.normalize_status(interview['status'])
                interview['normalized_state'] = interview['state'].title().strip() if interview['state'] else 'Unknown'
                filtered_interviews.append(interview)
        
        return filtered_interviews
    
    def get_recent_interviews(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent interviews within specified days"""
        query = f"""
        SELECT i.sno, i.date, i.status, i.state, i.description, c.company_name
        FROM interview_master i
        JOIN company_data c ON i.company_name_id = c.id
        WHERE i.is_deleted = 0 
        ORDER BY i.date DESC
        """
        
        result = self.db.execute_query(query)
        
        # Normalize for display
        for interview in result:
            interview['normalized_status'] = self.normalize_status(interview['status'])
            interview['normalized_state'] = interview['state'].title().strip() if interview['state'] else 'Unknown'
        
        return result
    
    def get_study_materials_statistics(self) -> Dict[str, Any]:
        """Get study materials statistics"""
        stats = {}
        
        # Total study materials
        total_query = "SELECT COUNT(*) as total FROM preparation_master WHERE is_deleted = 0"
        total_result = self.db.execute_query(total_query)
        stats['total_materials'] = total_result[0]['total']
        
        # Type breakdown
        type_query = """
        SELECT belongs_to, COUNT(*) as count 
        FROM preparation_master 
        WHERE is_deleted = 0 
        GROUP BY belongs_to
        """
        type_result = self.db.execute_query(type_query)
        stats['type_breakdown'] = {row['belongs_to']: row['count'] for row in type_result}
        
        return stats
    
    def get_questions_statistics(self) -> Dict[str, Any]:
        """Get questions statistics"""
        stats = {}
        
        # Total questions
        total_query = "SELECT COUNT(*) as total FROM question_master WHERE is_deleted = 0"
        total_result = self.db.execute_query(total_query)
        stats['total_questions'] = total_result[0]['total']
        
        # Question type breakdown
        type_query = """
        SELECT question_type, COUNT(*) as count 
        FROM question_master 
        WHERE is_deleted = 0 
        GROUP BY question_type
        """
        type_result = self.db.execute_query(type_query)
        stats['question_type_breakdown'] = {row['question_type']: row['count'] for row in type_result}
        
        return stats

# Database helper instance
db_helper = DBHelper()
company_db = CompanyDBHelper(db_helper)
interview_db = InterviewDBHelper(db_helper)
question_db = QuestionAnswerDBHelper(db_helper)
study_db = StudyMaterialDBHelper(db_helper)
status_state_db = StatusStateDBHelper(db_helper)
statistics_db = StatisticsDBHelper(db_helper)
