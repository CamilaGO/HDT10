# HDT10
1. Crear un nuevo grafo en neo4j con la contraseña deseada

2. Modificar en el área superior del archivo HDT10_FINAL.py el contenido de la contraseña por 

la ingresada en el paso 1

3. Darle "Start" al grafo y luego presionar el boton de "manage". 

4. En la ventana que se abrirá, seleccionar "browser" y pegar lo siguiente del documento ***doctores.cypher*** 
     Copiar desde *CREATE* hasta *(pANDY)-[:KNOWS]-> (pCRIS);*

5. Presionar el boton Play de lado derecho superior

6. Introducir en la misma barra el comando match (n) return n para visualizar los nodos

7. Minimizar la ventana y ejecutar el programa ***HDT10_FINAL.py***

8. Regresar a la ventana de neo4j e introducir el comando del paso 6 para actualizar la base de datos y visualizar los nodos modificados 
en el paso 7
