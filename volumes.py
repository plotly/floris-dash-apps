import dash
import random
import dash_html_components as html
import dash_vtk
import numpy as np

import floris.tools as wfct


# Initialize the FLORIS interface fi
fi = wfct.floris_interface.FlorisInterface("./data/example_input.json")
fd = fi.get_flow_data()

field = fd.u

origin = [fd.x.mean(), fd.y.mean(), fd.z.mean()]
ranges = np.array([axis.ptp() for axis in [fd.x, fd.y, fd.z]])
dimensions = np.array([np.unique(axis).shape[0] for axis in [fd.x, fd.y, fd.z]])
x, y, z = dimensions
spacing = np.round(ranges / dimensions).astype(int)


content = dash_vtk.View(
    dash_vtk.VolumeRepresentation(
        [
            dash_vtk.VolumeController(),
            dash_vtk.ImageData(
                dimensions=dimensions,
                spacing=spacing,
                origin=origin,
                children=dash_vtk.PointData(
                    dash_vtk.DataArray(registration="setScalars", values=field)
                ),
            ),
        ]
    )
)

# Dash setup
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"width": "100%", "height": "calc(100vh - 15px)"},
    children=[content],
)

if __name__ == "__main__":
    app.run_server(debug=True)