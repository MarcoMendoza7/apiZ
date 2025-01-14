from flask import Flask, render_template
from nbconvert import HTMLExporter
import nbformat
import os

app = Flask(__name__)

notebook_mapping = {
    "numpy": "01_Numpy_3501.ipynb",
    "pandas": "3501_Pandas.ipynb",
    "matplotlib": "3501_Matplotlib.ipynb",
    "visualizacion": "3501_Visualizacion-de-Datos.ipynb",
    "regresion_logistica": "3501_Regresion_Logistica.ipynb",
    "regresion_lineal": "3501_Regresion_Lineal.ipynb",
    "preparacion_dataset": "3501_Preparacion-del-DataSet.ipynb",
    "evaluacion_resultados": "3501_Evaluación_de_Resultados.ipynb",
    "transformadores_pipelines": "3501_Creacion-de-Transformadores-y-Pipelines-Personalizados.ipynb",
    "svm": "3501_Support-Vector-Machine.ipynb",
    "tree": "3501_Arboles_De_Desicion.ipynb",
    "new": "3501_Regresion_Logistica_DataSet.ipynb",
}

# Ruta a la carpeta de notebooks
notebooks_folder = "notebooks"

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/notebook/<notebook_name>")
def render_notebook(notebook_name):
    if notebook_name not in notebook_mapping:
        return f"<p>NOTEBOOK '{notebook_name}'NO ENCONTRADO.</p>", 404

    notebook_path = os.path.join(notebooks_folder, notebook_mapping[notebook_name])

   
    if not os.path.exists(notebook_path):
        return f"<p>NOTEBOOK '{notebook_path}'NO EXISTENTE.</p>", 404

    # Convertir el notebook a HTML, pero solo mostrar los resultados
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Filtrar celdas de tipo 'code' para mostrar solo salidas
        filtered_cells = []
        for cell in notebook_content.cells:
            if cell.cell_type == 'code':
                # Conservar solo las salidas (outputs) de las celdas de código
                cell['source'] = ''  # Eliminar el código
                cell['outputs'] = [output for output in cell.get('outputs', [])]
            # Conservar celdas de tipo 'markdown' (texto)
            if cell.cell_type == 'markdown' or (cell.cell_type == 'code' and cell['outputs']):
                filtered_cells.append(cell)

        # Crear un nuevo notebook con las celdas filtradas
        notebook_content.cells = filtered_cells

        # Usar nbconvert para convertir el notebook filtrado a HTML
        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(notebook_content)

        return body  # Devuelve el contenido HTML con solo los resultados

    except Exception as e:
        return f"<p>RENDERIZACIÓN ERRONEA: {str(e)}</p>", 500

if __name__ == "__main__":
    app.run(debug=True)
