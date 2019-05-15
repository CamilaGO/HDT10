/*
Nodos:
Paciente {nombre, telefono}
Doctor {nombre, colegiado, especialidad, telefono}
Medicina {nombre, desdeFecha, hastaFecha, dosis}

Relaciones:
Persona -[:VISITS] -> Doctor
Doctor -[PRESCRIBE] -> Medicina
Medicina <- [TAKES] - Paciente
Paciente -[:FRIEND] -> Paciente */

// Borra todo
MATCH (n) DETACH DELETE n


CREATE 
// PACIENTES 

	(pCRIS:Paciente {nombre:"Cristina", telefono: "8794"}),
	(pCAMI:Paciente {nombre:"Camila", telefono: "5524"}),
	(pINES:Paciente {nombre:"Ines", telefono: "9338"}),
	(pABRIL:Paciente {nombre:"Abril", telefono: "4567"}),
	(pDIANA:Paciente {nombre:"Diana", telefono: "2134"}),
	(pLUCA:Paciente {nombre:"Luca", telefono: "9702"}),
	(pWILLI:Paciente {nombre:"Willi", telefono: "2468"}),
	(pANDY:Paciente {nombre:"Andy", telefono: "5107"}),
	(pMARCO:Paciente {nombre:"Marco", telefono: "4492"}),
	(pROB:Paciente {nombre:"Roberto", telefono: "6083"}),
	(pDIEG:Paciente {nombre:"Diego", telefono: "1048"}),



	//DOCTORES
	(dCARLA :Doctor {nombre: "Carla", colegiado: "9345", especialidad: "Gastroenterologia", telefono: "3692"}),
	(dPAOLA :Doctor {nombre: "Paola", colegiado: "7459", especialidad: "Nutricion", telefono: "3459"}),
	(dJUL :Doctor {nombre: "Julio", colegiado: "6739", especialidad: "Fisioterapia", telefono: "9034"}),
	(dHEC :Doctor {nombre: "Hector", colegiado: "4891", especialidad: "General", telefono: "7734"}),
	(dDAV :Doctor {nombre: "David", colegiado: "4587", especialidad: "Psicologia", telefono: "9567"}),
	(dOSC :Doctor {nombre: "Oscar", colegiado: "9162", especialidad: "Pediatria", telefono: "3391"}),
	(dEVE :Doctor {nombre: "Evelyn", colegiado: "3401", especialidad: "Psicologia", telefono: "5930"}),
	(dEMI :Doctor {nombre: "Emilio", colegiado: "5582", especialidad: "Nutricion", telefono: "6123"}),
	(dALE :Doctor {nombre: "Alejandra", colegiado: "9203", especialidad: "Otorrinolaringologo", telefono: "4971"}),
	(dFER :Doctor {nombre: "Fernanda", colegiado: "1930", especialidad: "General", telefono: "8372"}),
	(dVAL :Doctor {nombre: "Valeria", colegiado: "9428", especialidad: "Fisioterapia", telefono: "5930"}),



	//MEDICINAS
	(mSUC:Medicina {nombre: "Sucralfato", desdeFecha: "04012019", hastaFecha: "04022019", dosis: "5mL antes de c/comida"}),
	(mB12:Medicina {nombre: "Vitamina B12", desdeFecha: "05042019", hastaFecha: "10122019", dosis: "1 tab al dia"}),
	(mCOF:Medicina {nombre: "Cofal", desdeFecha: "03082018", hastaFecha: "10102018", dosis: "Untar c/12 hrs"}),
	(mACE:Medicina {nombre: "Acetaminofen", desdeFecha: "01122018", hastaFecha: "01012019", dosis: "1 tab c/8 hrs"}),
	(mDIA:Medicina {nombre: "Diacepan", desdeFecha: "05062018", hastaFecha: "31072018", dosis: "1 tab antes de dormir"}),
	(mVC:Medicina {nombre: "Vitamina C", desdeFecha: "20032019", hastaFecha: "20042019", dosis: "1 tab en ayunas"}),
	(mESC:Medicina {nombre: "Escitalopram", desdeFecha: "15012018", hastaFecha: "15122019", dosis: "1 tab al dia"}),
	(mVD:Medicina {nombre: "Vitamina D", desdeFecha: "13052019", hastaFecha: "25092019", dosis: "4 tab a la semana"}),
	(mBUD:Medicina {nombre: "Budena Nasal", desdeFecha: "12012012", hastaFecha: "12112012", dosis: "Cada 6 hrs"}),
	(mHIE:Medicina {nombre: "HIERRO", desdeFecha: "04042019", hastaFecha: "04092019", dosis: "1 tab al dia"}),
	(mDI:Medicina {nombre: "DICLOFENACO", desdeFecha: "16102018", hastaFecha: "26122018", dosis: "1 tab si es necesario"}),


	//RELACIONES
	(pCRIS)-[:VISITS {fecha: "04012019"}]-> (dCARLA)-[:PRESCRIBE]-> (mSUC) <-[:TAKES]-(pCRIS),
	(pCAMI)-[:VISITS {fecha: "05042019"}]-> (dPAOLA)-[:PRESCRIBE]-> (mB12) <-[:TAKES]-(pCAMI),
	(pINES)-[:VISITS {fecha: "03082018"}]-> (dJUL)-[:PRESCRIBE]-> (mCOF) <-[:TAKES]-(pINES),
	(pABRIL)-[:VISITS {fecha: "01122018"}]-> (dHEC)-[:PRESCRIBE]-> (mACE) <-[:TAKES]-(pABRIL),
	(pDIANA)-[:VISITS {fecha: "05062018"}]-> (dDAV)-[:PRESCRIBE]-> (mDIA) <-[:TAKES]-(pDIANA),
	(pLUCA)-[:VISITS {fecha: "20032019"}]-> (dOSC)-[:PRESCRIBE]-> (mVC) <-[:TAKES]-(pLUCA),
	(pWILLI)-[:VISITS {fecha: "15012018"}]-> (dEVE)-[:PRESCRIBE]-> (mESC) <-[:TAKES]-(pWILLI),
	(pANDY)-[:VISITS {fecha: "13052019"}]-> (dEMI)-[:PRESCRIBE]-> (mVD) <-[:TAKES]-(pANDY),
	(pMARCO)-[:VISITS {fecha: "12012012"}]-> (dALE)-[:PRESCRIBE]-> (mBUD) <-[:TAKES]-(pMARCO),
	(pROB)-[:VISITS {fecha: "04042019"}]-> (dFER)-[:PRESCRIBE]-> (mHIE) <-[:TAKES]-(pROB),
	(pDIEG)-[:VISITS {fecha: "16102018"}]-> (dVAL)-[:PRESCRIBE]-> (mDI) <-[:TAKES]-(pDIEG),
//
	(pWILLI)-[:KNOWS]-> (pABRIL),
	(pABRIL)-[:KNOWS]-> (pDIANA),
	(pDIANA)-[:KNOWS]-> (pCRIS),
	(pCRIS)-[:KNOWS]-> (pLUCA),
	(pLUCA)-[:KNOWS]-> (pCAMI),
	(pCAMI)-[:KNOWS]-> (pINES),
	(pMARCO)-[:KNOWS]-> (pANDY),
	(pANDY)-[:KNOWS]-> (pABRIL),
	(pWILLI)-[:KNOWS]-> (pINES),
	(pANDY)-[:KNOWS]-> (pLUCA),
	(pANDY)-[:KNOWS]-> (pCRIS);




MATCH (n) RETURN n;


