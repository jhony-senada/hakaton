Create Database UAQ_Datos;
Using UAQ_Datos;
-- 1. CREACIÓN DE TABLAS INDEPENDIENTES (Catálogos)

CREATE TABLE edificios (
    id_edificio VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150),
    url_imagen VARCHAR(255) -- Puede ser NULL si no hay foto
);

CREATE TABLE profesores (
    id_profesor VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    oficina VARCHAR(100),
    horario_asesoria VARCHAR(150)
);

CREATE TABLE tramites (
    id_tramite VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    rol_requerido ENUM('invitado', 'usuario', 'admin') NOT NULL
);

CREATE TABLE eventos_calendario (
    id_evento VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    ubicacion VARCHAR(150),
    rol_requerido ENUM('invitado', 'usuario', 'admin') NOT NULL
);

-- 2. CREACIÓN DE TABLAS DEPENDIENTES (Con Llaves Foráneas)

CREATE TABLE usuarios (
    matricula VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('invitado', 'usuario', 'admin') NOT NULL DEFAULT 'invitado',
    id_grupo VARCHAR(50) -- Puede ser NULL para admins o invitados
);

CREATE TABLE clases_horarios (
    id_clase VARCHAR(20) PRIMARY KEY,
    id_grupo VARCHAR(50) NOT NULL,
    materia VARCHAR(100) NOT NULL,
    id_profesor VARCHAR(20) NOT NULL,
    id_edificio VARCHAR(20) NOT NULL,
    salon VARCHAR(50) NOT NULL,
    dia ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    
    -- Restricciones de integridad referencial
    CONSTRAINT fk_clase_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor) ON DELETE CASCADE,
    CONSTRAINT fk_clase_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio) ON DELETE CASCADE
);
