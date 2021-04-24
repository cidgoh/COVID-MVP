"""Entry point of the codebase.

This is the Python script that is run to launch the visualization
application.
"""

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html

from data_parser import get_data
import div_generator
import table_generator

app = dash.Dash(__name__,
                # We can use bootstrap CSS.
                # https://bit.ly/3tMqY0W for details.
                external_stylesheets=[dbc.themes.BOOTSTRAP])

data = get_data("data")
clade_defining_mutations_data = get_data("clade_defining_mutations_data")

app.layout = dbc.Container([
    html.Div(div_generator.get_toolbar_row_div()),
    html.Div(div_generator.get_heatmap_row_div(data), id="heatmap-fig"),
    html.Div(div_generator.get_table_row_div(data))
], fluid=True)


@app.callback(
    Output("table", "figure"),
    inputs=[
        Input("heatmap-center-fig", "clickData"),
        Input("clade-defining-mutations-switch", "value")
    ],
    prevent_initial_call=True
)
def display_table(click_data, switches_value):
    """Callback function for updating table.

    The table is updated when a heatmap cell is clicked, or the clade
    defining mutations switch is toggled.

    :param click_data: Information on heatmap cell clicked
    :type click_data: dict
    :param switches_value: Information on clade defining mutations
        switch.
    :type switches_value: dict
    :return: Table figure to show
    :rtype: plotly.graph_objects.Figure
    """
    if click_data is None:
        table_strain = data["heatmap_y"][0]
    else:
        table_strain = click_data["points"][0]["y"]

    if len(switches_value) > 0:
        return table_generator \
            .get_table_fig(clade_defining_mutations_data, table_strain)
    else:
        return table_generator.get_table_fig(data, table_strain)

@app.callback(
    Output("heatmap-fig", "children"),
    Input("clade-defining-mutations-switch", "value"),
    Input("upload-file", "contents"),
    State("upload-file", "filename"),
    prevent_initial_call=True
)
def update_heatmap(switches_value, file_contents, filename):
    """Callback function for updating heatmap.

    Dash does not allow a many-to-one mapping of callback functions and
    outputs, so this function will update the heatmap in a variety of
    ways, given a variety of inputs.

    When the clade definitions mutation switch is toggled, the heatmap
    is updated to show the appropriate mutations.

    When a file is uploaded, the heatmap is updated to show an
    additional row.

    :param switches_value: ``[1]`` or ``[0]`` is clade defining
        mutations switch is toggled on or off respectively.
    :type switches_value: list
    :param file_contents: base64 encoded string of uploaded file
        contents.
    :type file_contents: str
    :param filename: Name of uploaded file
    :type filename: str
    :return: New dash bootstrap components row containing heatmap
        figures.
    :rtype: dbc.Row
    """
    if len(switches_value) > 0:
        data_to_use = clade_defining_mutations_data
    else:
        data_to_use = data

    # TODO ensure appropriate uploaded file, and add to heatmap

    heatmap_row_div = div_generator.get_heatmap_row_div(data_to_use)

    return heatmap_row_div


if __name__ == "__main__":
    app.run_server(debug=True)
