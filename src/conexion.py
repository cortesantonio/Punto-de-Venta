
import mysql.connector
from mysql.connector import errorcode


class User():
    def __init__(self, rut , password , nombre, rol) -> None:
        self.rut = rut
        self.password = password
        self.nombre = nombre
        self.rol = rol
        
class Producto():
    def __init__(self,codigo,nombre,descripcion,precio, img='') -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.img=img

# CONEXION A BASE DE DATO MYSQL
class DAO:
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(user='root', password='',
                host='127.0.0.1',
                database='puntodeventa')
            print('ok')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

####### METODOS DE AUTENTICACIÓN DE DATOS DE USUARIO Y OBTENCIÓN DE DATOS

    # BUSCAR SI EXISTE EL USUARIO EN EL SISTEMA ANTES DE VERIFICAR PASSWORD
    def findUser(self,rut):
        cursor = self.cnx.cursor()
        consulta = "select * from usuario where rut = %s"
        info = (rut,)
        cursor.execute(consulta,info)
        r = cursor.fetchall()
        return r
    #   VERIFICA CREDENCIALES DEL USUARIO, RUT Y PASSWORD.
    def consultaAutenticacion(self,rut,password):
        cursor = self.cnx.cursor()
        consulta = "select * from usuario where rut = %s and password = %s"
        info = (rut,password)
        cursor.execute(consulta,info)
        results = cursor.fetchall()
        return results
    # IDENTIFICA EL TIPO DE USUARIO QUE ESTA INCIANDO SESION.
    def rolUsuario(self,rut):
        cursor = self.cnx.cursor()
        consulta = "select rol from usuario where rut = %s"
        info = (rut,)
        cursor.execute(consulta,info)
        results = cursor.fetchone()
        return results[0]
    # OBTIENE ELL NOMBRE DEL USUARIO
    def getName(self, rut):
        cursor = self.cnx.cursor()
        consulta = "select nombre from usuario where rut = %s"
        info = (rut,)
        cursor.execute(consulta,info)
        row=   cursor.fetchone()
        return row[0]

####### METODOS DE AUTENTICACIÓN DE DATOS DE USUARIO Y OBTENCIÓN DE DATOS




#######  - METODOS PARA LISTAR PRODUCTOS EN SECCION DE CATALOGO


#   FUNCION PARA OBTENER TODOS LOS PRODUCTOS DE LA BASE DE DATOS Y LISTARLO EN CATALOGO.
    def listarProducto(self):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM producto")
        return cursor.fetchall()

# FUNCION PARA FILTRAR BUSQUEDA EN CATALOGO
    def buscarProducto(self, busqueda):
        cursor = self.cnx.cursor()
        sql = ("select * from producto where nombre like %s or codigo like %s")
        bsq_format = str((busqueda+'%'))
        data = (bsq_format,bsq_format)
        cursor.execute(sql, data)
        return cursor.fetchall()


####### METODOS PARA LISTAR PRODUCTOS EN SECCION DE CATALOGO -


## METODOS ADMINISTRADOR


# ADMINISTRAR USUARIOS
    def addUser(self,rut,password,nombre,rol):
        cursor = self.cnx.cursor()
        sql = ("insert into usuario values(%s,%s,%s,%s)")
        data = (rut,password,nombre,rol)
        cursor.execute(sql, data)
        self.cnx.commit()
        return 'ok'

    def readAllUser(self):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT rut, nombre,rol FROM usuario")
        return cursor.fetchall()
    def searchUser(self, rut):
        cursor = self.cnx.cursor()
        sql =("SELECT rut, nombre,rol FROM usuario where rut = %s")
        data = (rut,)
        cursor.execute(sql, data)
        return cursor.fetchall()
    def updateUser(self, rut,password, nombre, rol):
        cursor = self.cnx.cursor()
        sql = ("update usuario set rut = %s , password = %s, nombre =  %s ,rol =  %s where rut =  %s")
        data = (rut,password,nombre,rol,rut)
        cursor.execute(sql, data)
        self.cnx.commit()
        return 'ok'
    def getPassword(self,rut):
        cursor = self.cnx.cursor()
        sql =("SELECT password FROM usuario where rut = %s")
        data = (rut,)
        cursor.execute(sql, data)
        return cursor.fetchone()[0]
    def deleteUser(self,rut):
        cursor = self.cnx.cursor()
        sql = ("delete from usuario where rut= %s")
        data = (rut,)
        cursor.execute(sql, data)
        self.cnx.commit()

# ADMINISTRAR USUARIOS

# ADM PRODUCTOS/

    def addProduct(self,codigo, nombre, descripcion, precio, img):
        cursor = self.cnx.cursor()
        sql = ("insert into producto values(%s,%s,%s,%s,%s)")
        data = (codigo,nombre,descripcion,precio,img)
        cursor.execute(sql, data)
        self.cnx.commit()
        return 'ok'
    def deleteProduct(self,codigo):
        cursor = self.cnx.cursor()
        sql = ("delete from producto where codigo= %s")
        data = (codigo,)
        cursor.execute(sql, data)
        self.cnx.commit()

    def updateProduct(self,codigo_antiguo,codigo, nombre, descripcion, precio, img):
        cursor = self.cnx.cursor()
        sql = 'update producto set codigo = %s, nombre = %s, descripcion =  %s ,precio =%s,img =%s where codigo = %s'
        data = (codigo, nombre, descripcion, precio, img,codigo_antiguo)
        cursor.execute(sql, data)
        self.cnx.commit()
        

