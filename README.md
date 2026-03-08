# Snake AI: Q-Learning Agent

**An autonomous Snake agent trained via tabular Q-Learning and reinforcement learning to master optimal gameplay strategies.**

Este proyecto implementa un agente de **Aprendizaje por Refuerzo** que aprende a jugar al clásico *Snake* desde cero. El agente evoluciona de movimientos aleatorios a una estrategia óptima en cuestión de minutos.



## Características Técnicas

* **Cerebro:** Algoritmo de **Q-Learning Tabular** (Ecuación de Bellman).
* **Entrada (Estado):** Vector de **11 bits** que detecta peligro inmediato, dirección actual y posición relativa de la comida.
* **Exploración:** Estrategia **$\epsilon$-greedy** con decaimiento dinámico para balancear el descubrimiento y la explotación.
* **Interfaz:** Desarrollado con **PyGame** con soporte para cambio de velocidad en tiempo real.



## Instalación y Uso

1. **Clonar el repositorio y preparar el entorno:**
   ```bash
   # Crear entorno virtual
   python3 -m venv .venv
   # Activar entorno
   source .venv/bin/activate
   # Instalar dependencias
   pip install -r requirements.txt
