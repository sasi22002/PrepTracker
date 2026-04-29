from typing import List, Dict, Any, Optional
from dbhelper import DBHelper

class CodingQuestionsDBHelper:
    """Database helper for coding questions CRUD operations"""
    
    def __init__(self, db_helper: DBHelper):
        self.db = db_helper
    
    def get_all_coding_questions(self) -> List[Dict[str, Any]]:
        """Get all coding questions - using question_type field for proper persistence"""
        query = """
        SELECT id, question, answer, belongs_to, repeat_count, created_at, updated_at
        FROM preparation_master 
        WHERE is_deleted = 0 
        AND question_type = 'coding'
        ORDER BY created_at DESC
        """
        return self.db.execute_query(query)
    
    def get_coding_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific coding question by ID"""
        query = """
        SELECT id, question, answer, belongs_to, repeat_count, created_at, updated_at
        FROM preparation_master 
        WHERE id = ? AND is_deleted = 0
        """
        result = self.db.execute_query(query, (question_id,))
        return result[0] if result else None
    
    def add_coding_question(self, question: str, answer: str, category: str) -> bool:
        """Add a new coding question"""
        try:
            query = """
            INSERT INTO preparation_master (question, answer, belongs_to, repeat_count, created_at, updated_at)
            VALUES (?, ?, ?, 0, datetime('now'), datetime('now'))
            """
            self.db.execute_write(query, (question, answer, category))
            return True
        except Exception as e:
            print(f"Error adding coding question: {e}")
            return False
    
    def update_coding_question(self, question_id: int, question: str, answer: str, category: str) -> bool:
        """Update an existing coding question"""
        try:
            query = """
            UPDATE preparation_master 
            SET question = ?, answer = ?, belongs_to = ?, updated_at = datetime('now')
            WHERE id = ? AND is_deleted = 0
            """
            self.db.execute_update(query, (question, answer, category, question_id))
            return True
        except Exception as e:
            print(f"Error updating coding question: {e}")
            return False
    
    def delete_coding_question(self, question_id: int) -> bool:
        """Delete a coding question (soft delete)"""
        try:
            query = """
            UPDATE preparation_master 
            SET is_deleted = 1, updated_at = datetime('now')
            WHERE id = ?
            """
            self.db.execute_update(query, (question_id,))
            return True
        except Exception as e:
            print(f"Error deleting coding question: {e}")
            return False
    
    def search_coding_questions(self, search_query: str) -> List[Dict[str, Any]]:
        """Search coding questions"""
        if not search_query:
            return self.get_all_coding_questions()
        
        query = """
        SELECT id, question, answer, belongs_to, repeat_count, created_at, updated_at
        FROM preparation_master 
        WHERE is_deleted = 0 
        AND (belongs_to = 'Python' OR belongs_to = 'Django' OR belongs_to = 'Database' OR belongs_to = 'Pandas' OR question LIKE '%code%' OR question LIKE '%function%' OR question LIKE '%algorithm%')
        AND (LOWER(question) LIKE LOWER(?) OR LOWER(answer) LIKE LOWER(?) OR LOWER(belongs_to) LIKE LOWER(?))
        ORDER BY created_at DESC
        """
        search_pattern = f"%{search_query}%"
        return self.db.execute_query(query, (search_pattern, search_pattern, search_pattern))
    
    def get_coding_statistics(self) -> Dict[str, Any]:
        """Get statistics for coding questions"""
        query = """
        SELECT 
            COUNT(*) as total_questions,
            COUNT(CASE WHEN belongs_to = 'Python' THEN 1 END) as python_count,
            COUNT(CASE WHEN belongs_to = 'Django' THEN 1 END) as django_count,
            COUNT(CASE WHEN belongs_to = 'Database' THEN 1 END) as database_count,
            COUNT(CASE WHEN belongs_to = 'Pandas' THEN 1 END) as pandas_count,
            SUM(repeat_count) as total_repeats
        FROM preparation_master 
        WHERE is_deleted = 0 
        AND (belongs_to = 'Python' OR belongs_to = 'Django' OR belongs_to = 'Database' OR belongs_to = 'Pandas' OR question LIKE '%code%' OR question LIKE '%function%' OR question LIKE '%algorithm%')
        """
        result = self.db.execute_query(query)
        return result[0] if result else {}

# Create instance
coding_db = CodingQuestionsDBHelper(DBHelper())
