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
        query = "SELECT id, question, answer, belongs_to, repeat_count FROM preparation_master WHERE is_deleted = 0"
        return self.db.execute_query(query)
    
    def get_study_material_by_id(self, material_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT id, question, answer, belongs_to, repeat_count FROM preparation_master WHERE id = ? AND is_deleted = 0"
        result = self.db.execute_query(query, (material_id,))
        return result[0] if result else None
    
    def create_study_material(self, question: str, answer: str, belongs_to: str) -> int:
        query = "INSERT INTO preparation_master (question, answer, belongs_to, repeat_count, is_deleted) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_write(query, (question, answer, belongs_to, 0, 0))
    
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

class StatusStateDBHelper:
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_status_options(self) -> List[Dict[str, Any]]:
        query = "SELECT id, status_name FROM status_options WHERE is_active = 1 ORDER BY status_name"
        return self.db.execute_query(query)
    
    def get_all_state_options(self) -> List[Dict[str, Any]]:
        query = "SELECT id, state_name FROM state_options WHERE is_active = 1 ORDER BY state_name"
        return self.db.execute_query(query)

# Database helper instance
db_helper = DBHelper()
company_db = CompanyDBHelper(db_helper)
interview_db = InterviewDBHelper(db_helper)
question_db = QuestionAnswerDBHelper(db_helper)
study_db = StudyMaterialDBHelper(db_helper)
status_state_db = StatusStateDBHelper(db_helper)
