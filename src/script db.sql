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

;
create table Boleta(
	id_boleta int,
	total int,
	fecha varchar(50),
    iva int,
    vendedor_emisor varchar(50),
	primary key (id),
	FOREIGN KEY (vendedor_emisor) REFERENCES usuario(rut)


);


create table Factura(
	id_factura int,
	razon_social varchar(200),
	rut varchar(200),
	direccion varchar(200),
	giro int,
	iva int,
	neto int,
	fecha date,
	vendedor_emisor varchar(50),
	FOREIGN KEY (vendedor_emisor) REFERENCES usuario(rut),
	primary key (id_factura)
);


 
create table detalle_boleta(
	id int,
    id_producto int,
    cantidad int,
    id_documento int, 
    precio int,
    primary key(id),
	FOREIGN KEY (id_producto) REFERENCES producto(id),
	FOREIGN KEY (id_documento) REFERENCES  boleta(id_boleta)  
    
);
 
create table detalle_factura(
	id int,
    id_producto int,
    cantidad int,
    id_documento int, 
    precio int,
    primary key(id),
	FOREIGN KEY (id_producto) REFERENCES producto(id),
	FOREIGN KEY (id_documento) REFERENCES  factura(id_factura)
    
);

create table temp (
	cod_producto int,
	nombre_producto varchar(255),
	precio int,
	cantidad int,
	total int,
	id_venta int

);


insert into Tipo_Usuario values(0,'vendedor');
insert into Tipo_Usuario values (1,'administrador');

insert into usuario values('321','321','antonio cortes sotelo', 0);
insert into usuario values('123','123','antonio cortes sotelo', 1);

insert into categoria_Producto values(1,'Frutas y Verduras');
insert into categoria_Producto values(2,'Carnes y Pescados');
insert into categoria_Producto values(3,'Panaderia y Pasteleria');
insert into categoria_Producto values(4,'Abarrotes');