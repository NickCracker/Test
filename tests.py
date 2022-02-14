from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import pymysql
from flask import Flask, redirect, url_for
from flask import render_template
from flask import request

#engine to mysql = mysql+pymysql://user:password@host/database
engine = create_engine('mysql+pymysql://root@localhost/prueba')

#engine to SQL server 

base = declarative_base()

class Producto(base):
    __tablename__ = 'new_inve_web'
    codigo=Column(String(50),primary_key=True)
    descripcion=Column(String(150))
    stock=Column(Integer())
    reserva=Column(Integer())
    clase=Column(String(50))
    subclase=Column(String(50))
    laboratorio=Column(String(50))
    precio=Column(Integer())
    lote=Column(String(50))
    bodega=Column(String(50))
    ubicacion=Column(String(50))

    def __str__(self):
        return self.descripcion

class Usuario(base):
    __tablename__ = 'usuarios'
    correo=Column(String(50),primary_key=True)
    nombre=Column(String(50))
    apellido=Column(String(50))
    usuario=Column(String(50))
    contraseña=Column(String(50))

Session = sessionmaker(engine)
session = Session()

app = Flask(__name__)
@app.route('/')
def Login():
    return render_template('login.html')

@app.route('/Permitir_acceso', methods=['POST'])
def Permitir_acceso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        coincidencias = session.query(Usuario).filter(Usuario.usuario==usuario and Usuario.contraseña==contraseña)
        for coincidencia in coincidencias:
            if coincidencia.usuario is not None:
                return redirect(url_for('Buscador'))
        return redirect(url_for('Login'))

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : RENDERIZADO
@app.route('/registro')
def Registro():
    return render_template('registro.html')

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : LOGICA BACKEND
@app.route('/Registrar', methods=['POST'])
def Registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        if not '' in [nombre,apellido,usuario,correo,contraseña] :
            usuario_nuevo = Usuario(nombre=nombre,apellido=apellido,usuario=usuario,correo=correo,contraseña=contraseña)
            session.add(usuario_nuevo)
            session.commit()
        return redirect(url_for('Login'))

#PAGINA .2 REGISTRO PARA USUARIOS NUEVOS : LOGICA BACKEND
@app.route('/Volver')
def Volver():
    return redirect(url_for("Login"))

#PAGINA .3 STOCK DE LOS PRODUCTOS : RENDERIZADO Y LOGICA BASICA
@app.route('/busqueda')
def Buscador():
    productos = session.query(Producto).all()
    return render_template('buscador.html',productos=productos)

#PAGINA .3 STOCK DE LOS PRODUCTOS CON BUSQUEDA : RENDERIZADO Y LOGICA
@app.route('/busqueda/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        entrada = request.form['entrada']
        patron = r"^{0}".format(entrada)
        productos = session.query(Producto).filter()
        return render_template('buscador.html',productos=productos)

#PAGINA .4 DETALLES DE LOS PRODUCTOS : RENDERIZADO 
@app.route('/detalle/<string:id>/<string:bodega>')
def Mostrar_detalle(id,bodega):
    productos = session.query(Producto).filter(Producto.codigo==id and Producto.bodega==bodega)
    return render_template('detalle.html',productos=productos)

















if __name__ == '__main__':
    app.run(debug=True,port=5000)
    #base.metadata.create_all(engine)

    #producto1=Producto(codigo="002",descripcion="jabon",stock=9,reserva=5,clase="010",subclase="32",laboratorio="KNOP",precio=5000,lote="3P",bodega="PRIMERA",ubicacion="AV.AMERICAS")
    #session.add(producto1)
    #session.commit()

    #productos = session.query(Producto).all()
    #for producto in productos:
    #   print(producto)

