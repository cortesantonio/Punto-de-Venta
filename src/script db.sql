create database puntodeventa;

use puntodeventa;

create table Estado_Jornada(
	id_Jornada date,
	Estado varchar(50),
    primary key (id_Jornada)
);

create table Tipo_Usuario(
	id int,
	tipo varchar(50),
    primary key (id)
);
create table Usuario(
	rut varchar(50),
    password varchar(200),
    nombre varchar(200),
    id_TipoUsuario int,
    primary key (rut),
    FOREIGN KEY (id_TipoUsuario) REFERENCES Tipo_Usuario(id)
);


create table Producto(
	id int,
    nombre varchar(200),
    descripcion varchar(255),
    precio int,
    primary key (id)
);


create table Boleta(
	id int,
	detalles text, 
	total int,
	fecha date,
    vendedor_emisor varchar(30),
	primary key (id)
);


create table Factura(
	id int,
	razon_social varchar(200),
	rut varchar(200),
	direccion varchar(200),
	detalles text, 
	giro int,
	iva int,
	neto int,
	fecha date,
	vendedor_emisor varchar(30),

	primary key (id)
);

create table Informe(
	fecha date,
    id_Facturas int,
    id_boletas int,
    ventaTotal int,
    ventaTotal_Facturas int,
	ventaTotal_Boletas int,
    primary key (fecha),
    FOREIGN KEY (id_Facturas) REFERENCES Factura(id),
    FOREIGN KEY (id_Boletas) REFERENCES Boleta(id)

);

create table jornada(
	fecha date,
    id_informe date,
    trabajador varchar(255),
    EstadoJornada date,
    primary key (fecha),
	FOREIGN KEY (id_informe) REFERENCES Informe(fecha),
    FOREIGN KEY (EstadoJornada) REFERENCES Estado_Jornada(id_Jornada)

);
