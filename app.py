import streamlit as st
import pandas as pd
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Historia de México",
    page_icon="🇲🇽",
    layout="wide"
)

# -----------------------------
# Datos históricos
# -----------------------------

periodos = {
    "México prehispánico": {
        "inicio": -2500,
        "fin": 1521,
        "color": "#8E44AD",
        "descripcion": (
            "Periodo de desarrollo de diversas civilizaciones mesoamericanas, "
            "como los olmecas, mayas, zapotecas, mixtecas, toltecas y mexicas."
        ),
        "eventos": [
            "Aparición de las primeras aldeas agrícolas",
            "Desarrollo de ciudades mesoamericanas",
            "Fundación de México-Tenochtitlan",
            "Expansión del Imperio mexica"
        ]
    },
    "Conquista y Virreinato": {
        "inicio": 1521,
        "fin": 1821,
        "color": "#D35400",
        "descripcion": (
            "Etapa de dominio español, reorganización política y social, "
            "evangelización y formación de la Nueva España."
        ),
        "eventos": [
            "Caída de México-Tenochtitlan",
            "Creación del Virreinato de Nueva España",
            "Reformas borbónicas",
            "Desigualdad social y económica"
        ]
    },
    "Independencia": {
        "inicio": 1810,
        "fin": 1821,
        "color": "#27AE60",
        "descripcion": (
            "Proceso político y militar que terminó con el dominio español "
            "y dio origen al México independiente."
        ),
        "eventos": [
            "Grito de Dolores",
            "Campañas insurgentes",
            "Constitución de Apatzingán",
            "Consumación de la Independencia"
        ]
    },
    "México del siglo XIX": {
        "inicio": 1821,
        "fin": 1910,
        "color": "#2980B9",
        "descripcion": (
            "Periodo marcado por la construcción del Estado mexicano, "
            "conflictos entre liberales y conservadores, guerras e intervención extranjera."
        ),
        "eventos": [
            "Primera República Federal",
            "Guerra de Reforma",
            "Intervención francesa",
            "Restauración de la República",
            "Porfiriato"
        ]
    },
    "Revolución Mexicana": {
        "inicio": 1910,
        "fin": 1920,
        "color": "#C0392B",
        "descripcion": (
            "Conflicto armado y transformación política que cuestionó el régimen "
            "porfirista y promovió cambios sociales y agrarios."
        ),
        "eventos": [
            "Plan de San Luis",
            "Caída de Porfirio Díaz",
            "Constitución de 1917",
            "Reformas agrarias y laborales"
        ]
    },
    "México contemporáneo": {
        "inicio": 1920,
        "fin": 2026,
        "color": "#16A085",
        "descripcion": (
            "Etapa de institucionalización política, industrialización, "
            "urbanización y cambios democráticos."
        ),
        "eventos": [
            "Creación de instituciones nacionales",
            "Industrialización",
            "Movimiento estudiantil de 1968",
            "Transición democrática",
            "México actual"
        ]
    }
}

# -----------------------------
# Encabezado
# -----------------------------

st.title("🇲🇽 Mapa conceptual: Historia de México")
st.write(
    "Explora los principales periodos históricos de México mediante un mapa "
    "conceptual, estadísticas y una línea del tiempo."
)

# -----------------------------
# Barra lateral
# -----------------------------

st.sidebar.header("Filtros")

periodo_seleccionado = st.sidebar.selectbox(
    "Selecciona un periodo",
    ["Todos"] + list(periodos.keys())
)

mostrar_eventos = st.sidebar.checkbox(
    "Mostrar eventos principales",
    value=True
)

# -----------------------------
# Estadísticas generales
# -----------------------------

total_periodos = len(periodos)
total_eventos = sum(len(p["eventos"]) for p in periodos.values())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Periodos históricos", total_periodos)
col2.metric("Eventos registrados", total_eventos)
col3.metric("Inicio aproximado", "2500 a. C.")
col4.metric("Año de independencia", "1821")

st.divider()

# -----------------------------
# Crear mapa conceptual
# -----------------------------

st.subheader("Mapa conceptual")

red = Network(
    height="650px",
    width="100%",
    bgcolor="#FFFFFF",
    font_color="#222222",
    directed=True
)

red.set_options("""
{
  "nodes": {
    "shape": "dot",
    "size": 25,
    "font": {
      "size": 18,
      "face": "Arial"
    },
    "borderWidth": 2
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 1
      }
    },
    "smooth": {
      "type": "curvedCW",
      "roundness": 0.2
    }
  },
  "physics": {
    "enabled": true,
    "stabilization": {
      "iterations": 150
    }
  }
}
""")

# Nodo principal
red.add_node(
    "historia_mexico",
    label="Historia de México",
    color="#006847",
    size=40,
    title="Proceso histórico de México"
)

# Filtrar periodos
if periodo_seleccionado == "Todos":
    periodos_mostrados = periodos
else:
    periodos_mostrados = {
        periodo_seleccionado: periodos[periodo_seleccionado]
    }

for nombre, datos in periodos_mostrados.items():
    id_periodo = nombre.replace(" ", "_")

    red.add_node(
        id_periodo,
        label=nombre,
        color=datos["color"],
        title=datos["descripcion"],
        size=30
    )

    red.add_edge("historia_mexico", id_periodo)

    if mostrar_eventos:
        for indice, evento in enumerate(datos["eventos"]):
            id_evento = f"{id_periodo}_{indice}"

            red.add_node(
                id_evento,
                label=evento,
                color="#95A5A6",
                size=17,
                title=f"Evento relacionado con {nombre}"
            )

            red.add_edge(id_periodo, id_evento)

red.save_graph("mapa_historia_mexico.html")

with open("mapa_historia_mexico.html", "r", encoding="utf-8") as archivo:
    html = archivo.read()

components.html(html, height=680, scrolling=True)

# -----------------------------
# Información del periodo
# -----------------------------

st.divider()
st.subheader("Información histórica")

if periodo_seleccionado == "Todos":
    for nombre, datos in periodos.items():
        with st.expander(nombre):
            st.write(datos["descripcion"])
            st.write(
                f"**Periodo aproximado:** {datos['inicio']} - {datos['fin']}"
            )
            st.write("**Eventos principales:**")
            for evento in datos["eventos"]:
                st.write(f"- {evento}")
else:
    datos = periodos[periodo_seleccionado]

    st.info(datos["descripcion"])
    st.write(
        f"**Periodo aproximado:** {datos['inicio']} - {datos['fin']}"
    )

    st.write("**Eventos principales:**")
    for evento in datos["eventos"]:
        st.write(f"- {evento}")

# -----------------------------
# Línea del tiempo
# -----------------------------

st.divider()
st.subheader("Línea del tiempo")

datos_tiempo = []

for nombre, datos in periodos.items():
    datos_tiempo.append({
        "Periodo": nombre,
        "Inicio": datos["inicio"],
        "Fin": datos["fin"],
        "Duración": datos["fin"] - datos["inicio"],
        "Color": datos["color"]
    })

df_tiempo = pd.DataFrame(datos_tiempo)

grafica = px.timeline(
    df_tiempo,
    x_start="Inicio",
    x_end="Fin",
    y="Periodo",
    color="Periodo",
    hover_data=["Duración"],
    title="Duración aproximada de los principales periodos"
)

grafica.update_yaxes(autorange="reversed")
grafica.update_layout(
    height=500,
    showlegend=False,
    xaxis_title="Año",
    yaxis_title=""
)

st.plotly_chart(grafica, use_container_width=True)

# -----------------------------
# Estadística de duración
# -----------------------------

st.divider()
st.subheader("Duración aproximada por periodo")

grafica_duracion = px.bar(
    df_tiempo,
    x="Periodo",
    y="Duración",
    color="Periodo",
    text="Duración",
    title="Duración aproximada en años"
)

grafica_duracion.update_layout(
    showlegend=False,
    xaxis_title="Periodo histórico",
    yaxis_title="Años"
)

st.plotly_chart(grafica_duracion, use_container_width=True)

# -----------------------------
# Tabla de datos
# -----------------------------

st.subheader("Tabla de datos")

df_tabla = df_tiempo.copy()
df_tabla["Inicio"] = df_tabla["Inicio"].apply(
    lambda x: f"{abs(x)} a. C." if x < 0 else str(x)
)
df_tabla["Fin"] = df_tabla["Fin"].apply(
    lambda x: f"{abs(x)} a. C." if x < 0 else str(x)
)

st.dataframe(
    df_tabla[["Periodo", "Inicio", "Fin", "Duración"]],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Nota: Las fechas de los periodos prehispánicos son aproximadas y "
    "pueden variar según la fuente histórica."
)
