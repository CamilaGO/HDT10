from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "soyUVG17"))

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
    for record in tx.run ("MATCH (d:Doctor) WHERE d.especialidad = $name RETURN d.nombre",
            name=name):
        print (record["d.nombre"])
 
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


#opcion=input("Escoja 1 de las siguientes opciones")
with driver.session() as session:
    elec=0;
    print("------BIENVENIDO AL RECOMENDADOR DE DOCTORES------")
    while (elec!=7):
        print("\nIngrese opcion que desea realizar\n")
        print("1.Ingresar doctor\n")
        print("2.Ingresar paciente\n")
        print("3.Ingresar paciente e informacion de visita\n")
        print("4.Consultar dosctores por especialidad\n")
        print("5.Ingresar amistad paciente-paciente\n")
        print("6.Ingresar amistad doctor-doctor\n")
        print("7. Salir\n")
        elec=input("")
        elec = int(elec)
        if (elec==1):
            nombre=input("Nombre del doctor\n")
            colegiado=input("Colegiado del doctor\n")
            especialidad=input("Especialidad del doctor\n")
            numero=input("Numero del doctor\n")
            session.write_transaction(add_doc, nombre, colegiado, especialidad, numero)
        elif (elec==2):
            nombre=input("Nombre del paciente\n")
            numero=input("Numero del paciente\n")
            session.write_transaction(add_pac, nombre, numero)
        elif (elec==3):
            nombre=input ("Nombre paciente")
            telefono=input ("Telefono\n")
            nombred=input ("Nombre de medicina\n")
            desdeFecha=input ("Desde que fecha\n")
            hastaFecha=input ("Hasta que fecha\n")
            dosis=input ("Dosis\n")
            nombreDoc=input ("Nombre del doctor\n")
            fechaVisit=input ("Fecha de visita\n")
            session.write_transaction(mergeVisit, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis, nombreDoc, fechaVisit)
        elif (elec==4):
            espec=input ("Nombre de especialidad")
            session.read_transaction(return_docs, espec)
        elif (elec==5):
            nombre=input("Tu nombre\n")
            nombre2=input("nombre de conocido\n")
            session.write_transaction(knows_pacient, nombre, nombre2)
        elif (elec==6):
            nombre=input("Nombre doctor\n")
            nombre2=input("Nombre de conocido\n")
            session.write_transaction(knows_doctor, nombre, nombre2)
    if(elec==7):
        print("Hasta luego!")
       # elif (elec=="5"):
        #    nombre=input ("Nombre paciente")
         #   telefono=input ("Telefono\n")
          #  nombred=input ("Nombre de medicina\n")
           # desdeFecha=input ("Desde que fecha\n")
            #hastaFecha=input ("Hasta que fecha\n")
            #dosis=input ("Dosis\n")
            #session.write_transaction(mergePacDoc, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis)
       # elif (elec=="6"):
      #      nombre=input ("Nombre paciente")
        #    telefono=input ("Telefono\n")
         #   nombred=input ("Nombre de medicina\n")
          #  desdeFecha=input ("Desde que fecha\n")
          #  hastaFecha=input ("Hasta que fecha\n")
           # dosis=input ("Dosis\n")
            #nombreDoc=input ("Nombre del doctor\n")
            #fechaVisit=input ("Fecha de visita\n")
            #session.write_transaction(mergeVisit, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis, nombreDoc, fechaVisit)
            
    


