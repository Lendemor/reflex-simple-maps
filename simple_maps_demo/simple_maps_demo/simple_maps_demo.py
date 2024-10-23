"""Welcome to Reflex! This file showcases the custom component in a basic app."""

import httpx
from reflex_simple_maps import simple_maps as sm
from rxconfig import config

import reflex as rx

filename = f"{config.app_name}/{config.app_name}.py"

geoUrl = "https://code.highcharts.com/mapdata/custom/world-highres.topo.json"


class State(rx.State):
    """The app state."""

    clicked_names: dict[str, int] = {}
    border = "none"

    def show_clicked_name(self, name, properties):
        print(name, properties)
        if name in self.clicked_names:
            if self.clicked_names[name] > 5:
                self.clicked_names[name] = 5
            else:
                self.clicked_names[name] += 1
        else:  # First time clicked
            self.clicked_names[name] = 1


def scale_match():
    return rx.match(
        State.clicked_names[rx.Var("geo.id").to(str)],
        (0, "gray"),
        (1, "green"),
        (2, "blue"),
        (3, "red"),
        (4, "yellow"),
        (5, "purple"),
        "black",
    )


def index():
    return rx.vstack(
        rx.text(State.clicked_names),
        sm.composable_map(
            sm.graticule(stroke="#999"),
            sm.geographies(
                geography="/features.json",
                on_click=State.show_clicked_name,
                fill="#FFFFFF",
                stroke=rx.color("accent", 10),
                border=State.border,
                geography_props={
                    "default": {
                        "fill": scale_match(),
                        "outline": "none",
                        "z_index": 0,
                    },
                    "hover": {
                        "fill": scale_match(),
                        "stroke": "red",
                        "outline": "none",
                        "z_index": 5,
                    },
                },
            ),
            projection="geoEqualEarth",
            projection_config={
                "rotate": [-10.0, -52.0, 0],
                "center": [5, -4],
                "scale": 1100,
            },
            # border="1px solid red",
            style={
                "svg": {"display": "inline-block", "vertical-align": "middle"},
                "path": {"fill": "#E0E0E0"},
            },
        ),
        width="100%",
        height="100%",
    )  # , rx.color_mode.button(position="top-right")


# Add state and page to the app.
app = rx.App()
app.add_page(index)
