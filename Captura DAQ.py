# -*- coding: utf-8 -*-
"""
=============================================================================
PRÁCTICA DE LABORATORIO – SEÑALES ELECTROMIOGRÁFICAS EMG
Universidad Militar Nueva Granada
Asignatura: Procesamiento Digital de Señales

PARTE A – Captura de señal EMG emulada (generador de señales biológicas)
         + Extensión periódica a duración objetivo
         + Análisis espectral con ventanas superpuestas (superimposed)

El generador produce una señal EMG periódica continua. Se captura un
fragmento con la DAQ y, como la señal es periódica, se repite por software
hasta alcanzar la duración objetivo (52 s). Luego se aplican ventanas
deslizantes con solapamiento del 50% para calcular la frecuencia media
(MNF) y mediana (MDF) a lo largo del tiempo.

PROCEDIMIENTO (guía, Parte A):
  a. Configurar generador en modo EMG (~5 contracciones simuladas)
  b. Adquirir y almacenar la señal con la DAQ
  c. Extender a 52 s por repetición (señal periódica) y segmentar
     con ventanas deslizantes superpuestas (overlap 50%)
  d. Calcular frecuencia media y mediana por ventana (vía Welch)
  e. Presentar resultados en tabla y gráfica de evolución
  f. Analizar cómo varían las frecuencias a lo largo del tiempo

VENTANAS SUPERIMPOSED (ejemplo con ventana=1s, overlap=0.5s):
  V1:  0.0 – 1.0 s
  V2:  0.5 – 1.5 s
  V3:  1.0 – 2.0 s
  ...

REQUISITOS:
  pip install nidaqmx matplotlib numpy scipy
=============================================================================
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch
from datetime import datetime

# =============================================================================
# PARÁMETROS CONFIGURABLES
# =============================================================================
# ── Captura real con DAQ ─────────────────────────────────────────────────────
FS               = 1000      # Frecuencia de muestreo [Hz]
DURACION_CAPTURA = 5         # Duración real de captura del generador [s]
                             # ← Ajustar según lo que dure el ciclo del generador

DISPOSITIVO      = 'Dev5/ai0'  # ← Ajustar según NI MAX
V_MIN            = -5
V_MAX            =  5

# ── Extensión periódica ──────────────────────────────────────────────────────
DURACION_OBJETIVO = 52       # Duración final deseada [s]

# ── Ventanas superpuestas (superimposed) ─────────────────────────────────────
DURACION_VENTANA  = 1.0      # Tamaño de cada ventana [s]
OVERLAP           = 0.5      # Solapamiento entre ventanas [s]
                             # Paso entre ventanas = DURACION_VENTANA - OVERLAP
                             # Ejemplo: ventana=1s, overlap=0.5s → paso=0.5s
                             # → V1: 0.0–1.0, V2: 0.5–1.5, V3: 1.0–2.0 ...

# ── Rango de análisis EMG ────────────────────────────────────────────────────
F_LOW  = 20                  # Hz
F_HIGH = 450                 # Hz

# ── Cálculos derivados ───────────────────────────────────────────────────────
PASO                    = DURACION_VENTANA - OVERLAP
muestras_ventana        = int(FS * DURACION_VENTANA)
muestras_paso           = int(FS * PASO)
total_muestras_captura  = int(FS * DURACION_CAPTURA)
total_muestras_objetivo = int(FS * DURACION_OBJETIVO)
n_ventanas_esperadas    = int((DURACION_OBJETIVO - DURACION_VENTANA) / PASO) + 1

print("=" * 64)
print("  PARTE A – CAPTURA EMG EMULADA CON DAQ")
print("=" * 64)
print(f"  Dispositivo          : {DISPOSITIVO}")
print(f"  Frecuencia           : {FS} Hz")
print(f"  Duración captura     : {DURACION_CAPTURA} s  ({total_muestras_captura} muestras)")
print(f"  Duración objetivo    : {DURACION_OBJETIVO} s  (extensión periódica)")
print(f"  Ventana              : {DURACION_VENTANA} s  |  Overlap: {OVERLAP} s  |  Paso: {PASO} s")
print(f"  Ventanas esperadas   : ~{n_ventanas_esperadas}")
print()

# =============================================================================
# CAPTURA CON LA DAQ
# =============================================================================
print("Iniciando captura del generador...")
try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(
            DISPOSITIVO,
            min_val=V_MIN,
            max_val=V_MAX
        )
        task.timing.cfg_samp_clk_timing(
            FS,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=total_muestras_captura
        )
        senal_capturada = np.array(
            task.read(number_of_samples_per_channel=total_muestras_captura)
        )
    print(f"✓ Captura completada  ({len(senal_capturada)} muestras)")

except Exception as e:
    print(f"\n✗ ERROR en la captura: {e}")
    print("  Verifica conexión DAQ, nombre del dispositivo y drivers (NI MAX).")
    raise

# =============================================================================
# GUARDAR SEÑAL CAPTURADA EN .TXT
# =============================================================================
timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_raw = f"parteA_senal_raw_{timestamp}.txt"
t_raw       = np.arange(len(senal_capturada)) / FS

np.savetxt(
    archivo_raw,
    np.column_stack((t_raw, senal_capturada)),
    fmt='%.6f', delimiter='\t',
    header=(f"Parte A – EMG emulado (crudo) | {timestamp}\n"
            f"Fs={FS} Hz | Duracion={DURACION_CAPTURA} s | Dispositivo={DISPOSITIVO}\n"
            "Tiempo[s]\tAmplitud[V]"),
    comments='# '
)
print(f"✓ Señal cruda guardada en: {archivo_raw}")

# =============================================================================
# EXTENSIÓN PERIÓDICA HASTA DURACION_OBJETIVO
# =============================================================================
repeticiones    = int(np.ceil(total_muestras_objetivo / len(senal_capturada)))
senal_extendida = np.tile(senal_capturada, repeticiones)[:total_muestras_objetivo]
t_ext           = np.arange(len(senal_extendida)) / FS

print(f"\n- Senal extendida:")
print(f"  Fragmento capturado  : {DURACION_CAPTURA} s")
print(f"  Repeticiones         : {repeticiones}")
print(f"  Señal final          : {len(senal_extendida)} muestras  ({DURACION_OBJETIVO} s)")

archivo_ext = f"parteA_senal_extendida_{timestamp}.txt"
np.savetxt(
    archivo_ext,
    np.column_stack((t_ext, senal_extendida)),
    fmt='%.6f', delimiter='\t',
    header=(f"Parte A – EMG emulado extendido | {timestamp}\n"
            f"Fs={FS} Hz | Duracion={DURACION_OBJETIVO} s | "
            f"Repeticiones={repeticiones}\n"
            "Tiempo[s]\tAmplitud[V]"),
    comments='# '
)
print(f"✓ Señal extendida guardada en: {archivo_ext}")

# =============================================================================
# SEGMENTACIÓN CON VENTANAS SUPERPUESTAS (SUPERIMPOSED)
# =============================================================================
inicios   = np.arange(0, len(senal_extendida) - muestras_ventana + 1, muestras_paso)
ventanas  = [senal_extendida[i: i + muestras_ventana] for i in inicios]
t_centros = (inicios + muestras_ventana / 2) / FS   # tiempo central de cada ventana
n_ventanas = len(ventanas)

print(f"\n✓ Ventanas superpuestas generadas: {n_ventanas}")
print(f"  (ventana={DURACION_VENTANA}s, overlap={OVERLAP}s, paso={PASO}s)")

# =============================================================================
# FUNCIÓN: MNF Y MDF VÍA PSD (Welch)
# =============================================================================
def frecuencia_media_mediana(segmento, fs, f_low, f_high):
    """
    MNF = Σ(f · PSD) / Σ(PSD)          → centroide espectral
    MDF = f donde área acumulada = 50%  → percentil 50 del espectro
    Calculados sobre el rango f_low–f_high Hz (banda EMG útil).
    """
    freqs, psd = welch(segmento, fs=fs, nperseg=min(512, len(segmento)))

    idx = (freqs >= f_low) & (freqs <= f_high)
    f_u = freqs[idx]
    p_u = psd[idx]

    area_total = np.trapz(p_u, f_u)
    mnf = np.trapz(f_u * p_u, f_u) / area_total if area_total > 0 else 0

    area_acum = np.cumsum(p_u * np.gradient(f_u))
    idx_mdf   = np.searchsorted(area_acum, area_acum[-1] / 2)
    mdf       = f_u[min(idx_mdf, len(f_u) - 1)]

    return mnf, mdf, freqs, psd

# =============================================================================
# ANÁLISIS POR VENTANA
# =============================================================================
resultados_mnf = []
resultados_mdf = []
espectros      = []

print("\n" + "=" * 68)
print(f"  {'V':^5} {'t_ini':^8} {'t_fin':^8} {'t_centro':^10} {'MNF (Hz)':^13} {'MDF (Hz)':^13}")
print("-" * 68)

for i, (ventana, inicio) in enumerate(zip(ventanas, inicios)):
    t_ini = inicio / FS
    t_fin = t_ini + DURACION_VENTANA
    t_cen = t_ini + DURACION_VENTANA / 2

    mnf, mdf, freqs, psd = frecuencia_media_mediana(ventana, FS, F_LOW, F_HIGH)
    resultados_mnf.append(mnf)
    resultados_mdf.append(mdf)
    espectros.append((freqs, psd))

    # Imprimir solo cada 5 ventanas para no saturar consola
    if i % 5 == 0 or i == n_ventanas - 1:
        print(f"  {i+1:^5} {t_ini:^8.2f} {t_fin:^8.2f} {t_cen:^10.2f} "
              f"{mnf:^13.2f} {mdf:^13.2f}")

print("=" * 68)
print(f"  (Se muestran cada 5 ventanas. Total: {n_ventanas} ventanas)")

resultados_mnf = np.array(resultados_mnf)
resultados_mdf = np.array(resultados_mdf)
x_ventanas     = np.arange(1, n_ventanas + 1)
z_mnf          = np.polyfit(x_ventanas, resultados_mnf, 1)
z_mdf          = np.polyfit(x_ventanas, resultados_mdf, 1)

# =============================================================================
# GRÁFICA 1 – Fragmento capturado vs señal extendida
# =============================================================================
fig1, axes = plt.subplots(2, 1, figsize=(14, 7))
fig1.suptitle("Parte A – Señal EMG emulada | Captura y extensión periódica",
              fontsize=13, fontweight='bold')

axes[0].plot(t_raw, senal_capturada, color='#C62828', lw=0.9,
             label=f'Fragmento capturado ({DURACION_CAPTURA} s)')
axes[0].set_ylabel("Amplitud (V)", fontsize=10)
axes[0].set_xlabel("Tiempo (s)", fontsize=10)
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

axes[1].plot(t_ext, senal_extendida, color='#455A64', lw=0.4,
             label=f'Señal extendida ({DURACION_OBJETIVO} s, ×{repeticiones})')
# Marcar las uniones entre repeticiones
for r in range(1, repeticiones):
    axes[1].axvline(r * DURACION_CAPTURA, color='#C62828',
                    lw=0.8, ls='--', alpha=0.5)
axes[1].set_ylabel("Amplitud (V)", fontsize=10)
axes[1].set_xlabel("Tiempo (s)", fontsize=10)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"parteA_captura_vs_extendida_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 2 – Señal extendida con ventanas superpuestas (zoom primeros 5 s)
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 5))
fig2.suptitle("Parte A – Ventanas superpuestas (superimposed) | Zoom primeros 5 s",
              fontsize=13, fontweight='bold')

zoom = 5   # segundos a mostrar para que se vea el solapamiento
mask = t_ext <= zoom
ax2.plot(t_ext[mask], senal_extendida[mask], color='#455A64', lw=0.8,
         label='EMG emulado extendido')

# Dibujar solo las ventanas dentro del zoom
colores_v = plt.cm.tab10(np.linspace(0, 0.9, 10))
for i, inicio in enumerate(inicios):
    t_ini_v = inicio / FS
    t_fin_v = t_ini_v + DURACION_VENTANA
    if t_ini_v > zoom:
        break
    ax2.axvspan(t_ini_v, min(t_fin_v, zoom),
                alpha=0.18, color=colores_v[i % 10])
    ax2.axvline(t_ini_v, color=colores_v[i % 10], lw=0.8, ls='--', alpha=0.6)

ax2.set_xlabel("Tiempo (s)", fontsize=11)
ax2.set_ylabel("Amplitud (V)", fontsize=11)
ax2.set_xlim(0, zoom)
ax2.set_title(f"Ventana={DURACION_VENTANA}s | Overlap={OVERLAP}s | "
              f"Paso={PASO}s  →  Total {n_ventanas} ventanas en {DURACION_OBJETIVO}s",
              fontsize=10)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteA_ventanas_superimposed_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 3 – Evolución de MNF y MDF (eje X en segundos)
# =============================================================================
fig3, ax3 = plt.subplots(figsize=(13, 5))
fig3.suptitle("Parte A – Evolución de MNF y MDF | Ventanas superpuestas",
              fontsize=13, fontweight='bold')

ax3.plot(t_centros, resultados_mnf, '-', color='#1565C0', lw=1.5,
         label='Frecuencia media (MNF)')
ax3.plot(t_centros, resultados_mdf, '--', color='#C62828', lw=1.5,
         label='Frecuencia mediana (MDF)')

# Tendencia lineal
t_trend = np.array([t_centros[0], t_centros[-1]])
ax3.plot(t_trend,
         np.poly1d(np.polyfit(t_centros, resultados_mnf, 1))(t_trend),
         ':', color='#1565C0', lw=2, alpha=0.6,
         label=f'Tendencia MNF ({z_mnf[0]:+.4f} Hz/ventana)')
ax3.plot(t_trend,
         np.poly1d(np.polyfit(t_centros, resultados_mdf, 1))(t_trend),
         ':', color='#C62828', lw=2, alpha=0.6,
         label=f'Tendencia MDF ({z_mdf[0]:+.4f} Hz/ventana)')

ax3.set_xlabel("Tiempo (s)", fontsize=11)
ax3.set_ylabel("Frecuencia (Hz)", fontsize=11)
ax3.set_xlim(t_centros[0], t_centros[-1])
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteA_evolucion_frecuencias_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 4 – Comparación espectral: primeras 3 vs últimas 3 ventanas
# =============================================================================
fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
fig4.suptitle("Parte A – Comparación espectral: primeras vs últimas ventanas",
              fontsize=13, fontweight='bold')

for label, indices, ax in [
    ("Primeras 3 ventanas", [0, 1, 2],                      axes4[0]),
    ("Últimas 3 ventanas",  [-3, -2, -1],                   axes4[1])
]:
    for j, vi in enumerate(indices):
        freqs, psd = espectros[vi]
        psd_norm   = psd / psd.max() if psd.max() > 0 else psd
        num_v      = vi + 1 if vi >= 0 else n_ventanas + vi + 1
        ax.plot(freqs, psd_norm, lw=1.5,
                label=f'V{num_v}  MNF={resultados_mnf[vi]:.1f} Hz')
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("Frecuencia (Hz)", fontsize=10)
    ax.set_ylabel("PSD normalizada", fontsize=10)
    ax.set_xlim(0, 500)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"parteA_espectros_comparacion_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# RESUMEN FINAL EN CONSOLA
# =============================================================================
print("\n  RESUMEN – PARTE A")
print("  " + "-" * 52)
print(f"  Fragmento capturado   : {DURACION_CAPTURA} s  ({FS} Hz)")
print(f"  Señal extendida       : {DURACION_OBJETIVO} s  (×{repeticiones} repeticiones)")
print(f"  Ventanas superpuestas : {n_ventanas}  "
      f"(ventana={DURACION_VENTANA}s, overlap={OVERLAP}s)")
print(f"  MNF promedio          : {resultados_mnf.mean():.2f} Hz")
print(f"  MDF promedio          : {resultados_mdf.mean():.2f} Hz")
print(f"  Pendiente MNF         : {z_mnf[0]:+.4f} Hz/ventana")
print(f"  Pendiente MDF         : {z_mdf[0]:+.4f} Hz/ventana")

if abs(z_mnf[0]) < 0.5:
    tend = "PLANA → esperado para señal periódica idéntica"
elif z_mnf[0] < 0:
    tend = "DESCENDENTE ↓"
else:
    tend = "ASCENDENTE ↑"

print(f"  Tendencia MNF         : {tend}")
print("\n✓ Parte A completada. Gráficas guardadas.")