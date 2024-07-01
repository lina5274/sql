import sqlite3 as sl


class University:
    def __init__(self, name_u):
        self.name_u = name_u
        self.conn = sl.connect('Students.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    subject TEXT,
                    grade REAL,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                );
            """)

    def add_student(self, name, age):
        if name != "" and age > 0:
            with self.conn:
                self.conn.execute("INSERT INTO students (name, age) VALUES (?, ?);", (name, age))

    def add_grade(self, student_id, subject, grade):
        if student_id > 0 and subject != "" and grade > 0:
            with self.conn:
                self.conn.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?);",
                                  (student_id, subject, grade))

    def get_students(self, subject=None):
        query = """
            SELECT s.id, s.name, s.age, g.subject, g.grade 
            FROM students s 
            LEFT JOIN grades g ON s.id = g.student_id
        """
        if subject:
            query += " WHERE g.subject = ?"
            rows = self.conn.execute(query, (subject,)).fetchall()
        else:
            rows = self.conn.execute(query).fetchall()

        students = []
        for row in rows:
            students.append({
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'subject': row[3],
                'grade': row[4]
            })
        return students


un = University('Urban')

un.add_student('Vlad', 25)
un.add_student('Ilya', 30)
un.add_student('Olga', 23)
un.add_student('Oleg', 35)

un.add_grade(1, 'Python', 4.8)
un.add_grade(1, 'PHP', 4.3)
un.add_grade(2, 'IOS', 4.2)
un.add_grade(2, 'Python', 5.0)
un.add_grade(3, 'Python', 4.6)
un.add_grade(3, 'PHP', 4.0)
un.add_grade(4, 'IOS', 4.9)
un.add_grade(4, 'Python', 4.7)

print(un.get_students())
print(un.get_students('Python'))