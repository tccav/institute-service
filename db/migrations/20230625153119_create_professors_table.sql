-- migrate:up

CREATE TABLE IF NOT EXISTS professors
(
	id            bigint PRIMARY KEY,
	name          varchar NOT NULL,
	cpf           varchar NOT NULL,
	email         varchar NOT NULL,
	department_id uuid    NOT NULL,
	CONSTRAINT fk_departments FOREIGN KEY (department_id) REFERENCES departments (id)
);

-- migrate:down

DROP TABLE IF EXISTS professors;