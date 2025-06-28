CREATE DATABASE IF NOT EXISTS books_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE books_demo;

CREATE TABLE libros (
    isbn VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(255),
    autor VARCHAR(255),
    anio_publicacion INT,
    editorial VARCHAR(255)
);

CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY,
    localidad VARCHAR(255),
    pais VARCHAR(255),
    edad INT
);

CREATE TABLE valoraciones (
    id_usuario INT,
    isbn VARCHAR(20),
    puntuacion INT,
    PRIMARY KEY (id_usuario, isbn),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (isbn) REFERENCES libros(isbn)
);
