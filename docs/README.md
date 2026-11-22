# Materiales para participantes

Lo que vieron en pantalla los 148 estudiantes, en español, tal como está en las plantillas de este repositorio. Todo el recorrido son 21 páginas en tres apps (`debate` → `conflict` → `results`) más cinco páginas de espera que no muestran contenido propio.

**Preregistro:** AsPredicted #201318, registrado el 26 de noviembre de 2024 a las 09:54 (hora de Bogotá), el día de las dos primeras sesiones. El PDF del registro no se incluye aquí porque no es parte del código; está en la carpeta del paper (`AsPredicted #201318.pdf`).

**Capturas de pantalla:** no se incluyen en este repositorio. Las cinco capturas de la versión de campo (escritura de argumentos, instrucciones de la etapa 2, las situaciones del juego y la página de valoración) están en la carpeta de materiales del paper, no en el código. `TODO (Ferley):` decidir si se publican aquí.

**Moneda.** Todas las cantidades que se muestran están escritas como pesos colombianos en las plantillas. En `settings.py`, `REAL_WORLD_CURRENCY_CODE` quedó en `'USD'`, así que el panel de administración de oTree formatea `payoff` con signo de dólar: los números son pesos.

## App `debate` (etapa 1: argumentación y valoración)

### 1. Bienvenida (`debate/Bienvenida.html`)

Bienvenida al Laboratorio de Economía Experimental de la Universidad del Rosario. Se avisa que la actividad es individual, que no se debe hablar ni mirar las respuestas de los demás, y que se levante la mano para pedir ayuda.

### 2. Consentimiento informado (`debate/Consentimiento.html`, campo `consentimiento`)

Texto completo del consentimiento: participación voluntaria, posibilidad de retirarse en cualquier momento (sin ganancias si se retira antes del final), duración máxima de 60 minutos, financiación de la Dirección de Investigación de la Universidad del Rosario, monto mínimo de 10.000 pesos más ganancias según las decisiones, uso confidencial de la información y correo de contacto `rebel@urosario.edu.co`. Se advierte que, tras conocer sus ganancias, debe diligenciar un cuestionario de pago con nombre, documento y cuenta bancaria, que se borra después del pago.

La pregunta es «¿Aceptar términos?» con dos opciones: «Sí acepto participar.» / «No acepto participar.». Quien responde que no ve el mensaje «Por favor levante su mano y espere las indicaciones de los encargados.» y queda en la página; su único paso siguiente es `Agradecimiento` («Levanta tu mano y espera las indicaciones de los encargados.»). Todas las demás páginas de `debate` solo se muestran si el consentimiento fue afirmativo.

### 3. Instrucciones generales (`debate/Inst_iniciales.html`)

Explica que la actividad tiene 2 etapas y una encuesta. **El texto cambia según el brazo:** en la etapa 1 deberá argumentar «UNA de las dos» posiciones (brazo *una perspectiva*, `treatment = False`) o «las DOS» (brazo *dos perspectivas*, `treatment = True`). También anuncia que valorará cuatro argumentaciones y distribuirá 12.000 pesos según su calidad, y que otros valorarán la suya. De la etapa 2 dice que habrá 4 situaciones con pagos para dos personas y que una se elegirá al azar.

### 4. La situación y la posición inicial (`debate/Lectura_Dilema.html`, campos `posicion_afin` y `exp_emp`)

El dilema: un grupo de estudiantes de un colegio cercano a la Ciénaga Grande de Santa Marta denuncia la contaminación del agua producida por actividades ilegales; los grupos armados de la región se benefician de esas actividades y les han pedido que no se involucren más. Seguir denunciando protege la salud de la comunidad y pone en riesgo la vida de los estudiantes.

Después se pregunta la **posición inicial**: «¿Deberían los estudiantes seguir denunciando las actividades ilegales que están contaminando la Ciénaga?» con las opciones «A favor» / «En contra». Al elegir una, un script muestra la segunda pregunta, «¿Cómo eligió su posición?», con cuatro opciones (ver el diccionario de variables).

### 5. Antes de argumentar (`debate/Inicio_debate.html`)

Anuncia cuatro minutos para argumentar una de las dos posiciones, que la posición será asignada al azar («en las dos rondas» en el brazo *una perspectiva*, «en la ronda inicial» en el brazo *dos perspectivas*), que la otra persona se elige al azar, que después valorará las argumentaciones de otros tres participantes y que el pago de esta ronda estará entre 0 y 24.000 pesos según las valoraciones recibidas.

Nota: el límite real de las páginas de escritura es de cinco minutos (`timeout_seconds = 5*60`), no de cuatro.

### 6. Ronda 1: su argumento (`debate/Afavor.html` o `debate/Encontra.html`, campos `arg_a_favor` / `arg_en_contra`)

Se repite la pregunta y se indica la posición asignada en negrita: **A FAVOR DE DENUNCIAR** o **EN CONTRA DE DENUNCIAR** (`C.FAVOR` / `C.CONTRA`). La etiqueta del cuadro de texto es «Escriba su argumento, debe escribir como mínimo 5 palabras:». Al pie: «Cuando el tiempo acabe, avanzará automáticamente.» La página no tiene botón de avance.

### 7. Ronda 1: el argumento de la pareja (`debate/Leer_argumento.html`)

Muestra, en un recuadro, el argumento que escribió la pareja (la que defendió la otra posición).

### 8. Ronda 2: su réplica o su segundo argumento (`debate/Replica_afavor.html` o `debate/Replica_encontra.html`, campos `rep_a_favor` / `rep_en_contra`)

Aquí está la diferencia entre los brazos:

- **Una perspectiva** (`treatment = False`): «Ahora debe escribir una respuesta a la argumentación presentada por el otro participante», y «Responda manteniendo la posición asignada», con la misma posición de la ronda 1.
- **Dos perspectivas** (`treatment = True`): «Ahora debe escribir un argumento tomando la otra posición», y se indica la posición contraria a la de la ronda 1.

En los dos casos se muestra el argumento de la pareja. La etiqueta del cuadro de texto es «Escriba su respuesta, debe escribir como mínimo 5 palabras:». Tampoco hay botón de avance.

### 9. Ronda 2: la réplica de la pareja (`debate/Leer_argumento_replica.html`)

Muestra el texto de la ronda 2 de la otra persona.

### 10. Pregunta de aprobación social (`debate/Posicion_final.html`, campo `posicion_final`)

Pregunta qué tan socialmente apropiada es la decisión de los estudiantes de seguir denunciando, en cuatro niveles. Avisa que el computador calculará la respuesta de la mayoría y que **si la respuesta coincide con la de la mayoría, el participante recibe 4.000 pesos**. La moda se calcula sobre todos los participantes de la sesión (`set_calcular_moda_global`).

### 11. Instrucciones de la valoración (`debate/Instr_calificacion.html`)

Explica que valorará la calidad de su propia argumentación, la de su pareja y la de otros dos participantes elegidos al azar, siempre textos de la **ronda 1**; que debe asignar 6000, 4000, 2000 y 0 pesos, 6000 a la mejor y 0 a la peor; que al final cada participante sabrá cuánto le asignaron, y que en ningún momento se conocen las identidades.

### 12. Valoración de argumentos (`debate/Calificacion.html`, campos `calificacion_usted`, `calificacion_pareja`, `calificacion_jugador_afavor`, `calificacion_jugador_encontra`)

Una tabla con cuatro filas, cada una con el texto completo del argumento: «Argumentación de usted», «Argumentación de su pareja», «Argumentación de la persona 1» (el argumento *a favor* de la pareja vecina) y «Argumentación de la persona 2» (el argumento *en contra* de la pareja vecina). Arriba hay cuatro etiquetas arrastrables (0, 2000, 4000, 6000) que se sueltan en la casilla de cada fila; el valor queda en un campo oculto. La instrucción dice que no se puede poner el mismo valor a dos personas, pero el código no lo verifica en el servidor. El botón de avance de oTree está oculto y la página usa su propio botón «Siguiente».

### 13. Fin de la etapa 1 (`debate/Siguiente_etapa.html`, campo `descrip_calificacion`)

Al entrar se calculan los pagos de la valoración (`set_pagocalificacion`). Pide: «Describa cómo valoró la calidad de su argumentación y la de su pareja».

## App `conflict` (etapa 2: cuatro juegos de conflicto)

En las URL esta app aparece como `PD_Chat` (`NAME_IN_URL = 'PD_Chat'`), aunque en las exportaciones se llama `conflict`.

### 14. Instrucciones de la etapa 2 (`conflict/Introduction.html`, que incluye `conflict/instructions.html`)

Avisa que será emparejado de nuevo con la misma persona de la etapa anterior, que esa pareja se mantiene en cuatro situaciones distintas y que al final se elegirá una al azar para determinar los pagos. Explica que ambos eligen simultáneamente entre A y B, que los pagos de cada situación están en una tabla y que los números a la izquierda de cada casilla son los propios, resaltados en azul. X e Y son cantidades que cambian en cada situación y se muestran antes de decidir. La tabla genérica pone 16.000 para A–A, 4.000 para B–B y [X, Y] para las combinaciones mixtas.

Nota: en esta tabla genérica X es el pago de quien elige A, mientras que en `Decision.html` y en el código quien elige A recibe Y. Las dos letras están intercambiadas en la página de instrucciones.

### 15-18. Las cuatro decisiones (`conflict/Decision.html`, campo `cooperate`)

Una página por ronda, titulada «Situación 1» a «Situación 4». Repite las tres reglas con las cantidades concretas de esa situación, muestra la tabla de pagos con los valores en pesos y dos botones azules, A y B. Debajo: «Usted puede hablar con su pareja aquí.» y el chat de oTree, con el apodo «Participante 1» o «Participante 2». El chat es libre y opcional.

Entre rondas hay una página de espera que calcula los pagos cuando ambos han decidido.

### 19. Fin de la etapa 2 (`conflict/TotalResult.html`, campo `descrip_cooperate`)

Solo en la cuarta ronda. Pide «Describa cómo eligió entre la Opción A y la Opción B».

## App `results` (encuesta y pago)

### 20. Encuesta 1: IRI (`results/Survey.html`, campos `p_selection_1` a `p_selection_28`)

Los 28 ítems del Interpersonal Reactivity Index de Davis, en una tabla de cinco columnas con el encabezado «¿Qué tan bien lo(a) describe a usted cada una de las siguientes afirmaciones?» y la escala «No me describe bien (1)», «Me describe un poco (2)», «Me describe bien (3)», «Me describe bastante bien (4)», «Me describe muy bien (5)». Las 28 frases están en [`diccionario_variables.md`](diccionario_variables.md).

### 21. Encuesta 2: características (`results/Survey_2.html`)

Catorce preguntas numeradas en pantalla como 1, 2, 3, 4, 7, 10, 11, 12, 13, 14, 15, 16, 18 y 19 (la numeración salta porque en pantalla se dejaron los números de un cuestionario más largo): edad, sexo, carrera, semestre, estrato, experiencia previa en experimentos, ingresos semanales, educación de la madre, educación del padre, escalera de ingresos de 10 escalones, disposición al riesgo de 0 a 10, confianza general de 0 a 10, paciencia de 1 a 5 y confianza en el sistema judicial. Al avanzar se calcula el pago total.

### 22. Página final (`results/Final.html`)

Muestra, uno por uno, el pago por la respuesta de aprobación social, el pago por las valoraciones recibidas en la etapa 1, la ronda elegida al azar en la etapa 2 con lo ganado en ella, y la ganancia total. Avisa que la transferencia se hace en 48 horas hábiles desde que se diligencie el formulario de pago. Después imprime el **código de participante** de oTree en rojo y pide copiarlo y pegarlo en un formulario de Google al que se enlaza desde la misma página.

Ese formulario recogía nombre, documento y cuenta bancaria, y por eso no debe reutilizarse: quien adapte el experimento tiene que cambiar el enlace (ver `AGENTS.md`, sección 3).
