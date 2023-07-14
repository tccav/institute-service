DO
$$
	DECLARE
		ime_id             faculties.id%type;
		comp_dep_id        departments.id%type;
		comp_course_id     courses.id%type;
	BEGIN

		-- populate faculties
		INSERT INTO faculties (name)
		VALUES ('Instituto de Matemática e Estatística')
		RETURNING id INTO ime_id;

		RAISE NOTICE 'IME_ID: %', ime_id;

		-- populate departments
		INSERT INTO departments (name, faculty_id)
		VALUES ('Análise Matemática', ime_id),
			   ('Estruturas Matemáticas', ime_id),
			   ('Geometria e Representação Gráfica', ime_id),
			   ('Informática e Ciências da Computação', ime_id),
			   ('Estatística', ime_id),
			   ('Matemática Aplicada', ime_id);

		SELECT id FROM departments WHERE name = 'Informática e Ciências da Computação' INTO comp_dep_id;

		RAISE NOTICE 'COMP_DEP_ID: %', comp_dep_id;


		-- populate courses
		INSERT INTO courses (name, faculty_id, minimum_periods_qty, maximum_periods_qty)
		VALUES ('Ciências da Computação - Maracanã', ime_id, 8, 14)
		RETURNING id INTO comp_course_id;

		-- populate subjects
		INSERT INTO subjects (id,
							  name,
							  department_id,
							  credits,
							  workload_hours_total,
							  workload_hours_per_week,
							  is_universal,
							  permits_agenda_conflict,
							  permits_preparation_situation,
							  credits_requirements,
							  approval_type)
		VALUES (10817, 'Fundamentos da Computação', comp_dep_id, 5, 90, 6, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10820, 'Algoritmos e Estruturas de Dados I', comp_dep_id, 6, 90, 6, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10821, 'Linguagem de Programação I', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10832, 'Banco de Dados I', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10838, 'Banco de Dados II', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10839, 'Interfaces Humano-Computador', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10835, 'Sistemas Operacionais I', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10840, 'Sistemas Operacionais II', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10826, 'Teoria da Computação', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10841, 'Compiladores', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE'),
			   (10849, 'Sistemas Distribuídos', comp_dep_id, 4, 60, 4, FALSE, FALSE, FALSE, 0, 'GRADE');

		-- populate requirements_subjects
		INSERT INTO requirements_subjects (subject_id, depends_on_subject_id)
		VALUES (10820, 10817),
			   (10821, 10817),
			   (10838, 10832),
			   (10840, 10835),
			   (10849, 10835),
			   (10841, 10826);

		-- populate courses_subjects
		INSERT INTO courses_subjects (course_id, subject_id, type, period)
		VALUES (comp_course_id, 10817, 'Obrigatória', 1),
			   (comp_course_id, 10820, 'Obrigatória', 2),
			   (comp_course_id, 10821, 'Obrigatória', 2),
			   (comp_course_id, 10832, 'Obrigatória', 5),
			   (comp_course_id, 10838, 'Obrigatória', 6),
			   (comp_course_id, 10839, 'Obrigatória', 6),
			   (comp_course_id, 10835, 'Obrigatória', 5),
			   (comp_course_id, 10840, 'Obrigatória', 6),
			   (comp_course_id, 10826, 'Obrigatória', 3),
			   (comp_course_id, 10841, 'Obrigatória', 6),
			   (comp_course_id, 10849, 'Obrigatória', 8);

		-- populate professors
		INSERT INTO professors (id, name, cpf, email, department_id)
		VALUES (20230521123, 'Eduardo Gonçalves Galúcio', '11111111030', 'eduardo.galucio@ime.uerj.br', comp_dep_id),
			   (20230521124, 'Flavia Maria Santoro', '72138242013', 'flavia.santoro@ime.uerj.br', comp_dep_id),
			   (20230521125, 'Claudia Cappeli Alo', '53766141074', 'claudia.cappeli@ime.uerj.br', comp_dep_id),
			   (20230521126, 'Lis Ingrid Roque Lopes Custódio', '71188595083', 'liscustodio@ime.uerj.br', comp_dep_id),
			   (20230521127, 'Alexandre Sztajnberg', '52806950090', 'alexszt@ime.uerj.br', comp_dep_id),
			   (20230521128, 'Ana Carolina Brito de Almeida', '58152032034', 'ana.almeida@ime.uerj.br', comp_dep_id),
			   (20230521129, 'Vera Maria Benjamim Werneck', '99717946086', 'vera@ime.uerj.br', comp_dep_id);
		COMMIT;
	END;
$$