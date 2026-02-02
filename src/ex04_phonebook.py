"""
EX04 (Texto) · Listín telefónico en fichero

Vas a implementar un pequeño "CRUD" (Crear/Leer/Actualizar/Borrar) de contactos,
guardados en un fichero de texto.

Formato del fichero (una línea por contacto):
nombre,telefono

Ejemplo:
Ana,600123123
Luis,600000000

Para que el ejercicio sea más limpio, se proponen dos funciones "privadas":
- _load_phonebook(): lee el fichero y lo convierte en dict
- _save_phonebook(): guarda el dict en el fichero

Luego, las funciones públicas usan esas helpers:
- add_contact(): alta/actualización
- get_phone(): consulta
- remove_contact(): baja
"""

from __future__ import annotations
from pathlib import Path


def _load_phonebook(path: str | Path) -> dict[str, str]:
    """
    Carga el listín desde `path` y devuelve un diccionario {name: phone}.

    Reglas:
    - Si el fichero no existe, devuelve {} (NO es error).
    - Ignora líneas vacías.
    - Cada línea debe tener exactamente 2 partes separadas por coma:
      "nombre,telefono"
      Si alguna línea está mal formada, lanza ValueError.
    - Recorta espacios alrededor de nombre y teléfono con .strip().

    Consejo:
    - Usa `with open(..., encoding="utf-8") as f:`
    - Recorre línea a línea con `for line in f:`
    """
    phonebook = {}
    path_str = str(path)
    
    try:
        with open(path_str, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, 1):
                linea = linea.strip()
                if not linea:  # Ignorar líneas vacías
                    continue
                
                if ',' not in linea:
                    raise ValueError(f"Línea {num_linea} mal formada: falta coma")
                
                partes = linea.split(',', 1)  # Split en máximo 2 partes
                if len(partes) != 2:
                    raise ValueError(f"Línea {num_linea} mal formada: debe ser 'nombre,telefono'")
                
                nombre, telefono = partes
                nombre = nombre.strip()
                telefono = telefono.strip()
                
                if not nombre or not telefono:
                    raise ValueError(f"Línea {num_linea}: nombre o teléfono vacío")
                
                phonebook[nombre] = telefono
    
    except FileNotFoundError:
        return {}  # Si el archivo no existe, devolver diccionario vacío
    
    return phonebook


def _save_phonebook(path: str | Path, phonebook: dict[str, str]) -> None:
    """
    Guarda el diccionario en `path` en formato "nombre,telefono", una línea por contacto.

    Reglas:
    - Sobrescribe el fichero (modo 'w').
    - Puedes guardar en cualquier orden.
    - Usa encoding="utf-8".
    """
    path_str = str(path)
    
    with open(path_str, 'w', encoding='utf-8') as f:
        for nombre, telefono in phonebook.items():
            f.write(f"{nombre},{telefono}\n")


def add_contact(path: str | Path, name: str, phone: str) -> None:
    """
    Añade o actualiza un contacto (name -> phone) en el fichero.

    Reglas:
    - name y phone no pueden estar vacíos (tras strip). Si lo están, ValueError.
    - Si el contacto ya existe, se actualiza su teléfono.
    - Si no existe, se añade.

    Pista:
    - load -> modificar dict -> save
    """
    # Validar entrada
    nombre = name.strip()
    telefono = phone.strip()
    
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    if not telefono:
        raise ValueError("El teléfono no puede estar vacío")
    
    # Cargar agenda actual
    phonebook = _load_phonebook(path)
    
    # Añadir/actualizar contacto
    phonebook[nombre] = telefono
    
    # Guardar agenda actualizada
    _save_phonebook(path, phonebook)


def get_phone(path: str | Path, name: str) -> str | None:
    """
    Devuelve el teléfono del contacto `name` o None si no existe.

    Reglas:
    - Si el fichero no existe, devuelve None (porque no hay contactos).
    - `name` se compara tras strip().
    """
    nombre = name.strip()
    phonebook = _load_phonebook(path)
    
    # Devolver teléfono o None si no existe
    return phonebook.get(nombre)


def remove_contact(path: str | Path, name: str) -> bool:
    """
    Elimina el contacto `name` si existe.

    Devuelve:
    - True si se eliminó
    - False si no existía

    Reglas:
    - Si el fichero no existe, devuelve False.
    - `name` se compara tras strip().

    Pista:
    - load -> borrar si existe -> save si cambió
    """
    nombre = name.strip()
    phonebook = _load_phonebook(path)
    
    # Verificar si el contacto existe
    if nombre in phonebook:
        # Eliminar contacto
        del phonebook[nombre]
        # Guardar agenda actualizada
        _save_phonebook(path, phonebook)
        return True
    
    return False