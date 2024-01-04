import plotly.graph_objects as go


def _get_layout():
    layout = go.Layout(
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor="black",
        hovermode=False
    )

    return layout


def generate_plot(objects):

    sun = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers",
        marker={
            "color": "yellow",
            "size": 4
        }
    )

    to_plot = [sun]
    for obj, params in objects.items():
        if params["orbit"] is True:
            x, y, z = obj.ellipse_points()
            orbit = go.Scatter3d(
                x=x, y=y, z=z,
                mode="lines",
                line={
                    "color": params["color"],
                    "width": params["width"]
                }
            )
            to_plot.append(orbit)

        if params["position"] is True:
            x, y, z = obj.position()
            marker = go.Scatter3d(
                x=x, y=y, z=z,
                mode="markers",
                marker={
                    "color": params["color"],
                    "size": params["size"]
                }
            )
            to_plot.append(marker)

    fig = go.Figure(
        data=to_plot,
        layout=_get_layout()
    )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.write_html("plot.html", include_plotlyjs="cdn")
    fig.show()
