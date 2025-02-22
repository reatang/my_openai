

class_courses = {
    1: 'course1',
    2: 'course2',
    3: 'course3',
}

students = {
    101: 'Alice',
    102: 'Bob',
    103: 'Charlie',
    104: 'David',
    105: 'Eve',
    106: 'Frank',
}

course_students = {
    1: [101, 102, 103],
    2: [104, 105, 106],
    3: [101, 103, 105],
    4: [102, 104, 106],
}

def get_courses():
    return list(class_courses.keys())

def get_course_info(course_id: int):
    course = class_courses.get(course_id, "Unknown")
    students = course_students.get(course_id, [])

    return {
        "id": course_id,
        "name": course,
        "students": students,
    }

def get_student_info(student_id: int):
    student = students.get(student_id, "Unknown")

    return {
        "id": student_id,
        "name": student,
    }