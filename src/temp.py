

from calendar import c
from conexion import *
dao = DAO()

r = dao.buscarProducto_vendedor('1')
resultado = list(r)

resultado.append(1)

print(
    resultado[len(resultado)-1]
    
    )
resultado[len(resultado)-1]  +=1


print(

    resultado[len(resultado)-1]
    
    )












    

@app.route('/puntodeventa/venta/boleta', methods=['POST','GET'])
def venta_con_boleta():
    fecha= time.strftime('%Y-%m-%d', time.localtime())
    if dao.verJornada(fecha) == 'abierta':
        if request.method == 'POST':
            busqueda = request.form['busqueda']
            r = dao.buscarProducto_vendedor(busqueda)
            if r==None:
                pass
            else:
                if r in lista:
                    pass
                else:
                    lista.append(r)

            data = {
                    'listado' : lista
                    
                }
            print(lista)
            return render_template('venta_boleta.html',data = data)
        else: 
            data = {
                'listado' : lista
            }
            return render_template('venta_boleta.html',data = data)
    else:
        return redirect('/puntodeventa')

@app.route('/puntodeventa/borrararticulo/<articulo>', methods=['POST','GET'])
def borrar(articulo):
    print(articulo)
    print(lista)
    c =0
    for i in lista:
        x = lista[i]
        if x == articulo:
            print('esta')
        
    return redirect ('/puntodeventa/venta/boleta')


@app.route('/puntodeventa/clear', methods=['POST','GET'])
def clear():
    lista.clear()
    return redirect ('/puntodeventa/venta/boleta')

@app.route('/puntodeventa/venta/factura', methods=['POST','GET'])
def venta_con_factura():
    
    return 'factura'

