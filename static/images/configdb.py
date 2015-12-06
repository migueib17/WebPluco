import pymongo
from datetime import date,datetime
"""
Clase auxiliar que ayuda a hacer las operaciones con pymongo
"""
class Database():
            #establecemos la conexion
            try:
                  conn=pymongo.MongoClient()
                  #definimos la base de datos a usar y coleccion
                  db = conn.pluco
                  collection = db.usuarios
                  print "Connected sucessfully!!!"
            except pymongo.errors.ConnectionFailure, e:
                  print "Could not connect to MongoDB: %s" %e    

            

            #obtener coleccion
            def getCollection(self):
                  try:
                        collection = db.usuarios
                  except:
                        return "Error coleccion inexistente"
                  return collection

             #insertar datos
            def insertData(self,form):
                 #como da problemos con date time, convertimos primero la fecha
                 date = datetime.combine(form.birthday.data,datetime.min.time())
                 doc = {"username": form.username.data,"name": form.name.data, "firstName": form.firstName.data,"secondName": form.secondName.data,"email": form.email.data,"creditCard": form.creditCard.data,"birthday": date,"address": form.address.data,"password": form.password.data,"confirm": form.confirm.data,"payMethod": form.paymethod.data}
                 #insertamos los datos en el documento
                 
                 self.collection.insert(doc)
                 print "Datos insertados"

            #actualizardatos
            def updateData(self,form):
                 #como da problemos con date time, convertimos primero la fecha
                  try:
                        date = datetime.combine(form.birthday.data,datetime.min.time())
                        self.collection.update(
                              {'username': form.username.data},
                              {"username": form.username.data,"name": form.name.data, "firstName": form.firstName.data,"secondName": form.secondName.data,"email": form.email.data,"creditCard": form.creditCard.data,"birthday": date,"address": form.address.data,"password": form.password.data,"confirm": form.confirm.data,"payMethod": form.paymethod.data}
                              )
                        
                        print ("Datos actualizados")
                  except:
                        print self.collection
                        print("Error actualizando datos")

            #obtener datos usuario
            def getUserData(self,username):
                  #pasamos username por funcion username
                  data = self.collection.find({'username':username})
                  for d in data:
                        print ("Datos de "+d['username'])

                  return d
                 
            #obtener prueba acceso
            def getUserLogin(self,username,password):
                  #pasamos username por funcion username
                  data = self.collection.find({'username':username})
                  for d in data:
                        print ("Datos de "+d['username'])
                        if d['username'] == username and d['password'] == password:
                              return True
                        else:
                              return False

            #obtener nombre de usuario, y comprobar que esta libre para poder registrar
            def getUserName(self,username):
                  #pasamos username por funcion username
                  data = self.collection.find({'username':username})
                  if (data):
                     print ("Existe usuario")
                     return False
                  else:
                     return True

            """> show databases
            local 0.078125GB
            > use pluco
            switched to db pluco
            > db.createCollection("usuarios")
            { "ok" : 1 }
            > show databases
            local 0.078125GB
            pluco 0.203125GB
            > show collections
            system.indexes
            usuarios
            > db
            pluco.usuarios.insert({
                  author: ""
                  ......
                  })
            doc = {"name":"Alberto","surname":"Negron","twitter":"@Altons"}
            #pasamos username por funcion username
            query = collection.find_one({"username":username})
            print (query['name'])
            b.people.update(
   { name: "Andy" },
   {
      name: "Andy",
      rating: 1,
      score: 1
   },
   { upsert: true }
)
            """
