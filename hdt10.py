from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "soyUVG17"))

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
           "MERGE (a) -[:KNOWS]-> (b)",
           nombre=nombre, conocido_nombre=conocido_nombre)
    
#Amistad entre dos doctores
def knows_doctor(tx, nombre, conocido_nombre):
    tx.run("MATCH (a:Doctor) WHERE a.nombre = $nombre "
           "MATCH (b:Doctor) WHERE b.nombre = $conocido_nombre "
           "MERGE (a) -[:KNOWS]-> (b)",
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


with driver.session() as session:
    elec=0;
    print("------BIENVENIDO AL RECOMENDADOR DE DOCTORES------")
    while (elec!=7):
        print("\n\nIngrese opcion que desea realizar\n")
        print("1. Agregar doctor\n")
        print("2. Agregar paciente\n")
        print("3. Agregar paciente con medicina y vincular visita a un doctor existente\n")
        print("4. Consultar doctores por especialidad\n")
        print("5. Ingresar amistad paciente-paciente\n")
        print("6. Ingresar amistad doctor-doctor\n")
        print("7. Salir\n")
        elec=input("")
        if ((validarNumero(elec)==False)or (int(elec)==0)or (int(elec)>7)):
            print("¡¡¡¡¡Ingresaste una opcion incorrecta!!!!\n")
        else:
            elec = int(elec)
            if (elec==1):
                print("\n-_-_-_-_-_-_Agregar nuevo doctor-_-_-_-_-_-_\n")
                nombre=input("Nombre del doctor: ")
                colegiado=input("Colegiado del doctor: ")
                especialidad=input("Especialidad del doctor: ")
                numero=input("Numero del doctor: ")
                session.write_transaction(add_doc, nombre, colegiado, especialidad, numero)
                print("\n>>> Doctor exitosamente agregado")
            elif (elec==2):
                print("\n-_-_-_-_-_-_Agregar nuevo paciente-_-_-_-_-_-_\n")
                nombre=input("Nombre del paciente: ")
                numero=input("Numero del paciente: ")
                session.write_transaction(add_pac, nombre, numero)
                print("\n>>> Paciente exitosamente agregado")
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
                else:
                    print("El doctor no existe en la DB")
            elif (elec==4):
                print("\n-_-_-_-_-_-_Conocer doctores especializados-_-_-_-_-_-_\n")
                espec=input ("Nombre de especialidad: ")
                session.read_transaction(return_docs, espec)
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
    #Termina el while        
    if(elec==7):
        print("Hasta luego!")
          


