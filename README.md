# Práctica de Laboratorio N° 4: Señales Electromiográficas EMG
Universidad Militar Nueva Granada — Ingeniería Biomédica — Procesamiento Digital de Señales
---
## Descripción

En este repositorio se presenta el informe y los resultados de la Práctica de Laboratorio #4 de Señales electromiográficas EMG.


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


<img width="1937" height="744" alt="parteC_3_pico_espectral_20260422_190847" src="https://github.com/user-attachments/assets/8f907a59-e361-4ace-bab8-e866cb1be241" />
<img width="1904" height="891" alt="parteC_2_espectrograma_20260422_190847" src="https://github.com/user-attachments/assets/95f16758-6095-4b85-b5e4-183a119f9f81" />
<img width="2085" height="742" alt="parteC_1_fft_primeras_vs_ultimas_20260422_190847" src="https://github.com/user-attachments/assets/1e7a5e34-7dd3-4212-be0c-3943da3ad64a" />
<img width="1637" height="744" alt="parteC_4_espectro_promedio_20260422_190847" src="https://github.com/user-attachments/assets/85f1813f-dc13-4c68-876e-5ad0d687633d" />



