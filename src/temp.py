
from conexion import *
dao = DAO()

b = dao.verTrabajadoresEnJornada_boelta('2022-06-17')
f = dao.verTrabajadoresEnJornada_factura('2022-06-17')

print(b)


list= []

