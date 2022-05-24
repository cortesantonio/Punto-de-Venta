from flask import *
import flask
from conexion import *
from flask import session

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
                    data = {
                        'rut':rut,
                        'nombre':nombre
                        }
                    return render_template('administrador.html', data=data)
                elif r==0:
                        # 0 for seller
                    data = {
                        'rut':rut,
                        'nombre':nombre
                    }
                    return render_template('vendedor.html',data=data)
                else:
                    return '<h1>Su cargo no fue indicado correctamente en el Sistema.</h1> <h5>Póngase en contacto con el Administrador del sistema</h5> '
            else:
                flash('invalid password')
                return render_template('login.html')

        else:
            flash('user not found')
            return render_template('login.html')
    else:
        return render_template('login.html')

# FUNCION PARA CERRAR SESION DE USUARIO
@app.route('/loggout')
def loggout():
    if 'rut' in session:
        session.pop('rut')
    return redirect('/login')

# FUNCION DE ADMINISTRADOR: ADMINISTRAR USUARIOS / 15:57 = registro en base de datos funcionando, falta listar en pantalla ,editar y eliminar
@app.route('/crud_user', methods=["GET", "POST"])
def crud_user():
    if request.method == 'POST':
        rut = request.form['rut']
        password=request.form['password']
        nombre =request.form['nombres']
        apellido = request.form['apellidos']
        rol =request.form['rol']
        nombre_completo = nombre+ ' ' + apellido
        print(rut,password,rol,nombre_completo)
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

@app.route('/crud_user/edit/<rut>')
def get_user(rut):
    data= { 
        'usuario': dao.searchUser(rut),
        'registros':dao.searchUser(rut),
        'password':dao.getPassword(rut)

    }
    return render_template('user_edit.html', data = data)

@app.route('/crud_user/updateUser/<rut>', methods=["GET", "POST"])
def updateUser(rut):
        password = request.form['password']
        nombre=request.form['nombre']
        rol=request.form['rol']
        dao.updateUser(rut,password,nombre,rol)
        data= { 
            'usuario': dao.searchUser(rut),
            'registros':dao.searchUser(rut)

        }
        
        return ' <script >window.close(); </script>  '
        
@app.route('/crud_user/deleteUser/<rut>', methods=["GET", "POST"])
def deleteUser(rut):
        dao.deleteUser(rut)
        return redirect('/crud_user')
        


@app.route('/crud_inventario', methods=["GET", "POST"])
def crud_inventario():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre=request.form['nombreproducto']
        descripcion =request.form['descripcion']
        precio = request.form['precio']
        img =request.form['url_img']
        dao.addProduct(codigo,nombre,descripcion,precio,img)
        data = {
            'productos': dao.listarProducto()
            }
        flash('product added!')
        return render_template('adm inventario.html', data=data)
    else:
        data = {
            'productos': dao.listarProducto()
            }
        return render_template('adm inventario.html', data=data)


@app.route('/crud_inventario/edit/<antiguo_codigo>' , methods=["GET", "POST"] )
def updateProduct(antiguo_codigo):
    if request.method == 'POST':
        codigo_antiguo = antiguo_codigo
        codigo = request.form['new_codigo']
        nombre=request.form['new_nombre']
        descripcion =request.form['new_descripcion']
        precio = request.form['new_precio']
        img =request.form['new_url']
        dao.updateProduct(codigo_antiguo,codigo,nombre,descripcion,precio,img)
        data = {
            'productos': dao.listarProducto()

            }
        
        return redirect('/crud_inventario')

@app.route('/crud_inventario/delete/<codigo>' , methods=["GET", "POST"])
def deleteProduct(codigo):
    dao.deleteProduct(codigo)
    return redirect('/crud_inventario')

#   METODO DE ARRANQUE DE SERVIDOR
if __name__ == '__main__':
    app.secret_key = "123123"
    app.run(debug=True)