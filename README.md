# Proyecto Ciencia de Datos - Fast and Safe

## Integrantes

* Juan Sebastian Sierra- 202343656
* Jhoan Sebastian Fernandez- 2222772
* Luis Felipe Londoño- 2343105

---

# Descripción del proyecto

Este proyecto implementa un proceso ETL (Extract, Transform, Load) y una Bodega de Datos (Data Warehouse) para el proyecto del curso: **Fast and Safe**.

A partir de una base de datos operacional exportada en formato SQL (`copia-BD.sql`), el sistema:

1. Extrae la información relevante.
2. Transforma los datos aplicando reglas de negocio.
3. Construye dimensiones y tablas de hechos.
4. Genera archivos CSV para análisis.
5. Carga automáticamente la información en PostgreSQL.

---

# Arquitectura

Base de Datos Operacional (SQL Dump)

↓

Extracción (Extract)

↓

Transformación (Transform)

↓

Data Warehouse

↓

PostgreSQL + CSV

↓

Power BI

---

# Tecnologías utilizadas

* Python 3.11+
* Pandas
* NumPy
* PostgreSQL 12
* Docker
* pgAdmin 4
* SQLAlchemy
* psycopg2
* Power BI

---

# Estructura del proyecto

```text
proyecto_ciencia_de_datos/

├── data/
│   ├── copia-BD.sql
│   └── fast_and_safe_dw.sql
│
├── docs/
│
├── dw_data/
│   ├── Dim_Ciudad.csv
│   ├── Dim_Cliente.csv
│   ├── ...
│   ├── Fact_Servicios.csv
│   └── Fact_Novedades.csv
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── test_postgres.py
│
├── main.py
├── requirements.txt
└── README.md
```

# Instalación

## 1. Clonar el repositorio

```bash
git clone <https://github.com/Sebastian6174/Proyecto_Ciencia_de_Datos.git>
cd proyecto_ciencia_de_datos
```

## 2. Crear entorno virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### Configuración de PostgreSQL y pgAdmin

El proyecto utiliza Docker Compose para desplegar PostgreSQL y pgAdmin.

## Levantar los servicios

Ubicarse en la raíz del proyecto y ejecutar:

```bash
docker compose up -d
```

Verificar que los contenedores estén ejecutándose:

```bash
docker ps
```

Se deben visualizar los contenedores:

```text
ciencia_datos
pgadmin4CD
```

## Configuración utilizada

### PostgreSQL

```text
Host: localhost
Puerto: 5432
Usuario: postgres
Contraseña: postgres
```

### pgAdmin

Acceder desde el navegador:

```text
http://localhost:8080
```

Credenciales:

```text
Correo: admin@admin.com
Contraseña: 12345
```

## Registrar el servidor en pgAdmin

Al ingresar por primera vez a pgAdmin:

1. Click derecho sobre "Servers".
2. Seleccionar "Register → Server".

### General

```text
Name: FastAndSafeDW
```

### Connection

```text
Host name/address: postgres
Port: 5432
Maintenance database: postgres
Username: postgres
Password: postgres
```

Guardar la configuración.

## Crear la base de datos

Dentro del servidor PostgreSQL crear la base de datos:

```text
fast_and_safe_dw
```

---

# Ejecución del proyecto

Ejecutar:

```bash
python main.py
```

El sistema realizará automáticamente:

* Extracción
* Transformación
* Construcción de dimensiones
* Construcción de tablas de hechos
* Generación de CSV
* Carga a PostgreSQL

---

# Tablas generadas

## Dimensiones

* Dim_Ciudad
* Dim_Cliente
* Dim_Sede
* Dim_Mensajero
* Dim_Tipo_Urgencia
* Dim_Servicio
* Dim_Tipo_Novedad
* Dim_Hora
* Dim_Fecha

## Hechos

* Fact_Servicios
* Fact_Novedades

---

# Conexión desde Power BI

Seleccionar:

```text
Obtener Datos
↓
PostgreSQL Database
```

Parámetros:

```text
Servidor: localhost
Puerto: 5432
Base de datos: fast_and_safe_dw
Usuario: postgres
Contraseña: postgres
```

Importar las dimensiones y tablas de hechos para construir los dashboards analíticos.

---

# Resultado esperado

Al finalizar la ejecución:

* Los archivos CSV quedan almacenados en `dw_data/`.
* Las tablas del Data Warehouse quedan cargadas en PostgreSQL.
* La base puede ser consultada desde pgAdmin y Power BI.
