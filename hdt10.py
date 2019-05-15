from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "netsa"))

def add_pac(tx, nombre, telefono):
    tx.run("CREATE (d:Paciente {nombre: $nombre, telefono: $telefono})",
           nombre=nombre, telefono=telefono)

def add_doc(tx, nombre, colegiado, especialidad, telefono):
    tx.run("CREATE (d:Doctor {nombre: $nombre, colegiado: $colegiado, especialidad: $especialidad, telefono: $telefono})",
           nombre=nombre,colegiado=colegiado, especialidad=especialidad, telefono=telefono)
def knows_pacient(tx, nombre, conocido_nombre):
    tx.run("MERGE (a:Paciente) -[:KNOWS] -> (b:Paciente) WHERE a.nombre = $nombre AND b.nombre = $conocido_nombre",
           nombre=nombre, conocido_nombre=conocido_nombre)
    #tx.run("MATCH (a:Paciente), (b:Paciente)"
     #      "WHERE a.nombre=$nombre AND b.nombre=$conocido_nombre"
      #     "CREATE (a)-[:KNOWS]->(b)")
def return_docs (tx, name):
   #for record in tx.run("MATCH (d:Doctor) WHERE d.especialidad=$name"
    #                     "RETURN d.nombre",
     #                   name=name):
      # print (record["d.nombre"])
    for record in tx.run ("MATCH (d:Doctor) WHERE d.especialidad = $name RETURN d.nombre",
            name=name):
        print (record["d.nombre"])
def mergePacDoc(tx, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis ):
    tx.run("MERGE (p:Paciente {nombre:$nombre, telefono:$telefono})"
           "MERGE (m:Medicina {nombre: $nombred, desdeFecha:$desdeFecha, hastaFecha: $hastaFecha, dosis: $dosis})"
           "MERGE (p)-[:TAKES]->(m)",
           nombre=nombre, telefono=telefono, nombred=nombred, desdeFecha=desdeFecha, hastaFecha=hastaFecha, dosis=dosis)
    


#opcion=input("Escoja 1 de las siguientes opciones")
with driver.session() as session:
    elec=0;
    while (elec!=7):
        print("Ingrese opcion que desea realizar\n")
        print("1.Ingresar doctor\n")
        print("2.Ingresar pacienta\n")
        print("3.\n")
        print("4.\n")
        print("7. Salir\n")
        elec=input("")
        print (elec)
        if (elec=="1"):
            nombre=input("Nombre del doctor\n")
            colegiado=input("Colegiado del doctor\n")
            especialidad=input("Especialidad del doctor\n")
            numero=input("Numero del doctor\n")
            session.write_transaction(add_doc, nombre, colegiado, especialidad, numero)
        elif (elec=="2"):
            nombre=input("Nombre del paciente\n")
            numero=input("Numero del paciente\n")
            session.write_transaction(add_pac, nombre, numero)
        elif (elec=="3"):
            nombre=input("Tu nombre\n")
            nombre2=input("nombre de conocido\n")
            session.write_transaction(knows_pacient, nombre, nombre2)
        elif (elec=="4"):
            espec=input ("Nombre de especialidad")
            session.read_transaction(return_docs, espec)
        elif (elec=="5"):
            nombre=input ("Nombre paciente")
            telefono=input ("Telefono\n")
            nombred=input ("Nombre de medicina\n")
            desdeFecha=input ("Desde que fecha\n")
            hastaFecha=input ("Hasta que fecha\n")
            dosis=input ("Dosis\n")
            session.write_transaction(mergePacDoc, nombre, telefono, nombred, desdeFecha, hastaFecha, dosis)
            
    


