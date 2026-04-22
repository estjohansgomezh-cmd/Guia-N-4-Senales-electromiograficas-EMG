# Guia-N-4-Senales-electromiograficas-EMG

## PARTE A

Debido a las limitaciones del generador de señales, no fue posible configurar directamente una señal de tipo EMG que representara ciclos alternados de contracción y relajación (contracción–relajación–contracción–relajación).

Ante esta restricción, se plantearon dos estrategias para la obtención de la señal deseada. La primera consistía en registrar múltiples eventos de contracción por separado y posteriormente concatenarlos para formar una señal compuesta. La segunda alternativa consistía en adquirir una contracción muscular sostenida y, a partir de esta, segmentar la señal mediante el uso de ventanas temporales.

Finalmente, se optó por la segunda metodología, ya que permite un mejor control sobre el procesamiento y análisis de la señal, además de facilitar la aplicación de técnicas de segmentación en el dominio del tiempo.

Adicionalmente, con el fin de evitar la saturación del programa y del compilador durante el procesamiento, se tomó un fragmento representativo de la señal en un intervalo de tiempo determinado y se replicó sucesivamente hasta completar una duración total de 52 s.

<img width="2085" height="1036" alt="parteA_captura_vs_extendida_20260422_151228" src="https://github.com/user-attachments/assets/ada7d704-c26e-4c41-9a4f-6816911ab1f1" />

Para la Parte A, se empleó una ventana temporal de 1 s con un solapamiento (overlap) del 50 %. Considerando una frecuencia de muestreo de 1000 Hz, cada ventana corresponde a 1000 muestras. Esta elección permite capturar adecuadamente la dinámica de la señal EMG, mientras que el solapamiento garantiza continuidad entre segmentos y reduce la pérdida de información en los bordes de cada ventana.

Para efectos de visualización, en la figura presentada se muestran únicamente los primeros 5 s de la señal. No obstante, el análisis se realizó considerando la totalidad de las ventanas obtenidas (103 en total).

<img width="2087" height="744" alt="parteA_ventanas_superimposed_20260422_151228" src="https://github.com/user-attachments/assets/a1e60d44-4542-459c-8909-3adf3fcbac7c" />

<img width="1937" height="744" alt="parteA_evolucion_frecuencias_20260422_151228" src="https://github.com/user-attachments/assets/e0b1747c-9936-4f9f-b656-696f97c235a4" />
<img width="1935" height="742" alt="parteA_espectros_comparacion_20260422_151228" src="https://github.com/user-attachments/assets/86d392ed-7db0-46dd-a114-eadbc500af1a" />


## PARTE B

## PARTE C
