"""
Migration script to identify and tag existing coding questions
"""
import sqlite3
import re
from typing import List, Dict, Any

def identify_coding_questions() -> List[Dict[str, Any]]:
    """Identify coding questions from existing study materials"""
    
    # Connect to database
    conn = sqlite3.connect('instance/prod.sqlite3')
    cursor = conn.cursor()
    
    # Get all study materials
    cursor.execute("""
        SELECT id, question, answer, belongs_to, repeat_count
        FROM preparation_master 
        WHERE is_deleted = 0
        ORDER BY created_at DESC
    """)
    
    questions = cursor.fetchall()
    
    # Keywords and patterns that indicate coding questions
    coding_keywords = [
        'code', 'function', 'algorithm', 'array', 'string', 'list', 'dictionary',
        'class', 'object', 'method', 'variable', 'loop', 'conditional',
        'recursion', 'sorting', 'searching', 'data structure', 'complexity',
        'time complexity', 'space complexity', 'optimization', 'debug',
        'syntax', 'error', 'exception', 'module', 'import', 'library',
        'framework', 'api', 'database', 'sql', 'query', 'join',
        'index', 'key', 'value', 'hash', 'tree', 'graph', 'linked list',
        'stack', 'queue', 'heap', 'sorting algorithm', 'search algorithm',
        'dynamic programming', 'greedy', 'backtracking', 'divide and conquer',
        'binary search', 'linear search', 'bubble sort', 'quick sort',
        'merge sort', 'heap sort', 'depth first search', 'breadth first search',
        'dijkstra', 'fibonacci', 'factorial', 'prime', 'gcd', 'lcm'
    ]
    
    # Categories that are typically coding-related
    coding_categories = ['Python', 'Django', 'Database', 'Pandas']
    
    coding_questions = []
    
    for question in questions:
        id_, question_text, answer, category, repeat_count = question
        
        # Convert to lowercase for checking
        question_lower = question_text.lower()
        answer_lower = answer.lower()
        category_lower = category.lower() if category else ''
        
        # Check if it's a coding question
        is_coding = False
        
        # Check category
        if category_lower in [cat.lower() for cat in coding_categories]:
            is_coding = True
        
        # Check for coding keywords in question
        for keyword in coding_keywords:
            if keyword in question_lower:
                is_coding = True
                break
        
        # Check for coding keywords in answer
        if not is_coding:
            for keyword in coding_keywords:
                if keyword in answer_lower:
                    is_coding = True
                    break
        
        # Check for code patterns (using regex)
        code_patterns = [
            r'def\s+\w+\s*\(',  # Function definitions
            r'class\s+\w+\s*[:\(]',  # Class definitions
            r'import\s+\w+',  # Import statements
            r'for\s+\w+\s+in',  # For loops
            r'while\s+\w+\s*:',  # While loops
            r'if\s+.*:',  # If statements
            r'print\s*\(',  # Print statements
            r'return\s+',  # Return statements
            r'=\s*{',  # Dictionary literals
            r'=\s*\[',  # List literals
            r'\.append\(',  # List operations
            r'\.push\(',  # Array operations
            r'sql\s+',  # SQL queries
            r'select\s+.*from',  # SQL SELECT
            r'insert\s+into',  # SQL INSERT
            r'update\s+.*set',  # SQL UPDATE
            r'delete\s+from',  # SQL DELETE
        ]
        
        if not is_coding:
            for pattern in code_patterns:
                if re.search(pattern, question_lower) or re.search(pattern, answer_lower):
                    is_coding = True
                    break
        
        if is_coding:
            coding_questions.append({
                'id': id_,
                'question': question_text,
                'answer': answer,
                'belongs_to': category,
                'repeat_count': repeat_count,
                'is_coding': True
            })
    
    conn.close()
    return coding_questions

def update_coding_flags(coding_questions: List[Dict[str, Any]]) -> int:
    """Update database to mark coding questions"""
    
    conn = sqlite3.connect('instance/prod.sqlite3')
    cursor = conn.cursor()
    
    updated_count = 0
    
    for question in coding_questions:
        # Update the category to ensure it's in coding categories if not already
        category = question['belongs_to']
        if category not in ['Python', 'Django', 'Database', 'Pandas']:
            # Assign to Python as default for coding questions
            category = 'Python'
        
        # We could add a new column to mark coding questions, but for now 
        # we'll ensure they're in proper categories
        cursor.execute("""
            UPDATE preparation_master 
            SET belongs_to = ?
            WHERE id = ? AND is_deleted = 0
        """, (category, question['id']))
        
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    return updated_count

def main():
    """Main migration function"""
    print("Starting coding questions migration...")
    
    # Identify coding questions
    coding_questions = identify_coding_questions()
    
    print(f"Found {len(coding_questions)} coding questions:")
    
    for i, question in enumerate(coding_questions[:5], 1):  # Show first 5
        print(f"{i}. {question['belongs_to']}: {question['question'][:50]}...")
    
    if len(coding_questions) > 5:
        print(f"... and {len(coding_questions) - 5} more.")
    
    # Update coding flags
    updated_count = update_coding_flags(coding_questions)
    
    print(f"Updated {updated_count} questions to ensure proper categorization.")
    print("Migration completed successfully!")
    
    return coding_questions

if __name__ == '__main__':
    main()
