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
	primary key (id_boleta),
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


 
create table detalle(
	id int NOT NULL AUTO_INCREMENT,
    id_producto int,
    cantidad int,
    id_documento int, 
    precio int,
    primary key(id),
	FOREIGN KEY (id_producto) REFERENCES producto(id),
	FOREIGN KEY (id_documento) REFERENCES  boleta(id_boleta)  
    
);
 

create table temp (
	id_venta int,
	cod_producto int,
	nombre_producto varchar(255),
	precio int,
	cantidad int,
	total int

);


insert into Tipo_Usuario values(0,'vendedor');
insert into Tipo_Usuario values (1,'administrador');

insert into usuario values('321','321','antonio cortes sotelo', 0);
insert into usuario values('123','123','antonio cortes sotelo', 1);

insert into categoria_Producto values(1,'Frutas y Verduras');
insert into categoria_Producto values(2,'Carnes y Pescados');
insert into categoria_Producto values(3,'Panaderia y Pasteleria');
insert into categoria_Producto values(4,'Abarrotes');

insert into producto values(1,'Limon','limon en malla',1990,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20409659-0VhIfGOv-large.jpg',1);
insert into producto values(2,'Palta Hass Malla','700gr',2190,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20411826-gd7EBe-H-large.jpg',1);
insert into producto values(3,'Zapallo Italiano','1 UN',650,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/05014004-PKcaDFxZ-large.jpg',1);
insert into producto values(4,'Lechuga','Lechuga Hidropónica Española Extra',1350,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/20254265-LwhHK5RO-large.jpg',1);
insert into producto values(5,'Pasta Spaghetti 3','400gr',1070,'https://7483c243aa9da28f329c-903e05bc00667eb97d832a11f670edad.ssl.cf1.rackcdn.com/1014063-sx68qEPg-large.jpg',4);




