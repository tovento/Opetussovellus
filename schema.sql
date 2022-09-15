CREATE TABLE Users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	teacher BOOLEAN
);

CREATE TABLE Courses (
	id SERIAL PRIMARY KEY,
	name TEXT,
	teacher_id INTEGER REFERENCES Users
);

CREATE TABLE Registrations (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES Courses,
	student_id INTEGER REFERENCES Users
);

CREATE TABLE Tasks (
	id SERIAL PRIMARY KEY,
	course_id INTEGER REFERENCES Courses,
	question TEXT,
	created_at TIMESTAMP
);

CREATE TABLE Completions (
	id SERIAL PRIMARY KEY,
	student_id INTEGER REFERENCES Users,
	task_id INTEGER REFERENCES Tasks	
);

CREATE TABLE Choices (
	id SERIAL PRIMARY KEY,
	task_id INTEGER REFERENCES Tasks,
	choice TEXT,
	correct BOOLEAN
);

CREATE TABLE Answers (
	id SERIAL PRIMARY KEY,
	task_id INTEGER REFERENCES Tasks,
	student_id INTEGER REFERENCES Users,
	answer TEXT
);
