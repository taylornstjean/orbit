import plotly.graph_objects as go
import numpy as np


def _get_layout(max_x, max_y, max_z):
    layout = go.Layout(
        scene=dict(
            aspectmode="data",
            xaxis_range=[-max_x, max_x],
            yaxis_range=[-max_y, max_y],
            zaxis_range=[-max_z, max_z],
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
        mode="markers+text",
        text="Star",
        marker={
            "color": "yellow",
            "size": 3
        }
    )

    x_vals = [0]
    y_vals = [0]
    z_vals = [0]

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

            x_vals.append(np.max(np.abs(x)))
            y_vals.append(np.max(np.abs(y)))
            z_vals.append(np.max(np.abs(z)))

        if params["position"] is True:
            x, y, z = obj.position()
            marker = go.Scatter3d(
                x=x, y=y, z=z,
                mode="markers+text",
                text=obj.name,
                marker={
                    "color": params["color"],
                    "size": params["size"]
                }
            )
            to_plot.append(marker)

    max_x = np.ceil(np.max(x_vals))
    max_y = np.ceil(np.max(y_vals))
    max_z = np.ceil(np.max(z_vals))

    fig = go.Figure(
        data=to_plot,
        layout=_get_layout(max_x, max_y, max_z)
    )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.write_html("plot.html", include_plotlyjs="cdn")
    fig.show()
