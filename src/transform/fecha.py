import pandas as pd


def build_dim_fecha(dfs):
    print("Building Dim_Fecha...")
    all_dates = set()
    services = dfs["mensajeria_servicio"]
    estados = dfs["mensajeria_estadosservicio"]
    novedades = dfs["mensajeria_novedadesservicio"]

    for col in ["fecha_solicitud", "fecha_deseada"]:
        valid_dates = pd.to_datetime(services[col], errors="coerce").dropna()
        all_dates.update(valid_dates.dt.date)

    valid_dates = pd.to_datetime(estados["fecha"], errors="coerce").dropna()
    all_dates.update(valid_dates.dt.date)

    valid_dates = pd.to_datetime(novedades["fecha_novedad"], errors="coerce").dropna()
    all_dates.update(valid_dates.dt.date)

    all_dates = {d for d in all_dates if d is not None and 2020 <= d.year <= 2026}

    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)
    else:
        min_date = pd.to_datetime("2023-01-01").date()
        max_date = pd.to_datetime("2024-12-31").date()

    date_range = pd.date_range(min_date, max_date)

    spanish_days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    spanish_months = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    filas = []
    for dt in date_range:
        filas.append({
            "Fecha_Key": int(dt.strftime("%Y%m%d")),
            "Fecha_Completa": dt.strftime("%d/%m/%Y"),
            "Dia_Semana": spanish_days[int(dt.strftime("%w"))],
            "Mes": spanish_months[dt.month],
            "Anio": dt.year
        })

    dim_fecha = pd.DataFrame(filas)
    default_fecha = pd.DataFrame([{
        "Fecha_Key": -1,
        "Fecha_Completa": "00/00/0000",
        "Dia_Semana": "No Especificado",
        "Mes": "No Especificado",
        "Anio": 0
    }])

    return pd.concat([default_fecha, dim_fecha], ignore_index=True)
