-- migrate:up

CREATE TABLE IF NOT EXISTS faculties
(
	id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	name varchar NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS faculties;