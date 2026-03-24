# Deduplicación de Clientes: Consolidación de Registros desde Múltiples Fuentes

Proyecto de análisis de datos que determina la cantidad de clientes únicos de una empresa, unificando y deduplicando registros provenientes de tres fuentes independientes mediante técnicas de record linkage.

## Problema

La empresa almacena datos de clientes en tres sistemas separados — un CRM, una base de datos de e-commerce y un registro de transacciones de ventas — sin ninguna clave compartida entre ellos. Un mismo cliente puede aparecer en los tres sistemas con ligeras variaciones en el nombre, la edad o el código postal. El objetivo es obtener un conteo confiable de clientes únicos sin necesidad de cruzar los datos manualmente.

## Fuentes de Datos

| Archivo | Descripción | Registros |
|---|---|---|
| `purchases.csv` | Transacciones de ventas. Contiene `customer_id` para clientes registrados y campos de invitado (`guest_first_name`, `guest_surname`, `guest_postcode`) para compras realizadas sin cuenta. | ~71 500 |
| `crm_export.csv` | Exportación del sistema CRM. Contiene nombre, apellido, edad y código postal de cada cliente. | ~7 800 |
| `customer_database.csv` | Base de datos de e-commerce. Misma estructura que el CRM, pero con una población de clientes considerablemente mayor. | ~23 500 |

> Los archivos de datos no están incluidos en este repositorio.

## Metodología

El pipeline de deduplicación utiliza la librería [`recordlinkage`](https://recordlinkage.readthedocs.io/) de Python y se desarrolla en dos etapas:

**1. Deduplicación interna (por fuente)**
- Eliminación de duplicados exactos con `drop_duplicates()`
- Detección de duplicados difusos mediante:
  - Codificación fonética Soundex para normalizar nombres
  - Blocking por iniciales para reducir el espacio de comparación
  - Similitud Jaro-Winkler para nombre y apellido
  - Distancia Levenshtein para código postal
  - Comparación exacta en edad
  - Clasificación por umbrales manuales

**2. Emparejamiento cruzado (e-commerce vs. CRM)**
- Mismas características de indexación y comparación
- **ECMClassifier** (Expectation-Maximization no supervisado) para clasificación probabilística
- Validación manual exhaustiva par a par de todas las combinaciones de atributos discrepantes
- Resolución de conflictos uno-a-muchos

## Resultados

| Categoría | Cantidad |
|---|---|
| Clientes registrados (e-commerce + CRM combinados) | 20754 |
| Clientes de sistema externo | 1248 |
| Invitados únicos (sin cuenta) | 8300 |
| **Total de clientes únicos** | **30302** |

De los 20 754 clientes registrados, 5 938 aparecían tanto en la base de datos de e-commerce como en el CRM.

## Limitaciones Conocidas

- **No se realizó matching invitado-cliente.** Algunos de los 8 300 invitados podrían ser clientes registrados que compraron sin iniciar sesión. El conteo final podría estar ligeramente sobreestimado.
- **Clave de bloqueo única.** Solo se utilizan las iniciales para el blocking, lo que podría perder coincidencias donde la primera letra del nombre contiene un error tipográfico.
- **Umbral conservador en edad.** La edad se compara con coincidencia exacta; no se toleran diferencias de ±1 año.
- **IDs de sistema externo sin datos demográficos.** Los 1 248 clientes de otro sistema solo cuentan con su `customer_id`, por lo que no es posible validar si alguno duplica a un cliente ya registrado.

## Estructura del Repositorio

```
DataModeling-Duplicates/
├── data_modeling.ipynb      # Notebook principal de análisis
├── helper_functions.py      # Funciones utilitarias compartidas
└── LinkageTutorial/
    └── linkage_tutorial.ipynb   # Notebook educativo usando el dataset FEBRL4
```

## Requisitos

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- recordlinkage

Instalación de dependencias:

## Cómo Ejecutar

1. Colocar los archivos de datos (`purchases.csv`, `crm_export.csv`, `customer_database.csv`) en un directorio `data/` dentro de `DataModeling/`.
2. Abrir `data_modeling.ipynb` en Jupyter o VSCode.
3. Ejecutar todas las celdas en orden.
