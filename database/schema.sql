-- ============================================================
-- IBS STUDENT MANAGEMENT SYSTEM
-- Database: SQLite
-- File: database/schema.sql
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    full_name TEXT NOT NULL,

    role TEXT NOT NULL
        CHECK (role IN ('admin', 'staff')),

    email TEXT UNIQUE,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. DEPARTMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,

    department_code TEXT NOT NULL UNIQUE,

    department_name TEXT NOT NULL UNIQUE,

    description TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 3. ACADEMIC TERMS
-- ============================================================

CREATE TABLE IF NOT EXISTS academic_terms (
    term_id INTEGER PRIMARY KEY AUTOINCREMENT,

    term_name TEXT NOT NULL,

    academic_year INTEGER NOT NULL,

    start_date TEXT NOT NULL,

    end_date TEXT NOT NULL,

    is_current INTEGER NOT NULL DEFAULT 0
        CHECK (is_current IN (0, 1)),

    UNIQUE (term_name, academic_year),

    CHECK (date(start_date) < date(end_date))
);


-- ============================================================
-- 4. STUDENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_number TEXT NOT NULL UNIQUE,

    first_name TEXT NOT NULL,

    middle_name TEXT,

    last_name TEXT NOT NULL,

    date_of_birth TEXT,

    gender TEXT
        CHECK (gender IN ('Male', 'Female', 'Other')),

    email TEXT UNIQUE,

    phone TEXT,

    address TEXT,

    department_id INTEGER,

    enrollment_year INTEGER NOT NULL,

    status TEXT NOT NULL DEFAULT 'Active'
        CHECK (
            status IN (
                'Active',
                'Inactive',
                'Graduated',
                'Suspended',
                'Withdrawn'
            )
        ),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);


-- ============================================================
-- 5. COURSES
-- ============================================================

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_code TEXT NOT NULL UNIQUE,

    course_name TEXT NOT NULL,

    description TEXT,

    credit_hours INTEGER NOT NULL
        CHECK (credit_hours > 0),

    department_id INTEGER NOT NULL,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


-- ============================================================
-- 6. ENROLLMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,

    course_id INTEGER NOT NULL,

    term_id INTEGER NOT NULL,

    enrollment_date TEXT NOT NULL DEFAULT CURRENT_DATE,

    status TEXT NOT NULL DEFAULT 'Enrolled'
        CHECK (
            status IN (
                'Enrolled',
                'Completed',
                'Dropped',
                'Withdrawn'
            )
        ),

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (term_id)
        REFERENCES academic_terms(term_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (student_id, course_id, term_id)
);


-- ============================================================
-- 7. GRADES
-- ============================================================

CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,

    enrollment_id INTEGER NOT NULL UNIQUE,

    assessment_score REAL
        CHECK (
            assessment_score IS NULL
            OR (
                assessment_score >= 0
                AND assessment_score <= 100
            )
        ),

    exam_score REAL
        CHECK (
            exam_score IS NULL
            OR (
                exam_score >= 0
                AND exam_score <= 100
            )
        ),

    final_score REAL
        CHECK (
            final_score IS NULL
            OR (
                final_score >= 0
                AND final_score <= 100
            )
        ),

    grade_letter TEXT
        CHECK (
            grade_letter IS NULL
            OR grade_letter IN (
                'A',
                'B',
                'C',
                'D',
                'E',
                'F'
            )
        ),

    grade_point REAL
        CHECK (
            grade_point IS NULL
            OR (
                grade_point >= 0
                AND grade_point <= 4
            )
        ),

    remarks TEXT,

    graded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (enrollment_id)
        REFERENCES enrollments(enrollment_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- ============================================================
-- 8. INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_students_last_name
    ON students(last_name);

CREATE INDEX IF NOT EXISTS idx_students_department
    ON students(department_id);

CREATE INDEX IF NOT EXISTS idx_students_status
    ON students(status);

CREATE INDEX IF NOT EXISTS idx_courses_department
    ON courses(department_id);

CREATE INDEX IF NOT EXISTS idx_enrollments_student
    ON enrollments(student_id);

CREATE INDEX IF NOT EXISTS idx_enrollments_course
    ON enrollments(course_id);

CREATE INDEX IF NOT EXISTS idx_enrollments_term
    ON enrollments(term_id);

CREATE INDEX IF NOT EXISTS idx_grades_enrollment
    ON grades(enrollment_id);

CREATE INDEX IF NOT EXISTS idx_users_role
    ON users(role);

CREATE INDEX IF NOT EXISTS idx_users_active
    ON users(is_active);


-- ============================================================
-- 9. INITIAL DEPARTMENTS
-- ============================================================

INSERT OR IGNORE INTO departments
    (department_code, department_name, description)
VALUES
    (
        'SIT',
        'School of Information Technology',
        'Information Technology and computing programs'
    );

INSERT OR IGNORE INTO departments
    (department_code, department_name, description)
VALUES
    (
        'SOB',
        'School of Business',
        'Business and management programs'
    );

INSERT OR IGNORE INTO departments
    (department_code, department_name, description)
VALUES
    (
        'SOE',
        'School of Economics',
        'Economics and related programs'
    );


-- ============================================================
-- 10. INITIAL ACADEMIC TERM
-- ============================================================

INSERT OR IGNORE INTO academic_terms
    (
        term_name,
        academic_year,
        start_date,
        end_date,
        is_current
    )
VALUES
    (
        'Semester 1',
        2026,
        '2026-01-01',
        '2026-06-30',
        0
    );

INSERT OR IGNORE INTO academic_terms
    (
        term_name,
        academic_year,
        start_date,
        end_date,
        is_current
    )
VALUES
    (
        'Semester 2',
        2026,
        '2026-07-01',
        '2026-12-31',
        1
    );