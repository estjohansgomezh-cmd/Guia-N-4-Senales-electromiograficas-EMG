# Práctica de Laboratorio N° 4: Señales Electromiográficas EMG
Universidad Militar Nueva Granada — Ingeniería Biomédica — Procesamiento Digital de Señales
---
## Descripción

En esta práctica se abordó la adquisición, acondicionamiento y procesamiento de señales electromiográficas (EMG) con el objetivo de evaluar cambios en sus características espectrales asociados a la fatiga muscular. La electromiografía de superficie (sEMG) permite registrar la actividad eléctrica muscular de forma no invasiva, capturando la suma de los potenciales de acción generados por las fibras musculares durante la contracción. A medida que el músculo se fatiga, la velocidad de conducción de las fibras disminuye como consecuencia de la acumulación de lactato y la reducción del ATP disponible, lo que se manifiesta como un desplazamiento del contenido espectral de la señal EMG hacia frecuencias más bajas.
Para cuantificar este fenómeno se emplearon dos medidaa espectrales clave: la frecuencia media (MNF) y la frecuencia mediana (MDF), complementadas con el análisis de espectros mediante la Transformada Rápida de Fourier (FFT).

La práctica se dividió en tres partes: la Parte A trabajó con una señal emulada por un generador de señales biológicas, la Parte B con una señal real adquirida de un individuo, y la Parte C realizó un análisis espectral profundo sobre la señal real mediante FFT, espectrograma y evolución del pico espectral.

## Metodología

Durante todo el desarrollo de la práctica se utilizó una ventana temporal de 1 segundo con un solapamiento del 50 %. Con una frecuencia de muestreo de 1000 Hz y con ventanas que contienen 1000 muestras. Esta elección garantiza continuidad entre segmentos y reduce la pérdida de información en los bordes. La señal analizada tuvo una duración total de 52 segundos, generando un total de 103 ventanas.

## PARTE A

Debido a las limitaciones del generador de señales, no fue posible configurar directamente una señal de tipo EMG que representara ciclos alternados de contracción y relajación (contracción–relajación–contracción–relajación).

Ante esta restricción, se plantearon dos estrategias para la obtención de la señal deseada. La primera consistía en registrar múltiples eventos de contracción por separado y posteriormente concatenarlos para formar una señal compuesta. La segunda alternativa consistía en adquirir una contracción muscular sostenida y, a partir de esta, segmentar la señal mediante el uso de ventanas temporales.

Finalmente, se optó por la segunda metodología, ya que permite un mejor control sobre el procesamiento y análisis de la señal, además de facilitar la aplicación de técnicas de segmentación en el dominio del tiempo.

Adicionalmente, con el fin de evitar la saturación del programa y del compilador durante el procesamiento, se tomó un fragmento representativo de la señal en un intervalo de tiempo determinado y se replicó sucesivamente hasta completar una duración total de 52 s.


<img width="2085" height="1036" alt="parteA_captura_vs_extendida_20260422_151228" src="https://github.com/user-attachments/assets/ada7d704-c26e-4c41-9a4f-6816911ab1f1" />


Para la Parte A, se empleó una ventana temporal de 1 s con un solapamiento (overlap) del 50 %. Considerando una frecuencia de muestreo de 1000 Hz, cada ventana corresponde a 1000 muestras. Esta elección permite capturar adecuadamente la dinámica de la señal EMG, mientras que el solapamiento garantiza continuidad entre segmentos y reduce la pérdida de información en los bordes de cada ventana.

Para efectos de visualización, en la figura presentada se muestran únicamente los primeros 5 s de la señal. No obstante, el análisis se realizó considerando la totalidad de las ventanas obtenidas (103 en total).


<img width="2087" height="744" alt="parteA_ventanas_superimposed_20260422_151228" src="https://github.com/user-attachments/assets/a1e60d44-4542-459c-8909-3adf3fcbac7c" />


En la gráfica de evolución temporal, se observa que tanto la frecuencia media (MNF) como la frecuencia mediana (MDF) presentan oscilaciones periódicas a lo largo del tiempo. Este comportamiento es consistente con el uso de ventanas superpuestas (50 % de overlap), lo que genera redundancia entre segmentos consecutivos.

A pesar de estas variaciones locales, no se evidencia una tendencia creciente o decreciente en ninguna de las dos métricas, lo cual se confirma con las líneas de tendencia prácticamente horizontales. Esto indica que no hay un desplazamiento del contenido espectral hacia frecuencias más bajas.


<img width="1937" height="744" alt="parteA_evolucion_frecuencias_20260422_151228" src="https://github.com/user-attachments/assets/e0b1747c-9936-4f9f-b656-696f97c235a4" />


En la figura de comparación espectral entre las primeras y últimas ventanas, se observa que la forma de la densidad espectral de potencia (PSD) es prácticamente igual en ambos casos. Las componentes de mayor energía se concentran en bajas frecuencias y el espectro decae progresivamente a medida que aumenta la frecuencia.

Al comparar las primeras tres ventanas con las últimas tres, no se evidencian cambios significativos en la distribución espectral. Además, los valores de la frecuencia media (MNF) mostrados en la gráfica son muy similares entre ambos grupos de ventanas, lo que indica que el contenido frecuencial de la señal se mantiene estable a lo largo del tiempo.


<img width="1935" height="742" alt="parteA_espectros_comparacion_20260422_151228" src="https://github.com/user-attachments/assets/86d392ed-7db0-46dd-a114-eadbc500af1a" />


A partir de ambas imagenes, se concluye que no hay evidencia de fatiga muscular en la señal analizada. En un escenario real, la fatiga se manifestaría como una disminución progresiva de la MNF y la MDF, acompañada de un desplazamiento del espectro hacia bajas frecuencias.

Sin embargo, en este caso la señal proviene de un generador, por lo que sus características espectrales permanecen constantes en el tiempo. En consecuencia, no es posible simular de manera realista el fenómeno de fatiga muscular, lo cual explica la estabilidad observada en ambas gráficas.

## PARTE B

Debido a que la señal en la Parte B corresponde a una medición real (adquirida de un sujeto), fue necesario realizar un preprocesamiento previo para garantizar la calidad de la señal EMG. En este sentido, se aplicó un filtro pasa banda entre 20 Hz y 450 Hz, con el fin de eliminar componentes de baja frecuencia asociadas a movimiento y ruido de línea base, así como componentes de alta frecuencia relacionadas con ruido eléctrico.

A diferencia de la Parte A, en este caso se trabajó directamente con una señal continua adquirida experimentalmente, lo que permitió conservar la variabilidad natural del fenómeno fisiológico a lo largo del tiempo.


<img width="2085" height="1038" alt="parteB_1_cruda_vs_filtrada_20260421_210538" src="https://github.com/user-attachments/assets/1ba4e341-206a-400f-840c-f77f3e6116f3" />


Al igual que en la Parte A, se empleó una ventana temporal de 1 s con un solapamiento (overlap) del 50 %. Considerando una frecuencia de muestreo de 1000 Hz, cada ventana corresponde a 1000 muestras. Esta configuración permite una adecuada segmentación de la señal, manteniendo continuidad entre ventanas y reduciendo la pérdida de información en los bordes.

Esta misma metodología fue aplicada sobre una señal con una duración total de 52 s. Para efectos de visualización, se presentan únicamente los primeros 5 s de la señal; sin embargo, el análisis se realizó considerando la totalidad de las ventanas obtenidas.


<img width="2087" height="744" alt="parteB_2_ventanas_superimposed_20260421_210538" src="https://github.com/user-attachments/assets/cc2c5f30-83fc-4855-84eb-65af2e6ee099" />


En la gráfica de evolución temporal se presentan tres representaciones complementarias: los datos originales de la MNF y la MDF (mostrados de forma tenue), las curvas suavizadas mediante media móvil (líneas sólidas) y las tendencias lineales (líneas punteadas).

El suavizado por media móvil permite reducir la variabilidad inherente de la señal EMG y resaltar el comportamiento global de las métricas espectrales. Gracias a esto, se observa con mayor claridad la evolución de la señal a lo largo del tiempo, sin perder la referencia de los datos reales.

Aunque las tendencias lineales no muestran una disminución pronunciada y presentan una ligera pendiente positiva, se evidencian fluctuaciones en las curvas suavizadas que reflejan cambios en el contenido frecuencial de la señal. Este comportamiento es consistente con la naturaleza no estacionaria de señales fisiológicas reales.


<img width="1937" height="744" alt="parteB_3_evolucion_frecuencias_20260421_210538" src="https://github.com/user-attachments/assets/a8e34162-c6a0-457e-963d-edec3001f1f8" />


En la comparación entre las primeras y últimas ventanas, se observan diferencias en la distribución de la densidad espectral de potencia (PSD).

En las primeras ventanas, la señal presenta una mayor concentración de energía en frecuencias medias-altas (aproximadamente entre 100 y 200 Hz). En contraste, en las últimas ventanas se evidencia una ligera redistribución del contenido espectral hacia frecuencias más bajas, junto con una disminución relativa de las componentes de mayor frecuencia.

Adicionalmente, los valores de la frecuencia media (MNF) muestran mayor variabilidad en las últimas ventanas en comparación con las iniciales, lo cual es característico de señales EMG reales y refleja cambios en la actividad muscular a lo largo del tiempo.


<img width="1935" height="742" alt="parteB_4_espectros_comparacion_20260421_210538" src="https://github.com/user-attachments/assets/ebdd4a0e-df07-4bcc-9c99-ab55e6570ade" />


A diferencia de la Parte A, en este caso la señal proviene de una medición real, por lo que presenta una mayor variabilidad tanto en el dominio temporal como frecuencial.

Se observan indicios de fatiga muscular, principalmente en la redistribución del contenido espectral hacia frecuencias más bajas en las últimas ventanas y en la variabilidad de las métricas espectrales a lo largo del tiempo. Este comportamiento está asociado a la disminución de la velocidad de conducción de las fibras musculares durante el esfuerzo sostenido.

No obstante, la ausencia de una tendencia claramente decreciente en la MNF y la MDF indica que la fatiga no se manifiesta de manera uniforme, lo cual es esperable en registros reales debido a factores como variaciones en la contracción, ruido y características propias del sujeto.


## PARTE C

<img width="1760" height="744" alt="parteC_G1_fft_todas_emulada_20260423_110109" src="https://github.com/user-attachments/assets/8d820cc3-6240-4232-abc4-8920ecfbda96" />

La grfica presenta la superposición de todos los espectros de amplitud de la señal EMG emulada a lo largo de la contracción sostenida. Se observa un comportamiento espectral altamente regular y predecible, típico de una señal sintética estacionaria. La distribución de energía es constante en todas las ventanas de tiempo, con picos de frecuencia que no varían independientemente de la duración del esfuerzo. La barra de colores confirma que no hay una evolución temporal significativa, indicando la ausencia de procesos fisiológicos como la fatiga muscular. Esta señal sirve como control para diferenciar un comportamiento ideal de uno biológico.

<img width="1760" height="744" alt="parteC_G2_fft_todas_real_20260423_110109" src="https://github.com/user-attachments/assets/1e8ca791-00f3-44b8-9af6-1813fc745a0c" />

En contraste con la señal emulada, la grafica de la señal real muestra la superposición de los espectros de amplitud de la señal EMG real. Este espectro es característico de un proceso biológico estocástico, reflejando la suma asincrónica de los potenciales de acción de múltiples unidades motoras. Se evidencia una mayor variabilidad y una distribución de energía más densa en comparación con G1. Aunque la superposición dificulta la visualización detallada de la evolución temporal, la 'riqueza' espectral y la dispersión de los picos son indicativos de la complejidad de la activación muscular y sugieren la presencia de cambios fisiológicos dinámicos a lo largo de la contracción sostenida.

<img width="2085" height="742" alt="parteC_G3_primeras_vs_ultimas_emulada_20260423_110109" src="https://github.com/user-attachments/assets/eeece868-8962-49b6-9aff-9fb72f471f38" />

La anterior grafica compara los espectros de amplitud de las primeras tres ventanas de tiempo (inicio de la contracción) con las últimas tres (final de la contracción) para la señal emulada. Esta comparación directa confirma la estabilidad temporal observada en G1. El contenido de frecuencia permanece idéntico, con picos principales consistentes en 21.0 Hz para todas las ventanas analizadas. La falta de variación entre el inicio y el final del 'esfuerzo' ratifica que la señal sintética no reproduce los fenómenos de fatiga muscular, sirviendo como un control negativo de referencia.

<img width="2085" height="742" alt="parteC_G4_primeras_vs_ultimas_real_20260423_110109" src="https://github.com/user-attachments/assets/9eae18b3-4a3f-452a-9210-e0a1313fe0db" />

La grafica presenta una comparación directa de las FFT de las primeras y últimas ventanas de tiempo para la señal real, revelando diferencias significativas. Se observa una marcada alteración en la distribución de energía y en la forma de los espectros a medida que progresa la contracción sostenida. Al inicio, los espectros muestran una mayor dispersión con presencia en frecuencias más altas. Hacia el final, la energía tiende a concentrarse de manera diferente, y los picos de frecuencia identificados son notablemente variables. Esta variabilidad y el cambio en la forma espectral son indicadores directos de la fatiga muscular y de la adaptación del sistema neuromuscular.

<img width="1891" height="1330" alt="parteC_G5_espectrograma_20260423_110109" src="https://github.com/user-attachments/assets/7404a95d-588a-4dc3-ab64-1a327dd47c13" />

La anterior grafica proporciona una representación visual clara de la evolución temporal del contenido de frecuencia mediante espectrogramas. El espectrograma de la señal emulada (panel superior) es uniforme y constante, con una línea de tendencia del pico espectral prácticamente plana ($+0.009 \text{ Hz/s}$), confirmando la ausencia de cambios. Por el contrario, el espectrograma de la señal real (panel inferior) muestra una dinámica compleja con variaciones en la intensidad a través de diferentes frecuencias. La línea de tendencia amarilla revela un desplazamiento ascendente del pico espectral ($+0.094 \text{ Hz/s}$), indicando un cambio medible en la frecuencia dominante a lo largo de la contracción sostenida.

<img width="1937" height="744" alt="parteC_G6_pico_espectral_20260423_110109" src="https://github.com/user-attachments/assets/7e2192c8-0a30-4c9f-b668-588e3fbc8e79" />

La ultima grafica cuantifica el desplazamiento del pico espectral, el indicador clave de fatiga analizado. Se confirma que la señal emulada mantiene una frecuencia de pico constante (línea azul), reflejando una tendencia nula ($+0.00 \text{ Hz}$ de desplazamiento total). La señal real muestra un comportamiento radicalmente diferente: a pesar de fluctuaciones significativas (línea roja cruda), la tendencia suavizada es marcadamente ascendente ($+0.094 \text{ Hz/s}$). Este aumento sistemático en la frecuencia del pico dominante, con un desplazamiento total de $+77.33 \text{ Hz}$ según el resumen, es la evidencia definitiva del proceso de fatiga muscular en este experimento.

<img width="500" height="262" alt="image" src="https://github.com/user-attachments/assets/b47e3f0c-8972-4c8f-817f-caa45d40dee6" />

La tabla adjunta resume las métricas clave de la Parte C, corroborando cuantitativamente todas las observaciones visuales. La señal emulada presenta una tendencia plana ($+0.0093 \text{ Hz/s}$) y un desplazamiento nulo ($+0.00 \text{ Hz}$), concluyendo un comportamiento típico de una señal periódica estable. La señal real muestra un aumento significativo en la frecuencia del pico, con un desplazamiento total de $+77.33 \text{ Hz}$ y una tendencia ascendente clara ($+0.0942 \text{ Hz/s}$). Estos resultados demuestran de manera inequívoca la presencia de fatiga muscular durante la contracción real y validan el uso del análisis espectral mediante FFT como una herramienta sensible para su detección y cuantificación.

## Análisis de resultados 

Al analizar las señales electromiográficas obtenidas, se observa un incremento progresivo tanto en la amplitud como en la frecuencia de la señal a lo largo del tiempo. En un principio, este comportamiento podría interpretarse como un indicio de fatiga muscular; sin embargo, al examinar la tendencia de los datos, se evidencia que no corresponde a un estado de fatiga.

En condiciones de fatiga muscular, es común observar una disminución en la frecuencia de la señal y una reducción en la amplitud debido a la incapacidad del músculo para mantener el mismo nivel de activación. No obstante, en este caso ocurre lo contrario: los picos de la señal aumentan y la frecuencia se incrementa, lo que indica una mayor actividad eléctrica.

Este comportamiento puede explicarse mediante el reclutamiento progresivo de unidades motoras. A medida que el músculo requiere mantener o aumentar la fuerza, el sistema nervioso activa más unidades motoras, incluyendo fibras musculares de contracción rápida, lo que genera un aumento en la amplitud y frecuencia de la señal EMG.

Por lo tanto, los resultados obtenidos no evidencian fatiga muscular, sino una respuesta adaptativa del sistema neuromuscular ante la demanda del ejercicio, caracterizada por un aumento en el reclutamiento de unidades motoras.

## Conclusiones

A partir del análisis de las señales electromiográficas, se concluye que no se evidenció un estado de fatiga muscular durante la adquisición de los datos. Aunque podrían presentarse indicios iniciales, el comportamiento general de la señal muestra un incremento en la amplitud y la frecuencia, lo cual no es característico de la fatiga.

En cambio, los resultados sugieren un aumento en el reclutamiento de unidades motoras por parte del sistema nervioso, como mecanismo para mantener o incrementar la fuerza muscular. Este fenómeno se refleja en una mayor actividad eléctrica registrada en la señal EMG.

Finalmente, se puede afirmar que el sistema neuromuscular respondió de manera adaptativa ante el esfuerzo, activando progresivamente más fibras musculares en lugar de presentar una disminución en el rendimiento asociada a la fatiga.

## Preguntas para la discusión

- ¿Cambian los valores de frecuencia media y mediana a medida que el músculo se acerca a la fatiga? ¿A qué podría atribuirse este cambio?
  
  En condiciones de fatiga muscular, los valores de la frecuencia media (MNF) y la frecuencia mediana (MDF) tienden a disminuir progresivamente. Este comportamiento se atribuye principalmente a la reducción de la velocidad de conducción de las fibras musculares, especialmente las de tipo II, debido a la acumulación de metabolitos como los iones de hidrógeno, lo que genera una disminución del pH intramuscular. Como consecuencia, los potenciales de acción se ensanchan en el tiempo, desplazando el contenido espectral hacia frecuencias más bajas.
Adicionalmente, durante la fatiga se presentan cambios en el reclutamiento de unidades motoras, donde las de mayor umbral pueden perder eficiencia, favoreciendo una mayor participación relativa de unidades motoras de menor frecuencia.
Sin embargo, en los resultados obtenidos en esta práctica no se evidencia una disminución clara y sostenida de la MNF y la MDF. Por el contrario, el comportamiento de la señal sugiere que no se alcanzó un estado de fatiga muscular definido, sino que se presentaron únicamente indicios parciales. Esto puede explicarse por un aumento en el reclutamiento de unidades motoras, lo cual compensa los efectos esperados de la fatiga y evita una caída marcada en las frecuencias.

- ¿Cómo justifica el uso de herramientas como la transformada de Fourier en escenarios como, por ejemplo, terapias de rehabilitación?
  
  La transformada de Fourier es una herramienta fundamental en el análisis de señales electromiográficas, ya que permite transformar una señal en el dominio del tiempo a su representación en frecuencia, facilitando la interpretación de la actividad muscular.
En el contexto de la rehabilitación, su uso se justifica porque permite evaluar de manera objetiva el estado funcional del músculo. A través del análisis espectral, es posible identificar cambios en la activación muscular, como variaciones en la frecuencia asociadas a procesos de fatiga o recuperación.
Además, permite monitorear la evolución del paciente a lo largo del tratamiento, comparando métricas como la frecuencia media y mediana entre diferentes sesiones. Esto ayuda a determinar si existe una mejora en la función muscular o si se presentan patrones anormales de activación.
También es útil para detectar compensaciones musculares, ya que cambios en el contenido espectral pueden indicar que otros músculos están siendo utilizados de forma inadecuada para realizar un movimiento.
En general, la transformada de Fourier convierte señales complejas en información cuantificable y clínicamente útil, lo que la hace una herramienta clave en el diagnóstico, seguimiento y optimización de terapias de rehabilitación.

## Referencias

1. Y. Tan, Y. Liu, R. Ye, H. Xu, W. Nie, J. Lu, B. Zhang, C. Wang y B. He,“Change of bio-electric interferential currents of acute fatigue and recovery in male sprinters,” Sports Medicine and Health Science, vol. 2, no. 1, pp. 1–6, 2020. https://doi.org/10.1016/j.smhs.2020.02.004.
2. K. Sahlin, “Metabolic factors in fatigue,” Sports Medicine: An International Journal of Applied Medicine and Science in Sport and Exercise, vol. 13, no. 2, pp. 99–107, 1992. https://doi.org/10.2165/00007256-199213020-00005.
3. D. Constantin-Teodosiu y D. Constantin, “Molecular mechanisms of muscle fatigue,” International Journal of Molecular Sciences, vol. 22, no. 21, art. 11587, 2021. https://doi.org/10.3390/ijms222111587.
4. A. Urdampilleta, I. Armentia, S. Gómez-Zorita, J. M. Martínez-Sanz y J. Mielgo-Ayuso, “La fatiga muscular en los deportistas: Métodos físicos,

