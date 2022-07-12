create database puntodeventa;

use puntodeventa;

create table estado_jornada(
	id_jornada date,
	estado varchar(50),
    primary key (id_jornada)
);

create table tipo_usuario(
	id int,
	tipo varchar(50),
    primary key (id)
);
create table usuario(
	rut varchar(50),
    password varchar(200),
    nombre varchar(200),
    rol int,
    primary key (rut),
    FOREIGN KEY (rol) REFERENCES tipo_usuario(id)
);



create table categoria_producto(
	id int,
    categoria varchar(200),
    primary key(id)

);

create table producto(
	id int,
    nombre varchar(200),
    descripcion varchar(255),
    precio int,
    img text,
    id_categoria int,
    primary key (id)

);

;
create table boleta(
	id_boleta int,
	total int,
	fecha varchar(50),
    iva int,
    vendedor_emisor varchar(50),
	primary key (id_boleta)


);


create table factura(
	id_factura int,
	razon_social varchar(200),
	rut varchar(200),
	direccion varchar(200),
	giro varchar(200),
	iva int,
	neto int,
	fecha date,
	vendedor_emisor varchar(50),
	primary key (id_factura)
);


 
create table detalle(
	id int NOT NULL AUTO_INCREMENT,
    id_producto int,
    cantidad int,
    id_documento int, 
    precio int,
    primary key(id)
    
);
 

create table temp (
	id_venta int,
	cod_producto int,
	nombre_producto varchar(255),
	precio int,
	cantidad int,
	total int

);


insert into tipo_usuario values(0,'vendedor');
insert into tipo_usuario values (1,'administrador');

insert into usuario values('admin-0','admin-0','Administrador', 1);

insert into categoria_producto values(1,'Frutas y Verduras');
insert into categoria_producto values(2,'Carnes y Pescados');
insert into categoria_producto values(3,'Panaderia y Pasteleria');
insert into categoria_producto values(4,'Abarrotes');

insert into producto values(1,'Limon','limon en malla',1990,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20409659-0VhIfGOv-large.jpg',1);
insert into producto values(2,'Palta Hass Malla','700gr',2190,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20411826-gd7EBe-H-large.jpg',1);
insert into producto values(3,'Zapallo Italiano','1 UN',650,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/05014004-PKcaDFxZ-large.jpg',1);
insert into producto values(4,'Lechuga','Lechuga Hidropónica Española Extra',1350,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20254265-LwhHK5RO-large.jpg',1);
insert into producto values(5,'Pasta Spaghetti 3','400gr',1070,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/1014063-sx68qEPg-large.jpg',4);




