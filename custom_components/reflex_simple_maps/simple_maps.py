"""Reflex custom component SimpleMaps."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

from typing import Any
import reflex as rx
from reflex.constants.colors import Color

# Some libraries you want to wrap may require dynamic imports.
# This is because they they may not be compatible with Server-Side Rendering (SSR).
# To handle this in Reflex, all you need to do is subclass `NoSSRComponent` instead.
# For example:
# from reflex.components.component import NoSSRComponent
# class SimpleMaps(NoSSRComponent):
#     pass


class BaseSimpleMaps(rx.Component):
    """SimpleMaps component."""

    # The React library to wrap.
    library = "react-simple-maps@2.3.0"


class Annotation(BaseSimpleMaps):
    """Annotation component."""

    # The React component to wrap.
    tag = "Annotation"

    alias = "SimpleMapsAnnotation"

    # The location target of the annotation.
    subject: rx.Var[list] = rx.Var.create([])

    # Horizontal offset for the content of the annotation.
    dx: rx.Var[int] = rx.Var.create(0)

    # Vertical offset for the content of the annotation.
    dy: rx.Var[int] = rx.Var.create(0)

    # The curve of the line connecting the annotation content and the target. Recommended values are between -1 and 1. Default is 0.
    curve: rx.Var[int] = rx.Var.create(0)

    # Props for the connector line.
    connector_props: rx.Var[dict] = rx.Var.create({})


class ComposableMap(BaseSimpleMaps):
    """ComposableMap component."""

    # The React component to wrap.
    tag = "ComposableMap"

    alias = "SimpleMapsComposableMap"

    width: rx.Var[int] = rx.Var.create(800)

    height: rx.Var[int] = rx.Var.create(400)

    projection: rx.Var[str] = rx.Var.create("geoEqualEarth")

    projection_config: rx.Var[dict] = rx.Var.create({})


# class GeoVar(Var):


class Geographies(BaseSimpleMaps):
    """Geographies component."""

    # The React component to wrap.
    tag = "Geographies"

    alias = "SimpleMapsGeographies"

    # The geography to render.
    geography: rx.Var[str | dict | list]

    fill: rx.Var[str] = rx.Var.create("transparent")

    stroke: rx.Var[str | Color] = rx.Var.create("currentcolor")

    def add_imports(self):
        return {
            self.library: rx.ImportVar(tag="Geography", alias="SimpleMapsGeography")
        }

    @classmethod
    def create(cls, *children, **props):
        """Create a Geographies component."""

        on_click = props.pop("on_click", None)

        Geography.create()

        def georender(geo):
            return Geography.create(
                key=rx.Var("geo.rsmKey"),
                geography=geo,
                style={
                    "default": {"fill": "gray", "outline": "none"},
                    "hover": {"stroke": "red", "outline": "none"},
                    "pressed": {"fill": "red", "outline": "none"},
                },
                on_click=lambda _1, _2: on_click(
                    rx.Var("geo.id", _var_type=str),
                    rx.Var("geo.properties", _var_type=dict),
                ).stop_propagation,
                **props.pop("geography_props", {}),
            )

        def get_children_1():
            fr = rx.foreach(
                rx.Var("geographies", _var_type=rx.Var),
                georender,
            )
            return [
                rx.Var(f"({{geographies}}) => {fr}"),
            ]

        def get_children_2():
            return [
                (rx.Var("geographies", _var_type=rx.Var).to(list).foreach(georender))
            ]

        if not children:
            children = get_children_1()

        props["on_click"] = lambda: on_click("", {})

        return super().create(*children, **props)


class Geography(BaseSimpleMaps):
    """Geography component."""

    # The React component to wrap.
    tag = "Geography"

    alias = "SimpleMapsGeography"

    geography: rx.Var[Any]

    on_click: rx.EventHandler[lambda e0, e1: [e0, e1]]

    def _get_style(self) -> dict:
        return {"style": self.style}


class Graticule(BaseSimpleMaps):
    """Graticule component."""

    # The React component to wrap.
    tag = "Graticule"

    alias = "SimpleMapsGraticule"

    # The fill color of the graticule. Default is transparent.
    fill: rx.Var[str] = rx.Var.create("transparent")

    # The stroke color of the graticule. Default is currentcolor.
    stroke: rx.Var[str] = rx.Var.create("currentcolor")

    # The separation between each line of the grid.
    step: rx.Var[list] = rx.Var.create([10, 10])


class Line(BaseSimpleMaps):
    """Line component."""

    # The React component to wrap.
    tag = "Line"

    alias = "SimpleMapsLine"

    from_: rx.Var[list] = rx.Var.create([0, 0])

    to: rx.Var[list] = rx.Var.create([0, 0])

    coordinates: rx.Var[list] = rx.Var.create([])

    stroke: rx.Var[str] = rx.Var.create("currentcolor")

    stroke_width: rx.Var[int] = rx.Var.create(3)

    fill: rx.Var[str] = rx.Var.create("transparent")


class Sphere(BaseSimpleMaps):
    """Sphere component."""

    # The React component to wrap.
    tag = "Sphere"

    alias = "SimpleMapsSphere"

    id: rx.Var[str] = rx.Var.create("rsm-sphere")

    fill: rx.Var[str] = rx.Var.create("transparent")

    stroke: rx.Var[str] = rx.Var.create("currentcolor")

    stroke_width: rx.Var[int] = rx.Var.create(0.5)


class Marker(BaseSimpleMaps):
    """Marker component."""

    # The React component to wrap.
    tag = "Marker"

    alias = "SimpleMapsMarker"

    coordinates: rx.Var[list] = rx.Var.create([])


inf = rx.Var("Infinity")
inf_min = rx.Var("-Infinity")


class ZoomableGroup(BaseSimpleMaps):
    """ZoomableGroup component."""

    # The React component to wrap.
    tag = "ZoomableGroup"

    alias = "SimpleMapsZoomableGroup"

    center: rx.Var[list] = rx.Var.create([0, 0])

    zoom: rx.Var[int] = rx.Var.create(1)

    min_zoom: rx.Var[int] = rx.Var.create(1)

    max_zoom: rx.Var[int] = rx.Var.create(8)

    translate_extent: rx.Var[list] = rx.Var.create([[inf_min, inf_min], [inf, inf]])

    on_move: rx.EventHandler[lambda e0: [e0]]

    on_move_start: rx.EventHandler[lambda e0: [e0]]

    on_move_end: rx.EventHandler[lambda e0: [e0]]

    filter_zoom_event: rx.EventHandler[lambda e0: [e0]]


class SimpleMapsNamespace(rx.ComponentNamespace):
    """SimpleMaps namespace."""

    annotation = Annotation.create
    composable_map = ComposableMap.create
    geographies = Geographies.create
    geography = Geography.create
    graticule = Graticule.create
    line = Line.create
    sphere = Sphere.create
    marker = Marker.create
    zoomable_group = ZoomableGroup.create


simple_maps = SimpleMapsNamespace()
