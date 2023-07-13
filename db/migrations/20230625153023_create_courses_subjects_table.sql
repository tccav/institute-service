-- migrate:up

CREATE TABLE IF NOT EXISTS courses_subjects
(
	course_id  uuid    NOT NULL,
	subject_id bigint NOT NULL,
	type varchar NOT NULL,
	period int NOT NULL,
	CONSTRAINT fk_courses FOREIGN KEY (course_id) REFERENCES courses (id),
	CONSTRAINT fk_subjects FOREIGN KEY (subject_id) REFERENCES subjects (id)
);

-- migrate:down

DROP TABLE IF EXISTS courses_subjects;