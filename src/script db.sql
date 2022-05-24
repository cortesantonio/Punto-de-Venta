CREATE DATABASE puntodeventa;

USE puntodeventa;

CREATE TABLE usuario(
    rut VARCHAR(16),
    password VARCHAR(255),
    nombre VARCHAR(200),
    rol int(1),
    PRIMARY KEY(rut)
);

CREATE TABLE producto(
    codigo int(11),
    nombre VARCHAR(50),
    descripcion VARCHAR(255),
    precio int(10),
    url_img VARCHAR(255)
    PRIMARY KEY(codigo)
);
