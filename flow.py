import dash
import dash_core_components as dcc
import dash_html_components as html
import vtk
import dash_vtk
from dash_vtk.utils import to_mesh_state

reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName("./data/flow_pyevtk.vtu")
reader.Update()  # Needed because of GetScalarRange
output = reader.GetOutput()

mesh_state = to_mesh_state(reader.GetOutput())
vtk_view = dash_vtk.View(
    id="vtk-view",
    children=[
        dash_vtk.GeometryRepresentation(
            children=[dash_vtk.Mesh(state=mesh_state)],
        )
    ],
)


app = dash.Dash(__name__, external_stylesheets=[])
app.layout = html.Div(
    style={"height": "calc(100vh - 16px)", "width": "100%"},
    children=[html.Div(vtk_view, style={"height": "100%", "width": "100%"})],
)


if __name__ == "__main__":
    app.run_server(debug=True)
