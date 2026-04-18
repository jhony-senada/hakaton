USE UAQ_Datos;

-- 1. EDIFICIOS
INSERT INTO edificios (id_edificio, nombre, ubicacion, url_imagen) VALUES
('EDIF-FIF', 'Facultad de Informática', 'Campus Juriquilla', 'https://ejemplo.com/img/fif.jpg'),
('EDIF-REC', 'Edificio de Rectoría', 'Campus Cerro de las Campanas', 'https://ejemplo.com/img/rectoria.jpg'),
('EDIF-BIB', 'Biblioteca Central', 'Campus Cerro de las Campanas', NULL);

-- 2. PROFESORES
INSERT INTO profesores (id_profesor, nombre, correo, oficina, horario_asesoria) VALUES
('PROF-101', 'Dr. Alejandro Martínez', 'amartinez@uaq.mx', 'Cubículo 5, FIF', 'Lunes y Miércoles 10:00 - 12:00'),
('PROF-102', 'Mtra. Silvia Ruiz', 'sruiz@uaq.mx', 'Cubículo 8, FIF', 'Martes 14:00 - 16:00'),
('PROF-103', 'Ing. Carlos López', 'clopez@uaq.mx', 'Sala de Maestros, FIF', 'Viernes 09:00 - 11:00');

-- 3. TRÁMITES (Con filtros de acceso)
INSERT INTO tramites (id_tramite, titulo, descripcion, rol_requerido) VALUES
('TRM-001', 'Proceso de Admisión y EXCOBA', 'Requisitos y fechas para aspirantes de nuevo ingreso...', 'invitado'),
('TRM-002', 'Registro de Servicio Social', 'Formatos para dar de alta el servicio social en el sistema...', 'usuario'),
('TRM-003', 'Gestión de Carga Académica', 'Módulo interno para asignar materias a los grupos del semestre...', 'admin');

-- 4. EVENTOS Y CALENDARIO (Con filtros de acceso)
INSERT INTO eventos_calendario (id_evento, titulo, tipo, fecha, ubicacion, rol_requerido) VALUES
('EVT-001', 'Feria de Orientación Vocacional', 'voluntarios', '2026-05-10', 'Explanada de Rectoría', 'invitado'),
('EVT-002', 'Día del Estudiante', 'sin_clase', '2026-05-23', 'Múltiples Sedes', 'usuario'),
('EVT-003', 'Cierre de Actas y Evaluaciones', 'administrativo', '2026-06-15', 'Plataforma Docente', 'admin');

-- 5. USUARIOS (Tus tres niveles de acceso)
INSERT INTO usuarios (matricula, nombre, rol, id_grupo) VALUES
('UAQ-ADMIN', 'Coordinación Académica', 'admin', NULL),
('UAQ-345678', 'José Carlos Cabello Silva', 'usuario', 'ISW-4A'),
('INV-001', 'Visitante General', 'invitado', NULL);

-- 6. CLASES Y HORARIOS (Ligados al grupo ISW-4A)
INSERT INTO clases_horarios (id_clase, id_grupo, materia, id_profesor, id_edificio, salon, dia, hora_inicio, hora_fin) VALUES
('CLS-001', 'ISW-4A', 'Ingeniería de Software', 'PROF-101', 'EDIF-FIF', 'Aula 10', 'Lunes', '08:00:00', '10:00:00'),
('CLS-002', 'ISW-4A', 'Bases de Datos Avanzadas', 'PROF-102', 'EDIF-FIF', 'Lab Cómputo 3', 'Martes', '11:00:00', '13:00:00'),
('CLS-003', 'ISW-4A', 'Desarrollo de Aplicaciones Web', 'PROF-103', 'EDIF-FIF', 'Lab Cómputo 1', 'Miércoles', '08:00:00', '10:00:00');