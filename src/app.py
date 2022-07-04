from flask import *
from conexion import *
import time
import random


dao = DAO()
app = Flask(__name__)

# DIRECCION RAIZ. VISIBLE PARA TODOS. 
@app.route('/')
def home():
    return render_template('inicio.html')



#CATALOGO DE LA TIENDA. VISIBLE PARA EL PUBLICO EN GENERAL
@app.route('/catalogo', methods= ['GET','POST'])
def catalogo():
    if request.method=='GET':
        search = str(request.args.get('search'))
        if search !='None':
            data = {
            'productos': dao.buscarProducto(search)
            }
            return render_template('catalogo.html' ,data=data)
        else:
            data = {
            'productos': dao.listarProducto()
            }
            return render_template('catalogo.html' ,data=data)
    else:
        data = {
            'productos': dao.listarProducto()
            }
        return render_template('catalogo.html' ,data=data)




# LOGIN DE ACCESO A SISTEMA DE VENTA
@app.route('/login', methods= ["GET", "POST"])
def login():   
    if request.method=='POST':
        rut = request.form['rut']
        password = request.form['password']
        i = dao.findUser(rut)
        if len(i)>0:
            r = dao.consultaAutenticacion(rut,password)
            if len(r)>0:
                r = dao.rolUsuario(rut)
                nombre =dao.getName(rut)
                session['rut'] = rut
                if r ==1:   
                    # 1 for admin
                    return  redirect('/administracion')
                elif r==0:
                        # 0 for seller
                    
                    return  redirect('/puntodeventa')
                else:
                    return '<h1>Su cargo no fue indicado correctamente en el Sistema.</h1> <h5>Póngase en contacto con el Administrador del sistema</h5>'
            else:
                flash('Contraseña invalida')
                return render_template('login.html')

        else:
            flash('Usuario no encontrado')
            return render_template('login.html')
    else:
        if len(session) > 0 :
            try: 
                usuarioActivo = session['rut']
                r = dao.rolUsuario(usuarioActivo)
                if r ==1:   
                        # 1 for admin
                    return  redirect('/administracion')
                elif r==0:
                        
                    return  redirect('/puntodeventa')
                else:
                    return render_template('login.html')
            except:
                loggout()
                return render_template('login.html')

        else:
            return render_template('login.html')


# FUNCION PARA CERRAR SESION DE USUARIO
@app.route('/loggout')
def loggout():
    if 'rut' in session:
        session.pop('rut')
        return redirect('/login')
    else: 
        return redirect('/login')



# INTERFA DE VENDEDOR

### en desarrollo
@app.route('/puntodeventa', methods=['POST','GET'])
def puntodeventa():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 0:
            fecha= time.strftime('%Y-%m-%d', time.localtime())
            global tempCode 
            tempCode = random.randint(1111,99999)
            data = {
                'rut':session['rut'],
                'nombre':dao.getName(session['rut']),
                'jornada': dao.verJornada(fecha)
            }
            
            return render_template('vendedor.html', data = data)
            
        else:
            return redirect('/login')
    else:
        return redirect('/login')



@app.route('/puntodeventa/append', methods=['POST'])
def addListado():
    if request.method=='POST':
        busqueda = request.form['busqueda']
        resultado = dao.buscarProducto_vendedor(busqueda)
        if str(resultado) == 'None':
            pass
        else:
            id = resultado[0]
            nombre = resultado[1]
            precio = resultado[2]

            if dao.comprobarExistenciaEnlista(id,tempCode) > 0:
                dao.aumentarCantidad_deProduto(id,tempCode)

                    
            else:
                id = resultado[0]
                nombre = resultado[1]
                precio = resultado[2]
                dao.addTemp_list(tempCode,id,nombre,precio,1,precio)
                

        return redirect('/puntodeventa/venta/boleta')


@app.route('/puntodeventa/delete/<id>')
def deleteFromTemp(id):
    dao.eliminarProducto_temp(id,tempCode)
    return redirect('/puntodeventa/venta/boleta')

@app.route('/puntodeventa/add/<id>')
def addProductTemp(id):
    dao.aumentarCantidad_deProduto(id,tempCode)
    return redirect('/puntodeventa/venta/boleta')

@app.route('/puntodeventa/subtract/<id>')
def substracProductTemp(id):
    dao.restarCantidad_deProduto(id,tempCode)
    return redirect('/puntodeventa/venta/boleta')



@app.route('/puntodeventa/venta/boleta', methods=['POST','GET'])
def venta_boleta():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 0:
            
            fecha= time.strftime('%Y-%m-%d', time.localtime())
            data = {
                    'tipo_venta':'boleta',
                    'rut':session['rut'],
                    'nombre':dao.getName(session['rut']),
                    'id_boleta':dao.codNuevo_documento(),
                    'listado': dao.readTemp(tempCode),
                   'cod_temp':tempCode,
                'total':dao.precioTotal_temp(tempCode),
                'iva':dao.precioIVA_temp(tempCode),
                'neto':dao.precioNETO_temp(tempCode)

                }            
            return render_template('venta.html', data = data)
            
        else:
            return redirect('/login')
    else:
        return redirect('/login')
@app.route('/puntodeventa/venta/boleta/cancelar/<id>')
def cancelarBoleta(id):
    dao.deleteTemp(id)
    return redirect('/puntodeventa')

@app.route('/puntodeventa/venta/boleta/pagar/<id>')
def pagar(id):
    venta = dao.readTemp(id)
    id_Boleta = dao.codNuevo_documento()
    total = dao.precioTotal_temp(tempCode)
    fecha = time.strftime('%Y-%m-%d', time.localtime())
    iva = dao.precioIVA_temp(tempCode)
    vendedor = session['rut']
    dao.ingresarBoleta(id_Boleta,total,fecha,iva,vendedor)
    for i in venta:
        id_producto = i[0]
        cantidad =i[3]
        id_documento = id_Boleta
        precio = i[2]
        dao.ingresarDetalles(id_producto,cantidad,id_documento,precio)
    
    data = {
        'id_boleta': id_Boleta,
        'total': total,
        'fecha': time.strftime('%m/%d/%Y, %H:%M:%S', time.localtime()),
        'iva':iva,
        'vendedor':vendedor,
        'nombreVendedor': dao.getName(vendedor),
        'venta' : venta

    }
    return render_template('plantilla_boleta.html', data= data)







@app.route('/puntodeventa/venta/factura', methods=['POST','GET'])
def venta_factura():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 0:

            fecha= time.strftime('%Y-%m-%d', time.localtime())
            data = {
                'tipo_venta':'factura',
                'rut':session['rut'],
                'nombre':dao.getName(session['rut']),
                'id_factura':dao.codNuevo_documento(),
                'listado': dao.readTemp(tempCode),
                'cod_temp':tempCode,
                'total':dao.precioTotal_temp(tempCode),
                'iva':dao.precioIVA_temp(tempCode),
                'neto':dao.precioNETO_temp(tempCode)
            }
            
            return render_template('venta.html', data = data)
            
        else:
            return redirect('/login')
    else:
        return redirect('/login')





@app.route('/puntodeventa/factura/append', methods=['POST'])
def addListadFactura():
    if request.method=='POST':
        busqueda = request.form['busqueda']
        resultado = dao.buscarProducto_vendedor(busqueda)
        if str(resultado) == 'None':
            pass
        else:
            id = resultado[0]
            if dao.comprobarExistenciaEnlista(id,tempCode) > 0:
                dao.aumentarCantidad_deProduto(id,tempCode)
   
            else:
                id = resultado[0]
                nombre = resultado[1]
                precio = resultado[2]
                dao.addTemp_list(tempCode,id,nombre,precio,1,precio)
                
        return redirect('/puntodeventa/venta/factura')

@app.route('/puntodeventa/venta/Factura/cancelar/<id>')
def cancelarFactura(id):
    dao.deleteTemp(id)
    return redirect('/puntodeventa')


@app.route('/puntodeventa/delete/factura/<id>')
def deleteFromTempfac(id):
    dao.eliminarProducto_temp(id,tempCode)
    return redirect('/puntodeventa/venta/factura')

@app.route('/puntodeventa/add/factura/<id>')
def addProductTempfac(id):
    dao.aumentarCantidad_deProduto(id,tempCode)
    return redirect('/puntodeventa/venta/factura')

@app.route('/puntodeventa/subtract/factura/<id>')
def substracProductTempfac(id):
    dao.restarCantidad_deProduto(id,tempCode)
    return redirect('/puntodeventa/venta/factura')


@app.route('/puntodeventa/venta/Factura/cliente/<id>', methods=['GET','POST'])
def clienteFactura(id):
    if request.method == 'GET':
        data = {
        'id_Factura': dao.codNuevo_documento(),
        'iva' : dao.precioIVA_temp(tempCode),
        'neto':dao.precioNETO_temp(tempCode),
        'total':dao.precioTotal_temp(tempCode),
        'venta' : dao.readTemp(id),
        'listado': dao.readTemp(tempCode),
        'id': id
        }
        return render_template('datosFactura.html', data = data)
    
@app.route('/puntodeventa/venta/Factura/pagar/<id>' , methods=['GET','POST'] )
def emitirFactura(id):
    if request.method == 'POST':
        giro = request.form['giroFactura']
        razonSocial = request.form['razon']
        rutCliente = request.form['rut']
        direccion= request.form['direccion'] 
        venta = dao.readTemp(id)
        id_Factura = dao.codNuevo_documento()

        total = dao.precioTotal_temp(tempCode)
        fecha = time.strftime('%Y-%m-%d', time.localtime())
        iva = dao.precioIVA_temp(tempCode)
        vendedor = session['rut']
        neto = dao.precioNETO_temp(tempCode)

        
        dao.ingresarFactura(id_Factura,razonSocial,rutCliente,direccion,giro,iva,neto,fecha,vendedor)
        for i in venta:
            id_producto = i[0]
            cantidad =i[3]
            id_documento = id_Factura
            precio = i[2]
            dao.ingresarDetalles(id_producto,cantidad,id_documento,precio)
        
        data = {
            'id_Factura': id_Factura,
            'giro': giro,
            'fecha': time.strftime('%m/%d/%Y, %H:%M:%S', time.localtime()),
            'iva':iva,
            'neto':neto,
            'vendedor':vendedor,
            'total':total,
            'nombreVendedor': dao.getName(vendedor).capitalize(),
            'venta' : venta,
            'razonsocial':razonSocial,
            'rutCliente':rutCliente,
            'direccion':direccion

        }
        return render_template('plantilla_factura.html', data= data)




@app.route('/administracion')
def administracion():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            fechaFormateada = time.strftime('%d-%m-%Y', time.localtime())
            fecha= time.strftime('%Y-%m-%d', time.localtime())

            data = {
                'rut':session['rut'],
                'nombre':dao.getName(session['rut']),
                'fecha':fecha,
                'ventasBoleta': dao.cantidadDeVentasBoleta(fecha),
                'ventasFactura':dao.cantidadDeVentasFactura(fecha),
                'totalVentas': dao.cantidadDeVentasFactura(fecha) + dao.cantidadDeVentasBoleta(fecha),
                'recaudacionBoleta':dao.recaudacionBoletaTotal(fecha),
                'recaudacionFactura':dao.recaudacionFactura(fecha),
                'estadoJornada':dao.verJornada(fecha),
                'fechaFormateada': fechaFormateada,
                'totalProductos': dao.totalRegistroProductos(),
                'totalColaboradores': dao.totalRegistroUsuarios()
            }
            return render_template('administrador.html', data = data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/registrodeventas', methods=['GET','POST'] )
def informedeventa():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                fecha = request.form['diaBusqueda']
                data = {
                'ventasFactura': dao.ventasConFactura(fecha),
                'ventasBoleta':dao.ventasConBoleta(fecha),
                'fecha':fecha
                }
                return render_template ('informeDiario.html',data=data)
            else: 
                data = {
                    'ventasFactura': dao.ventasConFacturaTODAS(),
                    'ventasBoleta':dao.ventasConBoletaTODAS(),
                    'fecha':time.strftime('%Y-%m-%d', time.localtime())
                }
                return render_template ('informeDiario.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/informesdeventas', methods = ['GET','POST' ])
def informesdeventas():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'GET':
                data = {
                    'listadoJornadas':dao.verJornadas()
                }
                return render_template ('informesdeventas.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/informesdeventas/fecha', methods = ['GET','POST' ])
def informesdeventasdia():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                dia = request.form['fecha']
                data = {
                    'listadoJornadas':dao.verJornadaXDIA(dia)
                }
                return render_template ('informesdeventas.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')
@app.route('/informesdeventasportrabajador', methods = ['GET','POST' ])
def informesdeventasXtrabajador():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            try:
                if request.method == 'POST':
                    busquedaXrut = request.form['rutenjornada']
                    data = {
                        'listadoJornadas':dao.trabajadoresEnjornadas(busquedaXrut)
                    }
                    return render_template ('informesdeventas.html',data=data)
            except:
                data = {
                    'listadoJornadas':dao.verJornadas()
                }
                return render_template ('informesdeventas.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/informeventa/hoy', methods=['GET','POST'] )
def informedeventaHoy():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'GET':
                fecha = time.strftime('%Y-%m-%d', time.localtime())
                data = {
                'ventasFactura': dao.ventasConFactura(fecha),
                'ventasBoleta':dao.ventasConBoleta(fecha),
                'cantidadVentasBoleta' : dao.cantidadDeVentasBoleta(fecha),
                'cantidadVentasFactura' : dao.cantidadDeVentasFactura(fecha),
                'recaudacionBoletaTotal':dao.recaudacionBoletaTotal(fecha),
                'recaudacionBoletaIVA': dao.recaudacionBoletaIVA(fecha),
                'recaudacionBoletaNeto': dao.recaudacionBoletaNeto(fecha),

                'recaudacionFactura': dao.recaudacionFactura(fecha),
                'fecha':fecha,
                
                'emisor_boleta': dao.trabajador_emisor_boleta(fecha),
                'emisor_factura': dao.trabajador_emisor_factura(fecha)

                }
                return render_template ('informeHoy.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')
## aregar metodo de llegada
@app.route('/informeventa/<fecha>', methods=['GET','POST'] )
def informedeventade(fecha):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'GET':
                fecha = fecha
                data = {
                'ventasFactura': dao.ventasConFactura(fecha),
                'ventasBoleta':dao.ventasConBoleta(fecha),
                'cantidadVentasBoleta' : dao.cantidadDeVentasBoleta(fecha),
                'cantidadVentasFactura' : dao.cantidadDeVentasFactura(fecha),
                'recaudacionBoletaTotal':dao.recaudacionBoletaTotal(fecha),
                'recaudacionBoletaIVA': dao.recaudacionBoletaIVA(fecha),
                'recaudacionBoletaNeto': dao.recaudacionBoletaNeto(fecha),
                'recaudacionFactura': dao.recaudacionFactura(fecha),
                'fecha':fecha,
                'emisor_boleta': dao.trabajador_emisor_boleta(fecha),
                'emisor_factura': dao.trabajador_emisor_factura(fecha)
                }
                return render_template ('informeHoy.html',data=data)
            else: 
                data = {
                    'listadoJornadas':dao.verJornadas()
                }
                return render_template ('informesdeventas.html',data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/informeventa/documentoN/', methods=['GET','POST'] )
def busquedaDocumento():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                cod = request.form['codigoDocumento']
                b  = dao.esBoleta(cod)
                f =dao.esFactura(cod)
                if b ==1:
                    # es boleta 
                    boleta = dao.verBoleta(cod)

                    data = {
                    'id_boleta': boleta[0],
                    'total': boleta[1],
                    'fecha': boleta[2],
                    'iva':boleta[3],
                    'vendedor':boleta[4],
                    'venta': dao.verDetalles(boleta[0]), 
                    'nombreVendedor': dao.getName(boleta[4]),

                    }
                    return render_template('plantilla_boleta.html', data= data)
                elif f == 1: 
                    factura = dao.verFactura(cod)

                    data = {
                        'id_Factura': factura[0],
                        'giro': factura[4],
                        'fecha': factura[7],
                        'iva':factura[5],
                        'neto':factura[6],
                        'vendedor':factura[8],
                        'total':factura[6],
                        'nombreVendedor': dao.getName(factura[8]).capitalize(),
                        'razonsocial':factura[1],
                        'venta': dao.verDetalles(factura[0]),

                        'rutCliente':factura[2],
                        'direccion':factura[3]

                    }
                    return render_template('plantilla_factura.html', data= data)
                else:
                    flash('Documento tributario no encontrado.')
                    return redirect('/registrodeventas')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
@app.route('/informeventa/documentoN/<cod>', methods=['GET','POST'] )
def detalleDocumento(cod):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            r  = dao.esBoleta(cod)
            if r ==1:
                # es boleta 
                boleta = dao.verBoleta(cod)

                data = {
                'id_boleta': boleta[0],
                'total': boleta[1],
                'fecha': boleta[2],
                'iva':boleta[3],
                'vendedor':boleta[4],
                'venta': dao.verDetalles(boleta[0]), # corregir
                'nombreVendedor': dao.getName(boleta[4]),

                }
                return render_template('plantilla_boleta.html', data= data)
            elif r == 0: 
                factura = dao.verFactura(cod)

                data = {
                    'id_Factura': factura[0],
                    'giro': factura[4],
                    'fecha': factura[7],
                    'iva':factura[5],
                    'neto':factura[6],
                    'vendedor':factura[8],
                    'total':factura[6],
                    'nombreVendedor': dao.getName(factura[8]).capitalize(),
                    'razonsocial':factura[1],
                    'venta': dao.verDetalles(factura[0]), # corregir

                    'rutCliente':factura[2],
                    'direccion':factura[3]

                }
                return render_template('plantilla_factura.html', data= data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')


# FUNCION DE ADMINISTRADOR: ADMINISTRAR USUARIOS 
# INTERFAZ Y AGREGADOR DE USUARIOS
@app.route('/administrar usuarios', methods=["GET", "POST"])
def administrar_usuarios():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                rut = request.form['rut']
                password=request.form['password']
                nombre =request.form['nombres']
                apellido = request.form['apellidos']
                rol =request.form['rol']
                nombre_completo = nombre+ ' ' + apellido
                dao.addUser(rut,password,nombre_completo,rol)

                data = {
                    'usuarios': dao.readAllUser()
                    }
                flash('User added!')
                return render_template('adm usuarios.html', data=data)
            else:
                data = {
                    'usuarios': dao.readAllUser()
                    }
                return render_template('adm usuarios.html', data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# EDITAR USUARIO
@app.route('/administrar usuarios/edit/<rut>')
def get_user(rut):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            data= { 
                'usuario': dao.searchUser(rut),
                'registros':dao.searchUser(rut),
                'password':dao.getPassword(rut)

            }
            return render_template('user_edit.html', data = data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/administrar usuarios/updateUser/<rut>', methods=["GET", "POST"])
def updateUser(rut):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            password = request.form['password']
            nombre=request.form['nombre']
            rol=request.form['rol']
            dao.updateUser(rut,password,nombre,rol)
            data= { 
                'usuario': dao.searchUser(rut),
                'registros':dao.searchUser(rut)

            }
            
            return ' <script >window.close(); </script>  '     
        else:
            return redirect('/login')
    else:
        return redirect('/login')
# ELIMINAR USUARIO
@app.route('/administrar usuarios/deleteUser/<rut>', methods=["GET", "POST"])
def deleteUser(rut):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            dao.deleteUser(rut)
            return redirect('/administrar usuarios')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
        


    #ADMINISTRAR INVENTARIO 
#metodo para agregar productos a inventario
@app.route('/administrar inventario', methods=["GET", "POST"])
def administrar_inventario():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                codigo = request.form['codigo']
                nombre=request.form['nombreproducto']
                descripcion =request.form['descripcion']
                precio = request.form['precio']
                img =request.form['url_img']
                categoria = request.form['categoria']
                dao.addProduct(codigo,nombre,descripcion,precio,img,categoria)
                data = {
                    'productos': dao.readProduct()
                    }
                flash('product added!')
                return render_template('adm inventario.html', data=data)
            else:
                data = {
                    'productos': dao.readProduct()
                    }
                return render_template('adm inventario.html', data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')
 
# metodo para editar productos
@app.route('/administrar inventario/edit/<antiguo_codigo>' , methods=["GET", "POST"] )
def updateProduct(antiguo_codigo):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'POST':
                codigo_antiguo = antiguo_codigo
                codigo = request.form['new_codigo']
                nombre=request.form['new_nombre']
                descripcion =request.form['new_descripcion']
                precio = request.form['new_precio']
                img =request.form['new_url']
                categoria = request.form['categoria']

                dao.updateProduct(codigo_antiguo,codigo,nombre,descripcion,precio,img,categoria)
                data = {
                    'productoSelect': dao.buscarProducto(antiguo_codigo)

                    }
                return render_template('product_edit.html', data=data)
            else: 
                data = {
                    'productoSelect': dao.buscarProducto(antiguo_codigo)

                    }
                return render_template('product_edit.html', data=data)
        else:
            return redirect('/login')
    else:
        return redirect('/login')

#elimina productos del inventario.
@app.route('/administrar inventario/delete/<codigo>' , methods=["GET", "POST"])
def deleteProduct(codigo):
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            dao.deleteProduct(codigo)
            return redirect('/administrar inventario')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
#Activar y desactivar estado de jornada.

@app.route('/gestor de jornada/switch' , methods=['POST','GET'])
def activarJornada():
    if len(session) > 0 :
        if dao.rolUsuario(session['rut']) == 1:
            if request.method == 'GET':
                fecha= time.strftime('%Y-%m-%d', time.localtime())
                verJornada = dao.verJornada(fecha)
                if verJornada== 'No iniciada':
                    dao.crearJornada(fecha)
                    redirect ('/administracion')
                elif verJornada== 'abierta':
                    dao.cerrarJornada(fecha)  
                    redirect ('/administracion')
                elif verJornada == 'cerrada':
                    dao.activarJornada(fecha)
            return redirect('/administracion')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
#   METODO DE ARRANQUE DE APLICACION
if __name__ == '__main__':
    app.secret_key = "s5HKwm5AtlmzLiU0FIrrMsWXsrTdoxco"
    app.run(debug=True)