# -*- coding: utf-8 -*-
"""
=============================================================================
PRÁCTICA DE LABORATORIO – SEÑALES ELECTROMIOGRÁFICAS EMG
Universidad Militar Nueva Granada
Asignatura: Procesamiento Digital de Señales

PARTE B – Lectura de señal EMG real (BITalino .txt)
         + Filtrado pasa banda 20–450 Hz
         + Ventanas superpuestas (superimposed)
         + Análisis espectral: MNF y MDF por ventana

PROCEDIMIENTO (guía, Parte B):
  a. Colocar electrodos sobre grupo muscular (antebrazo o bíceps)
  b. Registrar EMG durante contracción sostenida hasta fatiga
  c. Aplicar filtro pasa banda 20–450 Hz
  d. Segmentar con ventanas superpuestas (overlap 50%)
  e. Calcular MNF y MDF por ventana
  f. Graficar tendencia y analizar relación con fatiga muscular
  g. Discutir cambios de frecuencia y fisiología de la fatiga

FORMATO .TXT BITALINO (OpenSignals):
  Cabecera con #, columnas: nSeq | I1 | I2 | O1 | O2 | A1
  Canal EMG en ADC 10 bits (0–1023) → se convierte a mV

REQUISITOS:
  pip install matplotlib numpy scipy
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch
from datetime import datetime
import os

# =============================================================================
# PARÁMETROS CONFIGURABLES
# =============================================================================
ARCHIVO_TXT      = "señaljohanEMG.txt"  # ← Nombre del archivo BITalino
COLUMNA_EMG      = 5    # 2=A1, 3=A2... (última columna del OpenSignals)

FS               = 1000  # Frecuencia de muestreo [Hz]

# ── Filtro pasa banda ────────────────────────────────────────────────────────
F_LOW            = 20    # Hz
F_HIGH           = 450   # Hz
ORDEN_FILTRO     = 4

# ── Ventanas superpuestas ────────────────────────────────────────────────────
DURACION_VENTANA = 1.0   # Tamaño de ventana [s]
OVERLAP          = 0.5   # Solapamiento [s]  → paso = 0.5 s
                         # V1: 0.0–1.0s, V2: 0.5–1.5s, V3: 1.0–2.0s ...

# ── Suavizado de MNF/MDF ─────────────────────────────────────────────────────
VENTANA_SUAVIZADO = 10   # Número de ventanas para media móvil
                         # Aumentar para curva más suave, disminuir para más detalle

# =============================================================================
# LECTURA DEL ARCHIVO .TXT DE BITALINO
# =============================================================================
print("=" * 62)
print("  PARTE B – ANÁLISIS EMG REAL (BITALINO .TXT)")
print("=" * 62)

if not os.path.exists(ARCHIVO_TXT):
    raise FileNotFoundError(
        f"No se encontró '{ARCHIVO_TXT}'.\n"
        f"Asegúrate de que esté en la misma carpeta que este script."
    )

# Lectura manual: ignora cabecera (#), tab extra al final y retorno CRLF
filas = []
with open(ARCHIVO_TXT, 'r') as f:
    for linea in f:
        linea = linea.strip()
        if linea.startswith('#') or linea == '':
            continue
        cols = [c for c in linea.split('\t') if c.strip() != '']
        if len(cols) >= COLUMNA_EMG + 1:
            filas.append([float(c) for c in cols[:COLUMNA_EMG + 1]])

datos     = np.array(filas)
senal_adc = datos[:, COLUMNA_EMG]

# Conversión ADC → mV (fórmula oficial BITalino EMG)
senal_mv  = ((senal_adc / 1024.0) - 0.5) * (3.3 / 1.009) * 1000.0
t         = np.arange(len(senal_mv)) / FS
duracion  = len(senal_mv) / FS
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print(f"  Archivo          : {ARCHIVO_TXT}")
print(f"  Muestras         : {len(senal_mv)}  ({duracion:.2f} s a {FS} Hz)")
print(f"  Rango ADC        : {senal_adc.min():.0f} – {senal_adc.max():.0f}")
print(f"  Rango mV         : {senal_mv.min():.2f} – {senal_mv.max():.2f} mV")

# =============================================================================
# FILTRO PASA BANDA 20–450 Hz (Butterworth, fase cero)
# =============================================================================
nyquist  = FS / 2.0
b, a     = butter(ORDEN_FILTRO, [F_LOW/nyquist, F_HIGH/nyquist], btype='bandpass')
senal_f  = filtfilt(b, a, senal_mv)
print(f"\n✓ Filtro pasa banda aplicado: {F_LOW}–{F_HIGH} Hz")

# =============================================================================
# VENTANAS SUPERPUESTAS (SUPERIMPOSED)
# =============================================================================
muestras_ventana = int(FS * DURACION_VENTANA)
muestras_paso    = int(FS * (DURACION_VENTANA - OVERLAP))
inicios          = np.arange(0, len(senal_f) - muestras_ventana + 1, muestras_paso)
ventanas         = [senal_f[i: i + muestras_ventana] for i in inicios]
t_centros        = (inicios + muestras_ventana / 2) / FS
n_ventanas       = len(ventanas)

print(f"✓ Ventanas superpuestas: {n_ventanas}")
print(f"  (ventana={DURACION_VENTANA}s, overlap={OVERLAP}s, paso={DURACION_VENTANA-OVERLAP}s)")

# =============================================================================
# FUNCIÓN: MNF Y MDF VÍA PSD (Welch)
# =============================================================================
trapz = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz

def mnf_mdf(seg, fs, f_low, f_high):
    """
    MNF = Σ(f · PSD) / Σ(PSD)          → centroide espectral
    MDF = f donde área acumulada = 50%  → percentil 50 del espectro
    """
    freqs, psd = welch(seg, fs=fs, nperseg=min(512, len(seg)))
    idx  = (freqs >= f_low) & (freqs <= f_high)
    f_u, p_u = freqs[idx], psd[idx]
    area = trapz(p_u, f_u)
    mnf  = trapz(f_u * p_u, f_u) / area if area > 0 else 0
    acum = np.cumsum(p_u * np.gradient(f_u))
    mdf  = f_u[min(np.searchsorted(acum, acum[-1] / 2), len(f_u) - 1)]
    return mnf, mdf, freqs, psd

# =============================================================================
# ANÁLISIS POR VENTANA
# =============================================================================
resultados_mnf, resultados_mdf, espectros = [], [], []

print("\n" + "=" * 68)
print(f"  {'V':^5} {'t_ini':^8} {'t_fin':^8} {'t_centro':^10} {'MNF (Hz)':^13} {'MDF (Hz)':^13}")
print("-" * 68)

for i, (ventana, inicio) in enumerate(zip(ventanas, inicios)):
    t_ini = inicio / FS
    t_fin = t_ini + DURACION_VENTANA
    t_cen = t_ini + DURACION_VENTANA / 2

    mnf, mdf, freqs, psd = mnf_mdf(ventana, FS, F_LOW, F_HIGH)
    resultados_mnf.append(mnf)
    resultados_mdf.append(mdf)
    espectros.append((freqs, psd))

    if i % 5 == 0 or i == n_ventanas - 1:
        print(f"  {i+1:^5} {t_ini:^8.2f} {t_fin:^8.2f} {t_cen:^10.2f} "
              f"{mnf:^13.2f} {mdf:^13.2f}")

print("=" * 68)
print(f"  (Tabla muestra cada 5 ventanas. Total calculadas: {n_ventanas})")

resultados_mnf = np.array(resultados_mnf)
resultados_mdf = np.array(resultados_mdf)

# =============================================================================
# SUAVIZADO POR MEDIA MÓVIL
# =============================================================================
def media_movil(x, n):
    kernel = np.ones(n) / n
    return np.convolve(x, kernel, mode='same')

mnf_suav = media_movil(resultados_mnf, VENTANA_SUAVIZADO)
mdf_suav = media_movil(resultados_mdf, VENTANA_SUAVIZADO)

# Tendencia lineal (sobre datos suavizados)
z_mnf = np.polyfit(t_centros, mnf_suav, 1)
z_mdf = np.polyfit(t_centros, mdf_suav, 1)

print(f"\n  MNF promedio  : {resultados_mnf.mean():.2f} Hz")
print(f"  MDF promedio  : {resultados_mdf.mean():.2f} Hz")
print(f"  Pendiente MNF : {z_mnf[0]:+.4f} Hz/s  → "
      + ("DESCENDENTE ↓ (fatiga detectada)" if z_mnf[0] < 0 else "ASCENDENTE ↑"))
print(f"  Pendiente MDF : {z_mdf[0]:+.4f} Hz/s  → "
      + ("DESCENDENTE ↓ (fatiga detectada)" if z_mdf[0] < 0 else "ASCENDENTE ↑"))

# =============================================================================
# GRÁFICA 1 – Señal cruda vs filtrada
# =============================================================================
colores_v = plt.cm.tab10(np.linspace(0, 0.9, 10))

fig1, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True)
fig1.suptitle("Parte B – Señal EMG real | Cruda vs Filtrada (20–450 Hz)",
              fontsize=13, fontweight='bold')
axes[0].plot(t, senal_mv, color='#90A4AE', lw=0.5, label='Señal cruda (ADC→mV)')
axes[0].set_ylabel("Amplitud (mV)", fontsize=10)
axes[0].legend(fontsize=9); axes[0].grid(True, alpha=0.3)
axes[1].plot(t, senal_f, color='#1565C0', lw=0.5, label='Señal filtrada (20–450 Hz)')
axes[1].set_ylabel("Amplitud (mV)", fontsize=10)
axes[1].set_xlabel("Tiempo (s)", fontsize=11)
axes[1].legend(fontsize=9); axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteB_1_cruda_vs_filtrada_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 2 – Zoom ventanas superpuestas (primeros 5 s)
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(14, 5))
fig2.suptitle("Parte B – Ventanas superpuestas (superimposed) | Zoom primeros 5 s",
              fontsize=13, fontweight='bold')
zoom = 5
ax2.plot(t[t <= zoom], senal_f[t <= zoom], color='#1565C0', lw=0.8, label='EMG filtrado')
for i, inicio in enumerate(inicios):
    t_i = inicio / FS
    if t_i > zoom: break
    ax2.axvspan(t_i, min(t_i + DURACION_VENTANA, zoom),
                alpha=0.18, color=colores_v[i % 10])
    ax2.axvline(t_i, color=colores_v[i % 10], lw=0.8, ls='--', alpha=0.6)
ax2.set_xlabel("Tiempo (s)", fontsize=11)
ax2.set_ylabel("Amplitud (mV)", fontsize=11)
ax2.set_xlim(0, zoom)
ax2.set_title(f"Ventana={DURACION_VENTANA}s | Overlap={OVERLAP}s | "
              f"Paso={DURACION_VENTANA-OVERLAP}s → {n_ventanas} ventanas totales",
              fontsize=10)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteB_2_ventanas_superimposed_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 3 – Evolución MNF y MDF (cruda + suavizada + tendencia)
# =============================================================================
fig3, ax3 = plt.subplots(figsize=(13, 5))
fig3.suptitle("Parte B – Evolución de MNF y MDF | Tendencia de fatiga muscular",
              fontsize=13, fontweight='bold')

# Datos crudos (transparentes de fondo)
ax3.plot(t_centros, resultados_mnf, '-', color='#1565C0', lw=0.8, alpha=0.3)
ax3.plot(t_centros, resultados_mdf, '-', color='#C62828', lw=0.8, alpha=0.3)

# Suavizados
ax3.plot(t_centros, mnf_suav, '-', color='#1565C0', lw=2.0,
         label=f'MNF suavizada (media móvil {VENTANA_SUAVIZADO} ventanas)')
ax3.plot(t_centros, mdf_suav, '-', color='#C62828', lw=2.0,
         label=f'MDF suavizada (media móvil {VENTANA_SUAVIZADO} ventanas)')

# Tendencia lineal
t_trend = np.array([t_centros[0], t_centros[-1]])
ax3.plot(t_trend, np.poly1d(z_mnf)(t_trend), ':', color='#1565C0', lw=2.5, alpha=0.8,
         label=f'Tendencia MNF ({z_mnf[0]:+.3f} Hz/s)')
ax3.plot(t_trend, np.poly1d(z_mdf)(t_trend), ':', color='#C62828', lw=2.5, alpha=0.8,
         label=f'Tendencia MDF ({z_mdf[0]:+.3f} Hz/s)')

ax3.set_xlabel("Tiempo (s)", fontsize=11)
ax3.set_ylabel("Frecuencia (Hz)", fontsize=11)
ax3.set_xlim(t_centros[0], t_centros[-1])
ax3.legend(fontsize=9); ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteB_3_evolucion_frecuencias_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# GRÁFICA 4 – Comparación espectral primeras vs últimas ventanas
# =============================================================================
fig4, axes4 = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
fig4.suptitle("Parte B – Comparación espectral: primeras vs últimas ventanas",
              fontsize=13, fontweight='bold')
for label, indices, ax in [
    ("Primeras 3 ventanas", [0, 1, 2],    axes4[0]),
    ("Últimas 3 ventanas",  [-3, -2, -1], axes4[1])
]:
    for vi in indices:
        freqs, psd = espectros[vi]
        psd_norm = psd / psd.max() if psd.max() > 0 else psd
        num_v = vi + 1 if vi >= 0 else n_ventanas + vi + 1
        ax.plot(freqs, psd_norm, lw=1.5,
                label=f'V{num_v}  MNF={resultados_mnf[vi]:.1f} Hz')
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("Frecuencia (Hz)", fontsize=10)
    ax.set_ylabel("PSD normalizada", fontsize=10)
    ax.set_xlim(0, 500); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"parteB_4_espectros_comparacion_{timestamp}.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n✓ Parte B completada. Todas las gráficas guardadas.")