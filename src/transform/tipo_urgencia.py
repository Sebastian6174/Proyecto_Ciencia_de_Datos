import pandas as pd


def build_dim_tipo_urgencia():
    print("Building Dim_Tipo_Urgencia...")
    urgencia_data = [
        {"Tipo_Urgencia_Key": 1, "Categoria_Urgencia": "Alta", "Tiempo_Promesa_Horas": 1},
        {"Tipo_Urgencia_Key": 2, "Categoria_Urgencia": "Media", "Tiempo_Promesa_Horas": 3},
        {"Tipo_Urgencia_Key": 3, "Categoria_Urgencia": "Baja", "Tiempo_Promesa_Horas": 12},
        {"Tipo_Urgencia_Key": -1, "Categoria_Urgencia": "No Especificada", "Tiempo_Promesa_Horas": 0}
    ]
    return pd.DataFrame(urgencia_data)


def get_urgency_key(prio_str):
    if pd.isna(prio_str):
        return -1

    prio_str_lower = str(prio_str).lower()
    if "alta" in prio_str_lower or "una hora" in prio_str_lower:
        return 1
    if "media" in prio_str_lower or "1 a 3" in prio_str_lower or "1 - 3" in prio_str_lower:
        return 2
    if "baja" in prio_str_lower or "transcurso" in prio_str_lower:
        return 3

    return -1
