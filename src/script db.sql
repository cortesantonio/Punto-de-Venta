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
    rol int,
    primary key (rut),
    FOREIGN KEY (rol) REFERENCES Tipo_Usuario(id)
);



create table categoria_Producto(
	id int,
    categoria varchar(200),
    primary key(id)

);

create table Producto(
	id int,
    nombre varchar(200),
    descripcion varchar(255),
    precio int,
    img text,
    id_categoria int,
    primary key (id),
	FOREIGN KEY (id_categoria) REFERENCES categoria_Producto(id)

);

create table cliente(
	rut varchar(200),
    primary key(rut)
)
;
create table Boleta(
	id int,
	total int,
	fecha date,
    iva int,
    id_cliente varchar(200),
    vendedor_emisor varchar(50),
	primary key (id),
	FOREIGN KEY (vendedor_emisor) REFERENCES usuario(rut),
	FOREIGN KEY (id_cliente) REFERENCES cliente(rut)



);


create table Factura(
	id int,
	razon_social varchar(200),
	rut varchar(200),
	direccion varchar(200),
	giro int,
	iva int,
	neto int,
	fecha date,
	vendedor_emisor varchar(50),
	FOREIGN KEY (vendedor_emisor) REFERENCES usuario(rut),
	FOREIGN KEY (rut) REFERENCES cliente(rut),
	

	primary key (id)
);


 
create table detalles(
	id int,
    id_producto int,
    cantidad int,
    id_documento int, 
    precio int,
    primary key(id),
	FOREIGN KEY (id_producto) REFERENCES producto(id),
	FOREIGN KEY (id_documento) REFERENCES  factura(id),
	FOREIGN KEY (id_documento) REFERENCES  boleta(id)

    
    
);

create table jornada(
	fecha date,
    id_informe date,
    id_trabajador varchar(50),
    EstadoJornada date,
    primary key (fecha),
    FOREIGN KEY (EstadoJornada) REFERENCES Estado_Jornada(id_Jornada),
	FOREIGN KEY (id_trabajador) REFERENCES usuario(rut)

    

);
