-- Crear base de datos
CREATE DATABASE IF NOT EXISTS imdb_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE imdb_demo;

-- Tabla de películas
CREATE TABLE peliculas (
    id VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(255),
    tipo VARCHAR(50),
    anio_estreno INT,
    duracion INT,
    genero VARCHAR(100)
);

-- Tabla de personas
CREATE TABLE personas (
    id VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(255),
    nacimiento INT,
    profesion VARCHAR(255)
);

-- Relación entre personas y películas (actores, directores, etc.)
CREATE TABLE actores_peliculas (
    id_pelicula VARCHAR(20),
    id_persona VARCHAR(20),
    rol VARCHAR(100),
    PRIMARY KEY (id_pelicula, id_persona, rol),
    FOREIGN KEY (id_pelicula) REFERENCES peliculas(id),
    FOREIGN KEY (id_persona) REFERENCES personas(id)
);

-- Ratings de películas
CREATE TABLE ratings (
    id_pelicula VARCHAR(20) PRIMARY KEY,
    promedio DECIMAL(3, 1),
    votos INT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas(id)
);
