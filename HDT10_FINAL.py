# Maria Ines Vasquez 18250, Camila Gonzalez 18398, Abril Palencia 18198
# Hoja de trabajo numero 10
# 17/05/2019

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "netsa"))

#Agrega a la lista cada paciente que encuentre con ese nombre
def verificarDoc(nombre):
    lista=[]
    cql = "MATCH (x:Doctor {nombre: '" + nombre + "'}) RETURN x"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista

#Agrega a la lista cada paciente que encuentre con ese nombre
def verificarPac(nombre):
    lista=[]
    cql = "MATCH (x:Paciente {nombre: '" + nombre + "'}) RETURN x"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista

#Agrega a la lista cada paciente conocido que conozca a un doctor especializado
def conocePac(nombre, especialidad):
    lista=[]
    cql = "MATCH (p:Paciente {nombre: '" + nombre + "'})-[:KNOWS]->(:Paciente)-[:VISITS]->(d:Doctor {especialidad: '" + especialidad + "'}) RETURN d.nombre"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista
#Agrega a la lista cada paciente conocido que conozca otro paciente que conozca a un doctor especializado ((CONEXION EN SEGUNDO GRADO))
def conocePacdePac(nombre, especialidad):
    lista=[]
    cql = "MATCH (p:Paciente {nombre: '" + nombre + "'})-[:KNOWS]->(:Paciente)-[:KNOWS]->(:Paciente)-[:VISITS]->(d:Doctor {especialidad: '" + especialidad + "'}) RETURN d.nombre"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista

#Agrega a la lista cada doctor especializado conocido por el doctor
def conoceDocDoc(nombre, especialidad):
    lista=[]
    cql = "MATCH (d:Doctor {nombre: '" + nombre + "'})-[:KNOWS]->(x:Doctor {especialidad: '" + especialidad + "'}) RETURN x.nombre"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista
#Agrega a la lista cada doctor especializado conocido por el doctor conocido por doctor (CONEXION EN SEGUNDO GRADO)
def conoceDocdeDocdeDoc(nombre, especialidad):
    lista=[]
    cql = "MATCH (d:Doctor {nombre: '" + nombre + "'})-[:KNOWS]->(:Doctor)-[:KNOWS]->(x:Doctor {especialidad: '" + especialidad + "'}) RETURN x.nombre"
            # Execute the CQL query
    with driver.session() as graphDB_Session:
        nodes = graphDB_Session.run(cql)
        for node in nodes:
            lista.append(node)
        return lista

#Agrega un paciente con toda su info 
def add_pac(tx, nombre, telefono):
    tx.run("CREATE (d:Paciente {nombre: $nombre, telefono: $telefono})",
           nombre=nombre, telefono=telefono)
    
#Agrega un doctor con toda su info 
def add_doc(tx, nombre, colegiado, especialidad, telefono):
    tx.run("CREATE (d:Doctor {nombre: $nombre, colegiado: $colegiado, especialidad: $especialidad, telefono: $telefono})",
           nombre=nombre,colegiado=colegiado, especialidad=especialidad, telefono=telefono)

#Amistad entre dos pacientes
def knows_pacient(tx, nombre, conocido_nombre):
    tx.run("MATCH (a:Paciente) WHERE a.nombre = $nombre "
           "MATCH (b:Paciente) WHERE b.nombre = $conocido_nombre "
           "MERGE (a) -[:KNOWS]-> (b)"
           "MERGE (b) -[:KNOWS]-> (a)",
           nombre=nombre, conocido_nombre=conocido_nombre)
    
#Amistad entre dos doctores
def knows_doctor(tx, nombre, conocido_nombre):
    tx.run("MATCH (a:Doctor) WHERE a.nombre = $nombre "
           "MATCH (b:Doctor) WHERE b.nombre = $conocido_nombre "
           "MERGE (a) -[:KNOWS]-> (b)"
           "MERGE (b) -[:KNOWS]-> (a)",
           nombre=nombre, conocido_nombre=conocido_nombre)
    
#Muestra todos los doctores segun la especialidad ingresada 
def return_docs (tx, name):
    print("Doctores especializdos en " + name + "\n")
    cont = 0
    for record in tx.run ("MATCH (d:Doctor) WHERE d.especialidad = $name RETURN d.nombre",
            name=name):
        cont = cont + 1
        print (str(cont) + ". " + record["d.nombre"])
 
def mergePacDoc(tx, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis ):
    tx.run("MERGE (p:Paciente {nombre:$nombre, telefono:$telefono})"
           "MERGE (m:Medicina {nombre: $nombred, desdeFecha:$desdeFecha, hastaFecha: $hastaFecha, dosis: $dosis})"
           "MERGE (p)-[:TAKES]->(m)",
           nombre=nombre, telefono=telefono, nombred=nombred, desdeFecha=desdeFecha, hastaFecha=hastaFecha, dosis=dosis)
    
#Crea un nuevo paciente con la medicina recetada y la fecha en que visito a un doctor ya existente en la DB 
def mergeVisit(tx, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis, nombreDoc, fechaVisita  ):
    tx.run("MATCH (d:Doctor) WHERE d.nombre = $nombreDoc "
           "MERGE (p:Paciente {nombre:$nombre, telefono:$telefono})"
           "MERGE (m:Medicina {nombre: $nombred, desdeFecha:$desdeFecha, hastaFecha: $hastaFecha, dosis: $dosis})"
           "MERGE (p) -[:VISITS {fecha:$fechaVisita}]-> (d)"
           "MERGE (p) -[:TAKES]-> (m) <-[:PRESCRIBE]- (d)",
           nombre=nombre, telefono=telefono, nombred=nombred, desdeFecha=desdeFecha, hastaFecha=hastaFecha, dosis=dosis, nombreDoc=nombreDoc, fechaVisita=fechaVisita)
#Verifica que el valor de una variable sea un numero converitble a entero
def validarNumero(variable): 
    try:
        variable = int(variable)
        return True
    except ValueError:
        return False

# Primera recomendacion
# Recomienda a un doctor de una especialidad especifica a un usuario. Ingresa el nombre de un paciente y la especialidad que busca. 
def encontrarDOC(tx, nombre, especialidad):
    print("Doctores especializados en " + especialidad + "\n")
    cont = 0
    for doc in tx.run("MATCH (p:Paciente {nombre:$nombre})-[:KNOWS]->(:Paciente)-[:VISITS]->(d:Doctor {especialidad:$especialidad}) RETURN d.nombre",
           nombre=nombre, especialidad=especialidad):
            cont = cont + 1
            print (str(cont) + ". " + doc["d.nombre"])

# Recomienda a un doctor de una especialidad especifica a un usuario. Ingresa el nombre de un paciente y la especialidad que busca. Conexion en segundo grado
#dado que es un doctor especializado visitado por un conocido de un conocido
def encontrarDocdePacDePac(tx, nombre, especialidad):
    print("Doctores especializados en " + especialidad + "\n")
    cont = 0
    for doc in tx.run("MATCH (p:Paciente {nombre:$nombre})-[:KNOWS]->(:Paciente)-[:KNOWS]->(:Paciente)-[:VISITS]->(d:Doctor {especialidad:$especialidad}) RETURN d.nombre",
           nombre=nombre, especialidad=especialidad):
            cont = cont + 1
            print (str(cont) + ". " + doc["d.nombre"])
    
# Segunda recomendacion
# Recomienda un doctor de una especialidad especifica a otro doctor. Ingresa el nombre del doctor y la especialidad que busca.
def FindDocWithDoc(tx, nombre, especialidad):
    print("Doctores especializados en " + especialidad + "\n")
    cont = 0
    for doc in tx.run("MATCH (d:Doctor {nombre:$nombre})-[:KNOWS]->(x:Doctor {especialidad:$especialidad}) RETURN x.nombre",
           nombre=nombre, especialidad=especialidad):
            cont = cont + 1
            print (str(cont) + ". " + doc["x.nombre"])


# Recomienda un doctor de una especialidad especifica a otro doctor. Ingresa el nombre del doctor y la especialidad que busca.Conexion en segundo grado
#dado que es un doctor especializado conocido por un doctor conocido por el doctor original

def FindDocWithDocofDoc(tx, nombre, especialidad):
    print("Doctores especializados en " + especialidad + "\n")
    cont = 0
    for doc in tx.run("MATCH (d:Doctor {nombre:$nombre})-[:KNOWS]->(:Doctor)-[:KNOWS]->(x:Doctor {especialidad:$especialidad}) RETURN x.nombre",
           nombre=nombre, especialidad=especialidad):
            cont = cont + 1
            print (str(cont) + ". " + doc["x.nombre"])

    

# Programa
with driver.session() as session:
    elec=0;
    #muestra mensaje de bienvenida.
    print("------BIENVENIDO AL RECOMENDADOR DE DOCTORES------")
    while (elec!=9):
        #menu
        print("\n\nIngrese opcion que desea realizar\n")
        print("1. Agregar doctor\n")
        print("2. Agregar paciente\n")
        print("3. Agregar paciente con medicina y vincular visita a un doctor existente\n")
        print("4. Consultar doctores por especialidad\n")
        print("5. Ingresar amistad paciente-paciente\n")
        print("6. Ingresar amistad doctor-doctor\n")
        print("7. Consultar doctor visitado por paciente conocido\n")
        print("8. Consultar doctor conocido de doctor\n")
        print("9. Salir\n")
        elec=input("")
        # si ingresa una opcion incorrecta.
        if ((validarNumero(elec)==False)or (int(elec)==0)or (int(elec)>9)):
            print("¡¡¡¡¡Ingresaste una opcion incorrecta!!!!\n")
        else:
            elec = int(elec)
            # Agrega nuevo doctor.
            if (elec==1):
                print("\n-_-_-_-_-_-_Agregar nuevo doctor-_-_-_-_-_-_\n")
                nombre=input("Nombre del doctor: ")
                colegiado=input("Colegiado del doctor: ")
                especialidad=input("Especialidad del doctor: ")
                numero=input("Numero del doctor: ")
                session.write_transaction(add_doc, nombre, colegiado, especialidad, numero)
                print("\n>>> Doctor exitosamente agregado")
            # Agrega nuevo paciente.
            elif (elec==2):
                print("\n-_-_-_-_-_-_Agregar nuevo paciente-_-_-_-_-_-_\n")
                nombre=input("Nombre del paciente: ")
                numero=input("Numero del paciente: ")
                session.write_transaction(add_pac, nombre, numero)
                print("\n>>> Paciente exitosamente agregado")
            # Agregar paciente con su medicina y doctor
            elif (elec==3):
                print("\n-_-_-_-_-_-_Agregar paciente con medicina y vincular visita a un doctor existente-_-_-_-_-_-_\n")
                nombre=input ("Nombre paciente: ")
                telefono=input ("Telefono: ")
                nombred=input ("Nombre de medicina: ")
                desdeFecha=input ("Desde que fecha: ")
                hastaFecha=input ("Hasta que fecha: ")
                dosis=input ("Dosis: ")
                nombreDoc=input ("Nombre del doctor: ")
                fechaVisit=input ("Fecha de visita: ")
                if((len(verificarDoc(nombreDoc))>=1)):
                    session.write_transaction(mergeVisit, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis, nombreDoc, fechaVisit)
                    print("\n>>> Se ha creado exitosamente la visita de " + nombre + " a " + nombreDoc)
                # Doctor no existente.
                else:
                    print("El doctor no existe en la DB")
            # relacionar doctores con especialidad.
            elif (elec==4):
                print("\n-_-_-_-_-_-_Conocer doctores especializados-_-_-_-_-_-_\n")
                espec=input ("Nombre de especialidad: ")
                session.read_transaction(return_docs, espec)
            # Amistad paciente con paciente.
            elif (elec==5):
                print("\n-_-_-_-_-_-_Ingresar amistad paciente-paciente-_-_-_-_-_-_\n")
                nombre=input("Tu nombre: ")
                nombre2=input("nombre de conocido: ")
                #Se verifica que ambos pacientes existan
                if((len(verificarPac(nombre))>=1)and(len(verificarPac(nombre2))>=1)):
                    session.write_transaction(knows_pacient, nombre, nombre2)
                    print("\n>>> Se ha creado exitosamente la conexion entre " + nombre + " y " + nombre2)
                else:
                    print("Alguno de los pacientes no existe en la DB")
            # Amistad doctor con doctor.
            elif (elec==6):
                print("\n-_-_-_-_-_-_Ingresar amistad doctor-doctor-_-_-_-_-_-_\n")
                nombre=input("Nombre doctor: ")
                nombre2=input("Nombre de conocido: ")
                #Se verifica que ambos doctores existan
                if((len(verificarDoc(nombre))>=1)and(len(verificarDoc(nombre2))>=1)):
                    session.write_transaction(knows_doctor, nombre, nombre2)
                    print("\n>>> Se ha creado exitosamente la conexion entre " + nombre + " y " + nombre2)
                else:
                    print("\n>>> Alguno de los doctores no existe en la DB")
            # Doctor visitado por paciente conocido.
            elif (elec==7):
                print("\n-_-_-_-_-_-_Doctor visitado por paciente conocido-_-_-_-_-_-_\n")
                nombre=input("Nombre del paciente: ")
                espec=input("Especialidad interes: ")
                #Se verifica que el paciente exista
                if((len(verificarPac(nombre)))>=1):
                    if(len(conocePac(nombre, espec))>=1):
                        session.read_transaction(encontrarDOC, nombre, espec)
                    else:
                        print("Tus conocidos no conocen a nadie especializado en " + espec)
                    print("\n-_-_-_-_-_Doctor visitado por paciente conocido del paciente conocido original-_-_-_-_-_\n")
                    #Verifica si un una conexion en segundo grado de paciente que conoce a otro paciente que vaya con un doctor especializad0
                    if(len(conocePacdePac(nombre, espec))>=1):
                        session.read_transaction(encontrarDocdePacDePac, nombre, espec)
                    else:
                        print("Tus conocidos no conocen a nadie especializado en " + espec+" en segundo grado")
                else:
                    print("\n>>> El paciente llamado " + nombre + " no existe en la DB")
                    
                
            # Doctor con especialidad conocido por otro.
            elif (elec==8):
                print("\n-_-_-_-_-_-_Doctor especializado conocido por doctor-_-_-_-_-_-_\n")
                nombre=input("Nombre del Doctor: ")
                espec=input("Especialidad interes: ")
                #Se verifica que el doctor exista
                if((len(verificarDoc(nombre)))>=1):
                    if(len(conoceDocDoc(nombre, espec))>=1):
                        session.read_transaction(FindDocWithDoc, nombre, espec)
                    else:
                        print("No conoces a nadie especializado en " + espec)
                    print("\n-_-_-_-_Doctor especializado conocido por doctor que es conocido por doctor original-_-_-_-_\n")
                    #Verifica si un una conexion en segundo grado de doctor que conoce a otro doctor que conozca a un doctor especializad0
                    if(len(conoceDocdeDocdeDoc(nombre, espec))>=1):
                        session.read_transaction(FindDocWithDocofDoc, nombre, espec)
                    else:
                        print("No conoces a nadie especializado en " + espec+" en segundo grado")
                    
                else:
                    print("\n>>> El doctor llamado " + nombre + " no existe en la DB")
               
    #Termina el while        
    if(elec==9):
        print("Hasta luego!")
          


