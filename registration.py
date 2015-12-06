#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Registro de datos y exportación a dbm
"""
import re
import anydbm
import configdb
from wtforms import BooleanField
from wtforms import DateField
from wtforms import Form
from wtforms import PasswordField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators
from wtforms import IntegerField
from wtforms import RadioField
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import DateField


"""
Clase principal para los registros.
Crea registros con campos asociados a cada entrada.
:param: Form
"""
class RegistrationForm(Form):

      #Generamos todos los campos que necesitamos
      username = TextField('Nombre usuario',[validators.Length(min=5,max=30),validators.required()])

      name = TextField('Nombre ',[validators.Length(min=5,max=30),validators.required()])
      firstName = TextField('Primer apellido',[validators.Length(min=5,max=30)])
      secondName = TextField('Segundo apellido',[validators.Length(min=5,max=30)])
      email = EmailField('Direccion email',[validators.Length(min=6,max=50),validators.Email()])
      # match = re.search(r'\w+@\w+', str)
      creditCard = TextField('Numero tarjeta Visa y 4 dígitos de control',[
      validators.Regexp(r'\d{4}-\d{4}-\d{4}-\d{4}',message="Introduzca la #tarjeta separado por guiones")])
      birthday = DateField('Fecha nacimiento: aa-mm-dd',[validators.required()])

      address = TextAreaField('Direccion')

      password = PasswordField('Contrasenia',[validators.Length(min=7),validators.required(),validators.EqualTo('confirm',message='Contrasenias deben coincidir')])
      confirm = PasswordField('Repite contrasenia')


      paymethod = RadioField('Metodo Pago', choices=[('creditCard','Tarjeta Credito'),('efectivo','Pago Efectivo')])

      accept_tos = BooleanField('acepto los términos',[validators.required()])

      #Funcion que crea las bases de datos con el nombre usuario
      def databases(self):
        
          form = self
          #Creamos el fichero que contendrá la base de datos, cada usuario tiene la suya asociada
          db = anydbm.open('databases/'+str(form.username.data),'c')
          #Introducimos en la base de datos todos los datos de los usuarios
          db["username"] = (str(form.username.data))
          db["name"] = (str(form.name.data))
          db["firstName"] = (str(form.firstName.data))
          db["secondName"] = (str(form.secondName.data))
          db["email"] = (str(form.email.data))
          db["creditCard"] = (str(form.creditCard.data))
          db["birthday"] = (str(form.birthday.data))
          db["address"] = (str(form.address.data))
          db["password"] = (str(form.password.data))
          db["confirm"] = (str(form.confirm.data))
          print db["username"]
          db.close()

          
      def databasesMongo(self,conn):
          form = self
          try:
              conn.insertData(form)
          except ValueError:
            return ("Error coleccion inexistente, imposible registrar datos")

      def databasesMongoUpdate(self,conn,username):
          form = self
          try:
            #insertamos los datos
            conn.updateData(form)
          except ValueError:
            return ("Error coleccion inexistente imposible registrar datos")
     #Comprobamos si existe la base de datos, es decir existe usuario, y que la contraseña asociada es correcta
      def checkuser(self,user,passw):
          try:
             db = anydbm.open('databases/'+str(user),'r')
          except:
            return (False)

          if (db["password"]) == passw:
            return (True)
          else:
            return (False)

      def getData(self,form,user):
          try:

            db = anydbm.open('databases/'+str(user),'c')
          except:
            return (False)

          form.username.data = (db["username"])
          form.name.data = (db["name"])
          form.firstName.data = (db["firstName"])
          form.secondName.data = (db["secondName"])
          form.email.data = (db["email"])
          form.creditCard.data = (db["creditCard"])
          form.birthday.data = (db["birthday"])
          form.address.data = (db["address"])
          form.password.data = (db["password"])
          form.confirm.data = (db["confirm"])

          return form

      #comprobamos si exsite el usuario en Mongodb
      def checkuserMongo(self,connection,user,passw):
            re =  connection.getUserLogin(user,passw)
            return re

      #antes de registrar comprobamos que el nombre de usuario esta libre
      def checkuserNameMongo(self,connection,user):
            re =  connection.getUserName(user)
            return re

      #nos pasan la conexion y devolvemos formulario con los datos asociados
      def getDataMongo(self,form,user,connection):
          #obtenemos la coleccion del usuario
          try:
            collection = connection.getCollection()
            #obtenemos los datos del usuario
            db = connection.getUserData(user)

          except ValueError:
            return ("Error coleccion inexistente o usuario no encontrado")


          form.username.data = (db["username"])
          form.name.data = (db["name"])
          form.firstName.data = (db["firstName"])
          form.secondName.data = (db["secondName"])
          form.email.data = (db["email"])
          form.creditCard.data = (db["creditCard"])
          form.birthday.data = (db["birthday"])
          form.address.data = (db["address"])
          form.password.data = (db["password"])
          form.confirm.data = (db["confirm"])

          return form

