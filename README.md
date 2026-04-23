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

<img width="1937" height="744" alt="parteC_G6_pico_espectral_20260423_110109" src="https://github.com/user-attachments/assets/7e2192c8-0a30-4c9f-b668-588e3fbc8e79" />
<img width="1891" height="1330" alt="parteC_G5_espectrograma_20260423_110109" src="https://github.com/user-attachments/assets/7404a95d-588a-4dc3-ab64-1a327dd47c13" />
<img width="2085" height="742" alt="parteC_G4_primeras_vs_ultimas_real_20260423_110109" src="https://github.com/user-attachments/assets/9eae18b3-4a3f-452a-9210-e0a1313fe0db" />
<img width="2085" height="742" alt="parteC_G3_primeras_vs_ultimas_emulada_20260423_110109" src="https://github.com/user-attachments/assets/eeece868-8962-49b6-9aff-9fb72f471f38" />
<img width="1760" height="744" alt="parteC_G2_fft_todas_real_20260423_110109" src="https://github.com/user-attachments/assets/1e8ca791-00f3-44b8-9af6-1813fc745a0c" />
<img width="1760" height="744" alt="parteC_G1_fft_todas_emulada_20260423_110109" src="https://github.com/user-attachments/assets/8d820cc3-6240-4232-abc4-8920ecfbda96" />
<img width="500" height="262" alt="image" src="https://github.com/user-attachments/assets/b47e3f0c-8972-4c8f-817f-caa45d40dee6" />


## Análisis de resultados 

Al contrastar los resultados de las tres partes, emerge uno fundamental: la señal emulada (Parte A) no puede reproducir el fenómeno de fatiga por su naturaleza sintética, mientras que la señal real (Partes B y C) sí muestra indicios del proceso fisiológico, aunque de forma moderada y con ruido inherente a las condiciones de adquisición.

Desde el punto de vista fisiológico, la fatiga muscular se manifiesta espectralmente porque durante el esfuerzo sostenido disminuye la velocidad de conducción de las fibras musculares tipo II (rápidas), las cuales contribuyen con las componentes de mayor frecuencia al espectro EMG. A medida que estas fibras se fatigan, el espectro pierde energía en la banda alta y la gana en la baja, produciendo el descenso de MNF y MDF. Este mecanismo es el que permite usar el sEMG como indicador no invasivo de fatiga.

La metodología de ventaneo con overlap del 50 % demostró ser adecuada para capturar la dinámica temporal de las métricas espectrales. Sin embargo, para una detección más robusta de fatiga sería recomendable combinar estas métricas con indicadores del dominio del tiempo como el RMS (Root Mean Square), que típicamente aumenta con la fatiga como mecanismo compensatorio de reclutamiento de unidades motoras adicionales.

## Conclusiones

1. La práctica demostró que el análisis espectral mediante FFT, junto con el cálculo de la frecuencia media y mediana, constituye una herramienta válida y no invasiva para estudiar la fatiga muscular a través de señales EMG de superficie.
2. En la señal emulada (Parte A), la estabilidad absoluta de las métricas espectrales confirmó que un generador de señales no puede reproducir la dinámica fisiológica de la fatiga, lo que evidencia la importancia de trabajar con señales reales cuando el objetivo es el análisis de fenómenos biológicos.
3. En la señal real (Partes B y C), se observaron indicios de redistribución espectral hacia bajas frecuencias en las últimas ventanas, mayor variabilidad en la MNF y diferencias en los espectros FFT entre el inicio y el final del registro. Estos resultados son consistentes con los fundamentos teóricos de la fatiga muscular, aunque la magnitud de los cambios fue moderada, posiblemente porque la fatiga completa no fue alcanzada durante la sesión.
4. Respecto a la factibilidad de emplear técnicas espectrales en escenarios no controlados, como el entrenamiento de atletas, los resultados sugieren que es posible pero exige consideraciones adicionales: control de artefactos de movimiento, selección apropiada del músculo a monitorear, estandarización del protocolo de adquisición y el uso de sistemas portátiles de bajo ruido. En estos entornos dinámicos, la variabilidad de la señal es mayor, por lo que el suavizado y las técnicas de análisis tiempo-frecuencia (como el espectrograma) resultan especialmente útiles para extraer tendencias significativas.

## Preguntas para la discusión

- ¿Cambian los valores de frecuencia media y mediana a medida que el músculo se acerca a la fatiga? ¿A qué podría atribuirse este cambio?
  
  Sí, tanto la MNF como la MDF tienden a disminuir progresivamente cuando el músculo se aproxima a la fatiga.
  Este cambio se atribuye principalmente a la reducción de la velocidad de conducción de las fibras musculares, en especial las de tipo II (rápidas), como consecuencia de la acumulación de iones de hidrógeno (acidosis metabólica) asociada al incremento de lactato y la disminución del pH intramuscular. Al disminuir la velocidad de conducción, los potenciales de acción de cada unidad motora se ensanchan en el tiempo, lo que equivale espectralmente a que su energía se desplace hacia frecuencias más bajas. Adicionalmente, durante la fatiga se produce un cambio en el patrón de reclutamiento: las unidades motoras de mayor umbral (que contribuyen con componentes de alta frecuencia) comienzan a fallar, mientras las de menor umbral (frecuencias más bajas) siguen activas. La combinación de estos dos mecanismos explica el descenso observado en MNF y MDF como marcadores espectrales de fatiga.
  En los resultados de esta práctica, la señal real (Partes B y C) mostró indicios de este comportamiento en forma de redistribución espectral hacia bajas frecuencias en las últimas ventanas, aunque sin una tendencia decreciente completamente definida, lo que sugiere que la fatiga se alcanzó de forma parcial durante el registro.
  
- ¿Cómo justifica el uso de herramientas como la transformada de Fourier en escenarios como, por ejemplo, terapias de rehabilitación?
  
  La transformada de Fourier es fundamental en rehabilitación porque permite cuantificar de manera objetiva y cuantitativa el estado funcional del músculo a lo largo de una sesión terapéutica, algo que la observación clínica subjetiva no puede ofrecer. En este contexto, su aplicación se justifica por varias razones. Primero, permite monitorear la recuperación progresiva de un músculo lesionado: a medida que el tejido se recupera y la capacidad contráctil mejora, el espectro EMG tiende a recuperar su contenido en altas frecuencias, reflejando una mayor velocidad de conducción y reclutamiento de fibras tipo II. Segundo, facilita la detección temprana de compensaciones musculares inadecuadas, ya que cambios en los patrones espectrales de músculos sinérgicos pueden indicar que el paciente está usando grupos musculares incorrectos para completar un movimiento. Tercero, permite establecer criterios objetivos de progresión del tratamiento o de alta terapéutica, basados en métricas espectrales reproducibles y comparables entre sesiones.
  Finalmente, en el contexto de la electromiografía aplicada a prótesis y órtesis, la FFT permite clasificar de forma más precisa los patrones de activación muscular, mejorando el control de dispositivos de asistencia. En síntesis, la transformada de Fourier transforma una señal compleja en información clínicamente interpretable, lo que la convierte en una herramienta de alto valor diagnóstico y terapéutico.

## Referencias

1. Y. Tan, Y. Liu, R. Ye, H. Xu, W. Nie, J. Lu, B. Zhang, C. Wang y B. He,“Change of bio-electric interferential currents of acute fatigue and recovery in male sprinters,” Sports Medicine and Health Science, vol. 2, no. 1, pp. 1–6, 2020. https://doi.org/10.1016/j.smhs.2020.02.004.
2. K. Sahlin, “Metabolic factors in fatigue,” Sports Medicine: An International Journal of Applied Medicine and Science in Sport and Exercise, vol. 13, no. 2, pp. 99–107, 1992. https://doi.org/10.2165/00007256-199213020-00005.
3. D. Constantin-Teodosiu y D. Constantin, “Molecular mechanisms of muscle fatigue,” International Journal of Molecular Sciences, vol. 22, no. 21, art. 11587, 2021. https://doi.org/10.3390/ijms222111587.
4. A. Urdampilleta, I. Armentia, S. Gómez-Zorita, J. M. Martínez-Sanz y J. Mielgo-Ayuso, “La fatiga muscular en los deportistas: Métodos físicos,

