# Animación de Fondo con Scroll, Oscilación y Sprites usando Multiprocesamiento en Python

Trabajo final del curso **Algoritmos Paralelos**  
Universidad Nacional de Moquegua - Escuela Profesional de Ingeniería de Sistemas e Informática  
Autor: Jesús Ronald Rosales Roca  
Docente: Honorio Apaza Alanoca  
📅 Fecha: 26 de julio de 2025  

---

## Descripción del Proyecto

Este proyecto implementa una animación 2D basada en imágenes RGB, donde un sprite se desplaza sobre un fondo aplicando efectos visuales como scroll, oscilación y ciclo de paleta. La novedad principal radica en el uso de **multiprocesamiento en Python** para mejorar el rendimiento y la escalabilidad del renderizado.

Inspirado en sistemas de videojuegos clásicos (como el SNES), se replican efectos de animación típicos de consolas de 16 bits pero utilizando herramientas modernas como Python, OpenCV y NumPy.

---

## Objetivos

### Objetivo General
Aplicar los conocimientos del curso para representar una animación 2D de un kernel (sprite) sobre una imagen RGB con efectos visuales, paralelizando el procesamiento usando Python.

### Objetivos Específicos
- Realizar procesamiento de imágenes a nivel de píxeles con librerías como OpenCV o Pillow.
- Simular el movimiento y convolución de un kernel sobre una imagen base.
- Optimizar el código con paralelismo usando `multiprocessing`.

---

## Marco Teórico

- **Algoritmos paralelos:** División de tareas en hilos/procesos concurrentes.
- **Librerías en Python:** uso de `multiprocessing`, `opencv`, `numpy`, `matplotlib`.
- **Procesamiento de imágenes:** representaciones matriciales, kernels, convolución, oscilación y scroll.
- **Renderizado clásico:** se replican técnicas visuales de consolas de 16 bits como el SNES (tiles, VBlank, palette cycling).

---

## Herramientas Utilizadas

- **Lenguaje:** Python 3.13+
- **IDE:** Visual Studio Code
- **Sistema Operativo:** Windows 10
- **Procesador:** Intel Core i7-10700F (16 núcleos)
- **Librerías:**
  - `numpy`
  - `opencv-python`
  - `matplotlib`
  - `multiprocessing`
  - `time`

---

## Efectos Implementados

- **Scroll:** desplazamiento horizontal o vertical del fondo.
- **Oscilación:** efecto senoidal en píxeles (modo agua, calor).
- **Ciclo de paleta:** animación de colores sin cambiar píxeles.
- **Sprite animado:** rebote del sprite sobre el fondo usando máscaras.

---

## Resultados

| Intento | Secuencial (s) | Paralelo (s) |
|---------|----------------|--------------|
| 1       | 4.71           | 4.81         |
| 2       | 4.54           | 4.81         |
| ...     | ...            | ...          |
| 10      | 4.60           | 4.77         |

> *Conclusión:* el paralelismo mejora la eficiencia cuando se evitan estructuras como `Queue` entre procesos. La división por bloques sin comunicación es más escalable.

---

## Conclusiones

- Python permite construir animaciones visuales interactivas con buen rendimiento.
- La paralelización por bloques es efectiva si se evita el uso intensivo de colas.
- La combinación de procesamiento matricial + animación visual + multiproceso representa una herramienta educativa y técnica poderosa.

---

## Recomendaciones

- Evitar `Queue` en ambientes altamente paralelizados.
- Realizar pruebas desactivando la visualización para evaluar solo el rendimiento computacional.
- Explorar `concurrent.futures` o `multiprocessing.Pool` para una mejor administración.

---


## Recursos y Referencias

- [NumPy Documentation](https://numpy.org/doc/2.3/)
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [Matplotlib Cheatsheets](https://matplotlib.org/cheatsheets/)
- [GitHub del proyecto](https://github.com/JesvsRRR/Animaci-n-de-Fondo-con-Scroll-Oscilaci-n-y-Sprites-Usando-Multiprocesamiento-en-Python)

---


