# Guia-N-4-Senales-electromiograficas-EMG

## PARTE A

Debido a las limitaciones del generador de señales, no fue posible configurar directamente una señal de tipo EMG que representara ciclos alternados de contracción y relajación (contracción–relajación–contracción–relajación).

Ante esta restricción, se plantearon dos estrategias para la obtención de la señal deseada. La primera consistía en registrar múltiples eventos de contracción por separado y posteriormente concatenarlos para formar una señal compuesta. La segunda alternativa consistía en adquirir una contracción muscular sostenida y, a partir de esta, segmentar la señal mediante el uso de ventanas temporales.

Finalmente, se optó por la segunda metodología, ya que permite un mejor control sobre el procesamiento y análisis de la señal, además de facilitar la aplicación de técnicas de segmentación en el dominio del tiempo.

Adicionalmente, con el fin de evitar la saturación del programa y del compilador durante el procesamiento, se tomó un fragmento representativo de la señal en un intervalo de tiempo determinado y se replicó sucesivamente hasta completar una duración total de 52 s.


## PARTE B

## PARTE C
