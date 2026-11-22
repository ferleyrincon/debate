# Diccionario de variables

Todos los campos que produce el experimento, con la pregunta o la etiqueta que vio el participante. Fuente: `debate/__init__.py`, `conflict/__init__.py`, `results/__init__.py` y las plantillas HTML citadas en cada sección. Las variables de oTree que vienen por defecto (`participant.code`, `participant.payoff`, `session.code`, `player.id_in_group`, `subsession.round_number`, …) no se listan.

Totales: 21 campos en `debate` (13 de jugador + 8 de grupo), 4 en `conflict` (2 de jugador + 2 de grupo) y 43 en `results`.

## App `debate`

### Campos de jugador

| Campo | Tipo | Página | Qué vio el participante |
|---|---|---|---|
| `agree` | Booleano, asignado por el código | — (se usa en todas) | No se le mostró. Es el **lado sorteado**: `True` = A FAVOR DE DENUNCIAR, `False` = EN CONTRA DE DENUNCIAR. Se sortea en `creating_session`: el jugador 1 recibe un lado al azar y el jugador 2 el opuesto |
| `consentimiento` | Booleano, radio | `Consentimiento.html` | «¿Aceptar términos?» → «Sí acepto participar.» (True) / «No acepto participar.» (False) |
| `posicion_afin` | Booleano, radio | `Lectura_Dilema.html` | «¿Deberían los estudiantes seguir denunciando las actividades ilegales que están contaminando la Ciénaga?» → «A favor» (True) / «En contra» (False). Es la **posición propia antes del debate**, no la asignada |
| `exp_emp` | Entero 1-4, radio | `Lectura_Dilema.html` | «¿Cómo eligió su posición?» → 1 «Consideré las consecuencias que puede tener esta situación para los estudiantes.»; 2 «Imaginé cómo me sentiría si estuviera en el lugar de los estudiantes.»; 3 «Pensé en cómo pueden sentirse los estudiantes y los demás afectados por esta situación.»; 4 «Me sentí incómodo al pensar en los riesgos que enfrentan los estudiantes al denunciar.» |
| `posicion_final` | Entero 1-4, radio | `Posicion_final.html` | «¿Qué tan socialmente apropiado cree que es la decisión de los estudiantes de seguir denunciando las actividades ilegales que están contaminando la Ciénaga?» → 1 «Muy socialmente inapropiada»; 2 «Socialmente inapropiada»; 3 «Socialmente apropiada»; 4 «Muy socialmente apropiada» |
| `calificacion_usted` | Entero (0, 2000, 4000 o 6000) | `Calificacion.html` | Dinero que asignó a su **propia** argumentación de la ronda 1 (fila «Argumentación de usted») |
| `calificacion_pareja` | Entero (0, 2000, 4000 o 6000) | `Calificacion.html` | Dinero que asignó a la argumentación de **su pareja** (fila «Argumentación de su pareja») |
| `calificacion_jugador_afavor` | Entero (0, 2000, 4000 o 6000) | `Calificacion.html` | Dinero que asignó al argumento **a favor** de la pareja vecina (fila «Argumentación de la persona 1») |
| `calificacion_jugador_encontra` | Entero (0, 2000, 4000 o 6000) | `Calificacion.html` | Dinero que asignó al argumento **en contra** de la pareja vecina (fila «Argumentación de la persona 2») |
| `calificacion_otros` | Entero, calculado | — | Suma de lo que los dos participantes de la pareja vecina asignaron al argumento de este jugador. Lo calcula `set_pagocalificacion` |
| `pago_cal_usted` | Entero, calculado | `Siguiente_etapa.html` | Pago de la etapa 1: su autovaloración + lo que le asignó su pareja + `calificacion_otros`. Puede ir de 0 a 24.000 pesos |
| `pago_aprobacion_social` | Entero, calculado | `Final.html` | 4000 si `posicion_final` coincide con la moda de la sesión, 0 si no (`set_calcular_moda_global`) |
| `descrip_calificacion` | Texto largo | `Siguiente_etapa.html` | «Describa cómo valoró la calidad de su argumentación y la de su pareja» |

### Campos de grupo (la pareja)

| Campo | Tipo | Página | Contenido |
|---|---|---|---|
| `treatment` | Booleano, asignado por el código | — | **Brazo de la pareja**: `True` = dos perspectivas (en la ronda 2 cada uno argumenta el lado contrario), `False` = una perspectiva (en la ronda 2 cada uno responde manteniendo su lado). Se sortea en `creating_session`, mitad y mitad de las parejas |
| `arg_a_favor` | Texto largo | `Afavor.html` | Argumento de la ronda 1 a favor de denunciar. Etiqueta: «Escriba su argumento, debe escribir como mínimo 5 palabras:» |
| `arg_en_contra` | Texto largo | `Encontra.html` | Argumento de la ronda 1 en contra de denunciar. Misma etiqueta |
| `rep_a_favor` | Texto largo | `Replica_afavor.html` | Texto de la ronda 2 a favor de denunciar. Etiqueta: «Escriba su respuesta, debe escribir como mínimo 5 palabras:» |
| `rep_en_contra` | Texto largo | `Replica_encontra.html` | Texto de la ronda 2 en contra de denunciar. Misma etiqueta |
| `arg_cal_afavor` | Texto largo, copiado | `Calificacion.html` | El argumento `arg_a_favor` de la pareja vecina, mostrado como «Argumentación de la persona 1». Lo copia `set_argumento` |
| `arg_cal_contra` | Texto largo, copiado | `Calificacion.html` | El argumento `arg_en_contra` de la pareja vecina, mostrado como «Argumentación de la persona 2» |
| `has_arrived` | Booleano, `initial=False` | — | **No se usa.** Está declarado y nunca se escribe: siempre `False` |

## App `conflict` (`PD_Chat` en las URL), 4 rondas

| Campo | Tipo | Página | Qué vio el participante |
|---|---|---|---|
| `cooperate` | Booleano, dos botones | `Decision.html` | «elija entre A o B» → botón **A** (True) / botón **B** (False). A es la opción que da 16.000 a cada uno si ambos la eligen |
| `descrip_cooperate` | Texto largo | `TotalResult.html` (solo ronda 4) | «Describa cómo eligió entre la Opción A y la Opción B» |
| `levels` (grupo) | Texto, asignado por el código | — | Orden sorteado de las cuatro situaciones, como `"2,0,3,1"`. Solo sirve el valor de la **ronda 1**: es el que se copia a `participant.vars` y gobierna lo que se muestra en las cuatro rondas |
| `selected_round` (grupo) | Entero 1-4, asignado por el código | `Final.html` | Ronda sorteada para pagar la etapa 2. También solo sirve el valor de la ronda 1 |

Los cuatro niveles de pago (`X_VALUES`, `Y_VALUES`) son: 0 → X 8000, Y 8000; 1 → X 8000, Y 0; 2 → X 24000, Y 8000; 3 → X 24000, Y 0. A–A paga 16.000 a cada uno y B–B paga 4.000. Ojo con el desajuste entre la situación mostrada y la pagada descrito en el `README.md` principal.

El chat de cada página de decisión se guarda aparte (exportación «Chat messages» del administrador) con el apodo «Participante 1» / «Participante 2».

## App `results`

### Encuesta 1: Interpersonal Reactivity Index (`Survey.html`)

28 ítems, todos con la misma escala: 1 «No me describe bien», 2 «Me describe un poco», 3 «Me describe bien», 4 «Me describe bastante bien», 5 «Me describe muy bien». Encabezado: «¿Qué tan bien lo(a) describe a usted cada una de las siguientes afirmaciones?».

| Campo | Afirmación |
|---|---|
| `p_selection_1` | Sueño y fantaseo, con cierta regularidad, acerca de las cosas que me podrían suceder. |
| `p_selection_2` | A menudo tengo sentimientos tiernos y de preocupación hacia la gente menos afortunada que yo. |
| `p_selection_3` | A menudo me cuesta ver las cosas desde el punto de vista de otras personas. |
| `p_selection_4` | A veces no me siento muy preocupado por otras personas cuando tienen problemas. |
| `p_selection_5` | Verdaderamente me identifico con los sentimientos de los personajes de una novela. |
| `p_selection_6` | En situaciones de emergencia me siento aprensivo e incómodo. |
| `p_selection_7` | Normalmente soy objetivo cuando veo una película u obra de teatro y no me involucro completamente. |
| `p_selection_8` | Intento tener en cuenta cada una de las partes (opiniones) en un conflicto antes de tomar una decisión. |
| `p_selection_9` | Cuando veo que a alguien se le toma el pelo, tiendo a protegerlo. |
| `p_selection_10` | Normalmente siento desesperanza cuando estoy en medio de una situación muy emotiva. |
| `p_selection_11` | A menudo intento comprender mejor a mis amigos imaginándome cómo ven ellos las cosas (poniéndome en su lugar). |
| `p_selection_12` | Me resulta raro implicarme completamente en un buen libro o película. |
| `p_selection_13` | Cuando veo a alguien herido, tiendo a permanecer calmado. |
| `p_selection_14` | Las desgracias de otros normalmente no me molestan mucho. |
| `p_selection_15` | Si estoy seguro de que tengo la razón en algo, no pierdo tiempo escuchando los argumentos de los demás. |
| `p_selection_16` | Después de ver una obra de teatro o cine, me he sentido como si fuera uno de los personajes. |
| `p_selection_17` | Cuando estoy en una situación emocionalmente tensa, me asusto. |
| `p_selection_18` | Cuando veo a alguien que está siendo tratado injustamente, a veces no siento ninguna compasión por él. |
| `p_selection_19` | Normalmente soy bastante eficaz al ocuparme de emergencias. |
| `p_selection_20` | A menudo estoy bastante afectado emocionalmente por cosas que veo que ocurren. |
| `p_selection_21` | Pienso que hay dos partes para cada cuestión e intento tener en cuenta ambas partes. |
| `p_selection_22` | Me describiría como una persona bastante sensible. |
| `p_selection_23` | Cuando veo una buena película, puedo muy fácilmente situarme en el lugar del protagonista. |
| `p_selection_24` | A menudo pierdo el control durante las emergencias. |
| `p_selection_25` | Cuando estoy disgustado con alguien, normalmente intento ponerme en su lugar por un momento. |
| `p_selection_26` | Cuando estoy leyendo una historia interesante o una novela, imagino cómo me sentiría si los acontecimientos de la historia me sucedieran a mí. |
| `p_selection_27` | Cuando veo a alguien que necesita urgentemente ayuda en una emergencia, me derrumbo. |
| `p_selection_28` | Antes de criticar a alguien, intento imaginar cómo me sentiría si estuviera en su lugar. |

Las subescalas (Toma de perspectiva, Preocupación empática, Fantasía, Malestar personal) no están marcadas en el código: se construyen en el análisis.

### Encuesta 2: características (`Survey_2.html`)

El número entre paréntesis es el que se muestra en pantalla.

| Campo | Pregunta en pantalla | Opciones |
|---|---|---|
| `age` | (1) Edad | Entero libre |
| `gender_sex` | (2) Sexo | 0 «Masculino», 1 «Femenino», 2 «Otro» |
| `major` | (3) ¿Qué carrera cursó o cursa actualmente? | Lista de 63 opciones, de 1 «Administración de Empresas» a 62 «Contaduría» y 63 «Otra» (ver `results/__init__.py`) |
| `semester` | (4) Semestre que cursa del pregrado (si ya finalizó su pregrado seleccione «Egresado») | 0 «Egresado», 1 a 12, 13 «más de 12» |
| `stratum` | (7) De acuerdo con las facturas de servicios, ¿cuál es el estrato de la vivienda en la cual reside? | 0 «No estratificado», 1 a 6 |
| `experiments` | (10) ¿Ha participado antes en experimentos de economía o psicología? | 0 «No», 1 «Sí» |
| `income` | (11) A cuánto ascienden aproximadamente sus ingresos semanales (en pesos). Incluya todo tipo de ingresos (mesadas, ingresos laborales, rentas, etc.) | Entero, mínimo 1000 |
| `mother_educ` | (12) ¿Cuál es el máximo nivel de educación alcanzado por su madre? | 1 «Ninguno», 2 «Primaria», 3 «Secundaria/Bachillerato», 4 «Educación universitaria/tecnológica», 5 «Posgrado», 0 «No sabe» |
| `father_educ` | (13) ¿Cuál es el máximo nivel de educación alcanzado por su padre? | Las mismas seis opciones |
| `income_stair` | (14) Imagine una escalera con 10 escalones. Las personas con los ingresos más bajos se sitúan en el escalón 1 y las personas con los ingresos más altos en el escalón 10. ¿Dónde situarías a tu grupo familiar? | 1 a 10 |
| `risk_measure` | (15) En una escala del 0 al 10, donde 0 significa que «no está dispuesto(a) a tomar riesgos en lo absoluto» y 10 significa que «está muy dispuesto(a) a tomar riesgos», ¿qué tan dispuesto(a) está usted a tomar riesgos? | 0 a 10 |
| `G_trust` | (16) En una escala del 0 al 10, donde 0 significa «Por lo general, hay que tener mucho cuidado de las personas» y 10 significa «Por lo general, se puede confiar en la gente», ¿usted diría que se puede confiar en la mayoría de la gente o que hay que tener mucho cuidado al tratar con las personas? | 0 a 10 |
| `patience` | (18) En su vida personal, ¿en qué medida está dispuesto a renunciar a algo que puede ser beneficioso para usted hoy a cambio de obtener mayores beneficios en el futuro? 1 = no está dispuesto, 5 = totalmente dispuesto a esperar | 1 a 5 |
| `punish_justice` | (19) Si usted fuera víctima de un robo o asalto, ¿cuánto confiaría que el sistema judicial castigue al culpable? | 4 «Mucho», 3 «Algo», 2 «Poco», 1 «Nada» |

### Pago

| Campo | Tipo | Página | Contenido |
|---|---|---|---|
| `payoff_complete` | Entero, calculado | `Final.html` | `C.SHOWFEE` (10000) + lo ganado en la ronda sorteada de la etapa 2 + `pago_cal_usted` + `pago_aprobacion_social` |
