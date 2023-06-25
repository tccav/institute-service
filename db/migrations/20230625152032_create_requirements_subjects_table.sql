-- migrate:up

CREATE TABLE IF NOT EXISTS requirements_subjects
(
	id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
	subject_id            bigint NOT NULL,
	depends_on_subject_id bigint NOT NULL,
	UNIQUE (subject_id, depends_on_subject_id),
	CONSTRAINT fk_subjects FOREIGN KEY(subject_id) REFERENCES subjects(id)
);

CREATE INDEX IF NOT EXISTS idx_requirements_subjects_subject_id ON requirements_subjects USING hash (subject_id);
CREATE INDEX IF NOT EXISTS idx_requirements_subjects_depends_on_subject_id ON requirements_subjects USING hash (depends_on_subject_id);

-- migrate:down

DROP INDEX IF EXISTS idx_requirements_subjects_depends_on_subject_id;
DROP INDEX IF EXISTS idx_requirements_subjects_subject_id;

DROP TABLE IF EXISTS requirements_subjects;