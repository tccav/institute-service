-- migrate:up

CREATE TABLE IF NOT EXISTS subjects
(
	id                            bigint PRIMARY KEY,
	name                          varchar NOT NULL,
	department_id                 uuid    NOT NULL,
	credits                       int     NOT NULL,
	workload_hours_total          int     NOT NULL,
	workload_hours_per_week       int     NOT NULL,
	is_universal                  bool    NOT NULL,
	permits_agenda_conflict       bool    NOT NULL,
	permits_preparation_situation bool    NOT NULL,
	credits_requirements          int     NOT NULL,
	approval_type                 varchar NOT NULL,
	CONSTRAINT fk_departments FOREIGN KEY (department_id) REFERENCES departments (id)
);

-- migrate:down

DROP TABLE IF EXISTS subjects;