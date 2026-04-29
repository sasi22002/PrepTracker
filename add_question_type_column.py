"""
Migration script to add question_type column to preparation_master table
"""
import sqlite3

def add_question_type_column():
    """Add question_type column to preparation_master table"""
    try:
        # Connect to database
        conn = sqlite3.connect('instance/prod.sqlite3')
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(preparation_master)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'question_type' not in columns:
            # Add the column
            cursor.execute("""
                ALTER TABLE preparation_master 
                ADD COLUMN question_type TEXT DEFAULT 'theory'
            """)
            
            # Update existing coding questions based on content analysis
            cursor.execute("""
                UPDATE preparation_master 
                SET question_type = 'coding' 
                WHERE is_deleted = 0 
                AND (
                    belongs_to IN ('Python', 'Django', 'Database', 'Pandas')
                    OR (
                        LOWER(question) LIKE '%code%' 
                        OR LOWER(question) LIKE '%function%'
                        OR LOWER(question) LIKE '%algorithm%'
                        OR LOWER(question) LIKE '%class%'
                        OR LOWER(question) LIKE '%method%'
                        OR LOWER(question) LIKE '%variable%'
                        OR LOWER(question) LIKE '%loop%'
                        OR LOWER(question) LIKE '%conditional%'
                        OR LOWER(question) LIKE '%recursion%'
                        OR LOWER(question) LIKE '%sorting%'
                        OR LOWER(question) LIKE '%search%'
                        OR LOWER(question) LIKE '%data structure%'
                        OR LOWER(question) LIKE '%complexity%'
                        OR LOWER(question) LIKE '%debug%'
                        OR LOWER(question) LIKE '%syntax%'
                        OR LOWER(question) LIKE '%exception%'
                        OR LOWER(question) LIKE '%module%'
                        OR LOWER(question) LIKE '%import%'
                        OR LOWER(question) LIKE '%library%'
                        OR LOWER(question) LIKE '%framework%'
                        OR LOWER(question) LIKE '%api%'
                        OR LOWER(question) LIKE '%sql%'
                        OR LOWER(question) LIKE '%query%'
                        OR LOWER(question) LIKE '%join%'
                        OR LOWER(question) LIKE '%index%'
                        OR LOWER(question) LIKE '%key%'
                        OR LOWER(question) LIKE '%value%'
                        OR LOWER(question) LIKE '%hash%'
                        OR LOWER(question) LIKE '%tree%'
                        OR LOWER(question) LIKE '%graph%'
                        OR LOWER(question) LIKE '%linked list%'
                        OR LOWER(question) LIKE '%stack%'
                        OR LOWER(question) LIKE '%queue%'
                        OR LOWER(question) LIKE '%heap%'
                        OR LOWER(question) LIKE '%array%'
                        OR LOWER(question) LIKE '%string%'
                        OR LOWER(question) LIKE '%list%'
                        OR LOWER(question) LIKE '%dictionary%'
                        OR LOWER(question) LIKE '%tuple%'
                        OR LOWER(question) LIKE '%set%'
                        OR LOWER(answer) LIKE '%def %'
                        OR LOWER(answer) LIKE '%class %'
                        OR LOWER(answer) LIKE '%import %'
                        OR LOWER(answer) LIKE '%for %'
                        OR LOWER(answer) LIKE '%while %'
                        OR LOWER(answer) LIKE '%if %:'
                        OR LOWER(answer) LIKE '%print(%'
                        OR LOWER(answer) LIKE '%return %'
                    )
                )
            """)
            
            conn.commit()
            print("Successfully added question_type column and updated existing records")
            
            # Show statistics
            cursor.execute("""
                SELECT 
                    question_type,
                    COUNT(*) as count
                FROM preparation_master 
                WHERE is_deleted = 0
                GROUP BY question_type
            """)
            
            results = cursor.fetchall()
            print("\nQuestion type distribution:")
            for row in results:
                print(f"  {row[0]}: {row[1]} questions")
                
        else:
            print("question_type column already exists")
            
        conn.close()
        
    except Exception as e:
        print(f"Error adding question_type column: {e}")
        if conn:
            conn.close()

if __name__ == '__main__':
    add_question_type_column()
