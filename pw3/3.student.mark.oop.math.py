import math
import numpy as np
import curses
class Entity:
    def input(self, stdscr):
        pass

    def display(self, stdscr):
        pass
class Student(Entity):
    def __init__(self, s_id="", name="", dob=""):
        self.__id = s_id
        self.__name = name
        self.__dob = dob
        self.__gpa = 0.0
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_dob(self):
        return self.__dob
    def get_gpa(self):
        return self.__gpa
    def set_gpa(self, gpa):
        self.__gpa = gpa
class Course(Entity):
    def __init__(self, c_id="", name="", credits=0):
        self.__id = c_id
        self.__name = name
        self.__credits = credits
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_credits(self):
        return self.__credits
class StudentMarkSystem:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {} 

    def get_input_str(self, stdscr, prompt):
        """Helper function to get text input using curses."""
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        curses.echo()
        input_bytes = stdscr.getstr(1, 0)
        curses.noecho()
        return input_bytes.decode('utf-8').strip()
    def input_student(self, stdscr):
        try:
            n_str = self.get_input_str(stdscr, "Enter number of students: ")
            n = int(n_str)
        except ValueError:
            return
        for i in range(n):
            stdscr.clear()
            stdscr.addstr(0, 0, f"--- Enter info for student {i + 1}/{n} ---")
            
            s_id = self.get_input_str(stdscr, "Student ID: ")
            s_name = self.get_input_str(stdscr, "Student Name: ")
            s_dob = self.get_input_str(stdscr, "Date of Birth (dd/mm/yyyy): ")

            student = Student(s_id, s_name, s_dob)
            self.__students.append(student)
    def input_course(self, stdscr):
        try:
            c_str = self.get_input_str(stdscr, "Enter number of courses: ")
            c = int(c_str)
        except ValueError:
            return
        for i in range(c):
            stdscr.clear()
            stdscr.addstr(0, 0, f"--- Enter info for course {i + 1}/{c} ---")
            c_id = self.get_input_str(stdscr, "Course ID: ")
            c_name = self.get_input_str(stdscr, "Course Name: ")
            
            try:
                c_credits = int(self.get_input_str(stdscr, "Credits: "))
            except ValueError:
                c_credits = 0

            course = Course(c_id, c_name, c_credits)
            self.__courses.append(course)

    def input_marks(self, stdscr):
        if not self.__courses or not self.__students:
            stdscr.clear()
            stdscr.addstr(0, 0, "Please input students and courses first! Press any key...")
            stdscr.getch()
            return

        cid = self.get_input_str(stdscr, "Enter course ID to input marks: ")
        course_found = any(c.get_id() == cid for c in self.__courses)

        if not course_found:
            stdscr.clear()
            stdscr.addstr(0, 0, "Course ID not found! Press any key...")
            stdscr.getch()
            return

        for s in self.__students:
            try:
                raw_mark = float(self.get_input_str(
                    stdscr, 
                    f"Enter mark for {s.get_name()} (ID: {s.get_id()}): "
                ))
                floor_mark = math.floor(raw_mark * 10) / 10.0
                self.__marks[(cid, s.get_id())] = floor_mark
            except ValueError:
                continue

    def calculate_gpa(self):
        """Calculate weighted GPA for each student using NumPy arrays."""
        for s in self.__students:
            marks_list = []
            credits_list = []

            for c in self.__courses:
                key = (c.get_id(), s.get_id())
                if key in self.__marks:
                    marks_list.append(self.__marks[key])
                    credits_list.append(c.get_credits())

            if credits_list and sum(credits_list) > 0:
                np_marks = np.array(marks_list)
                np_credits = np.array(credits_list)
                gpa = np.sum(np_marks * np_credits) / np.sum(np_credits)
                s.set_gpa(round(gpa, 2))
            else:
                s.set_gpa(0.0)

    def sort_students_by_gpa(self):
        """Sort students by GPA descending."""
        self.calculate_gpa()
        self.__students.sort(key=lambda s: s.get_gpa(), reverse=True)

    def list_students(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "=== STUDENT LIST (SORTED BY GPA DESCENDING) ===")

        if not self.__students:
            stdscr.addstr(2, 0, "No students found!")
        else:
            self.sort_students_by_gpa()
            line = 2
            for s in self.__students:
                stdscr.addstr(
                    line, 0, 
                    f"ID: {s.get_id()} | Name: {s.get_name()} | DoB: {s.get_dob()} | GPA: {s.get_gpa():.2f}"
                )
                line += 1

        stdscr.addstr(line + 1, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()

    def list_courses(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "=== COURSE LIST ===")

        if not self.__courses:
            stdscr.addstr(2, 0, "No courses found!")
        else:
            line = 2
            for c in self.__courses:
                stdscr.addstr(
                    line, 0, 
                    f"ID: {c.get_id()} | Name: {c.get_name()} | Credits: {c.get_credits()}"
                )
                line += 1

        stdscr.addstr(line + 1, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()

    def show_marks(self, stdscr):
        if not self.__courses or not self.__students:
            stdscr.clear()
            stdscr.addstr(0, 0, "No data available! Press any key...")
            stdscr.getch()
            return

        cid = self.get_input_str(stdscr, "Enter course ID to view marks: ")
        stdscr.clear()
        stdscr.addstr(0, 0, f"=== MARKS FOR COURSE [{cid}] ===")

        line = 2
        has_marks = False
        for s in self.__students:
            key = (cid, s.get_id())
            if key in self.__marks:
                stdscr.addstr(
                    line, 0, 
                    f"Student: {s.get_name()} (ID: {s.get_id()}) -> Mark: {self.__marks[key]}"
                )
                line += 1
                has_marks = True

        if not has_marks:
            stdscr.addstr(line, 0, "No marks recorded for this course!")
            line += 1

        stdscr.addstr(line + 1, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()

    def main_menu(self, stdscr):
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "================ STUDENT MARK SYSTEM ================")
            stdscr.addstr(1, 0, "1. Input students")
            stdscr.addstr(2, 0, "2. Input courses")
            stdscr.addstr(3, 0, "3. Input marks for a course")
            stdscr.addstr(4, 0, "4. List students (sorted by GPA descending)")
            stdscr.addstr(5, 0, "5. List courses")
            stdscr.addstr(6, 0, "6. Show marks for a course")
            stdscr.addstr(7, 0, "0. Exit")
            stdscr.addstr(9, 0, "Your choice (0-7): ")
            stdscr.refresh()

            choice = stdscr.getkey()

            if choice == '1':
                self.input_student(stdscr)
            elif choice == '2':
                self.input_course(stdscr)
            elif choice == '3':
                self.input_marks(stdscr)
            elif choice == '4':
                self.list_students(stdscr)
            elif choice == '5':
                self.list_courses(stdscr)
            elif choice == '6':
                self.show_marks(stdscr)
            elif choice == '0':
                break


def main(stdscr):
    system = StudentMarkSystem()
    system.main_menu(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)