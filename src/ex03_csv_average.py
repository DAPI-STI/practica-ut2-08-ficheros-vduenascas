"""
EX03 (CSV) · Calcular la media de una columna

Objetivo:
- Leer un CSV con cabecera (primera línea).
- Usar la librería estándar `csv` (recomendado: csv.DictReader).
- Convertir datos a float y calcular una media.

Ejemplo típico:
- Un CSV de calificaciones con columnas: name, average
"""

from __future__ import annotations
from pathlib import Path
import csv

def csv_average(path: str | Path, column: str) -> float:
    """
    Calcula y devuelve la media de la columna numérica `column` en el CSV `path`.

    Reglas:
    - El CSV tiene cabecera.
    - `column` debe existir en la cabecera. Si no, ValueError.
    - Todos los valores de esa columna deben poder convertirse a float. Si no, ValueError.
    - Si no hay filas de datos (CSV vacío tras la cabecera), ValueError.
    - Si el fichero no existe, FileNotFoundError.

    Ejemplo:
    name,average
    Ana,10
    Luis,6

    csv_average(..., "average") -> 8.0
    """
    path_str = str(path)
    
    try:
        with open(path_str, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            if column not in lector.fieldnames:
                raise ValueError(f"Columna '{column}' no encontrada en el CSV")
            
            valores = []
            
            for fila in lector:
                valor_str = fila[column].strip()
                
                try:
                    valor = float(valor_str)
                    valores.append(valor)
                except ValueError:
                    raise ValueError(f"Valor no numérico en columna '{column}': '{valor_str}'")
            
            if not valores:
                raise ValueError("No hay datos en el CSV después de la cabecera")
            
            media = sum(valores) / len(valores)
            return media
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {path_str}")