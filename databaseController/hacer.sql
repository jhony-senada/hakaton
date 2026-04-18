-- ACTIVAR EL SOPORTE PARA LLAVES FORÁNEAS (Ejecutar esto cada vez que te conectes)
PRAGMA foreign_keys = ON;

-- 1. CREACIÓN DE TABLAS INDEPENDIENTES (Catálogos)

CREATE TABLE edificios (
    id_edificio TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    ubicacion TEXT,
    url_imagen TEXT -- Puede ser NULL si no hay foto
);

CREATE TABLE profesores (
    id_profesor TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE,
    oficina TEXT,
    horario_asesoria TEXT
);

CREATE TABLE tramites (
    id_tramite TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    rol_requerido TEXT NOT NULL CHECK(rol_requerido IN ('invitado', 'usuario', 'admin'))
);

CREATE TABLE eventos_calendario (
    id_evento TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    fecha TEXT NOT NULL, -- SQLite guarda fechas como TEXT (YYYY-MM-DD)
    ubicacion TEXT,
    rol_requerido TEXT NOT NULL CHECK(rol_requerido IN ('invitado', 'usuario', 'admin'))
);

-- 2. CREACIÓN DE TABLAS DEPENDIENTES (Con Llaves Foráneas)

CREATE TABLE usuarios (
    matricula TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'invitado' CHECK(rol IN ('invitado', 'usuario', 'admin')),
    password TEXT NOT NULL, 
    id_grupo TEXT 
);

CREATE TABLE clases_horarios (
    id_clase TEXT PRIMARY KEY,
    id_grupo TEXT NOT NULL,
    materia TEXT NOT NULL,
    id_profesor TEXT NOT NULL,
    id_edificio TEXT NOT NULL,
    salon TEXT NOT NULL,
    dia TEXT NOT NULL CHECK(dia IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')),
    hora_inicio TEXT NOT NULL, -- SQLite guarda horas como TEXT (HH:MM:SS)
    hora_fin TEXT NOT NULL,
    
    -- Restricciones de integridad referencial
    CONSTRAINT fk_clase_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor) ON DELETE CASCADE,
    CONSTRAINT fk_clase_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio) ON DELETE CASCADE
);