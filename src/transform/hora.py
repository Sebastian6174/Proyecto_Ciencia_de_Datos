import pandas as pd


def build_dim_hora():
    print("Building Dim_Hora...")
    horas = []
    for h in range(24):
        if 0 <= h <= 5:
            franja = "Madrugada"
        elif 6 <= h <= 11:
            franja = "Mañana"
        elif 12 <= h <= 17:
            franja = "Tarde"
        else:
            franja = "Noche"
        horas.append({
            "Hora_Key": h,
            "Hora_Militar": f"{h:02d}",
            "Franja_Horaria": franja
        })

    dim_hora = pd.DataFrame(horas)
    default_hora = pd.DataFrame([{
        "Hora_Key": -1,
        "Hora_Militar": "N/A",
        "Franja_Horaria": "No Especificada"
    }])

    return pd.concat([default_hora, dim_hora], ignore_index=True)
