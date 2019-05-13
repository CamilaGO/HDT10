/*
Nodos:
Paciente {nombre, telefono}
Doctor {nombre, colegiado, especialidad, telefono}
Medicina {nombre, desdeFecha, hastaFecha, dosis}

Relaciones:
Persona -[:VISITS] -> Doctor
Doctor -[PRESCRIBE] -> Medicina
Medicina <- [TAKES] - Paciente */

MATCH (n) DETACH DELETE n;


CREATE 
// PACIENTES 

	(pCRIS:Paciente {nombre:"Cristina", telefono: "8794"}),



	//DOCTORES
	(dCARLA :Doctor {nombre: "Carla", colegiado: "9345", especialidad: "Gastroenterologa", telefono: "3692"}),



	//MEDICINAS
	(mSUC:Medicina {nombre: "Sucralfato", desdeFecha: "04012019", hastaFecha: "04022019", dosis: "5mL antes de c/comida"}),


	//RELACIONES
	(pCRIS)-[:VISITS {fecha: "04012019"}]-> (dCARLA)-[:PRESCRIBE]-> (mSUC) <-[:TAKES]-(pCRIS);
