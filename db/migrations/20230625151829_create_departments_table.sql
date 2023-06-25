-- migrate:up

CREATE TABLE IF NOT EXISTS departments
(
	id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	name       varchar NOT NULL,
	faculty_id uuid    NOT NULL,
	CONSTRAINT fk_faculties FOREIGN KEY (faculty_id) REFERENCES faculties (id)
);

-- migrate:down

DROP TABLE IF EXISTS departments;