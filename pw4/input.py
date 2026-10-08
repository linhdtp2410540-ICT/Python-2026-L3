import math
import curses
from domains.student import Student
from domains.course import Course

def get_input_str(stdscr, prompt):
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    curses.echo()
    input_bytes = stdscr.getstr(1, 0)
    curses.noecho()
    return input_bytes.decode('utf-8').strip()

def input_students(stdscr, students):
    try:
        n_str = get_input_str(stdscr, "Enter number of students: ")
        n = int(n_str)
    except ValueError:
        return

    for i in range(n):
        stdscr.clear()
        stdscr.addstr(0, 0, f"--- Enter info for student {i + 1}/{n} ---")
        
        s_id = get_input_str(stdscr, "Student ID: ")
        s_name = get_input_str(stdscr, "Student Name: ")
        s_dob = get_input_str(stdscr, "Date of Birth (dd/mm/yyyy): ")

        students.append(Student(s_id, s_name, s_dob))

def input_courses(stdscr, courses):
    try:
        c_str = get_input_str(stdscr, "Enter number of courses: ")
        c = int(c_str)
    except ValueError:
        return

    for i in range(c):
        stdscr.clear()
        stdscr.addstr(0, 0, f"--- Enter info for course {i + 1}/{c} ---")
        
        c_id = get_input_str(stdscr, "Course ID: ")
        c_name = get_input_str(stdscr, "Course Name: ")
        
        try:
            c_credits = int(get_input_str(stdscr, "Credits: "))
        except ValueError:
            c_credits = 0

        courses.append(Course(c_id, c_name, c_credits))

def input_marks(stdscr, students, courses, marks):
    if not courses or not students:
        stdscr.clear()
        stdscr.addstr(0, 0, "Please input students and courses first! Press any key...")
        stdscr.getch()
        return

    cid = get_input_str(stdscr, "Enter course ID to input marks: ")
    course_found = any(c.get_id() == cid for c in courses)

    if not course_found:
        stdscr.clear()
        stdscr.addstr(0, 0, "Course ID not found! Press any key...")
        stdscr.getch()
        return

    for s in students:
        try:
            raw_mark = float(get_input_str(
                stdscr, 
                f"Enter mark for {s.get_name()} (ID: {s.get_id()}): "
            ))
            floor_mark = math.floor(raw_mark * 10) / 10.0
            marks[(cid, s.get_id())] = floor_mark
        except ValueError:
            continue