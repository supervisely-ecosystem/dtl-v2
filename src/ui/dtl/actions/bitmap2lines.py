import copy
import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class Bitmap2LinesAction(Action):
    name = "bitmap2lines"
    title = "Bitmap to Lines"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bitmap2lines"
    description = "This layer (bitmap2lines) converts thinned (skeletonized) bitmaps to lines. It is extremely useful if you have some raster objects representing lines or edges, maybe forming some tree or net structure, and want to work with vector objects. Each input bitmap should be already thinned (use Skeletonize layer to do it), and for single input mask a number of lines will be produced. Resulting lines may have very many vertices, so consider applying Approx Vector layer to results of this layer. Internally the layer builds a graph of 8-connected pixels, determines minimum spanning tree(s), then greedely extracts diameters from connected components of the tree."

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        cls.create_info_widget()
                    )
                ),
            ),
            NodesFlow.Node.Option(
                name="min_points_cnt_text",
                option_component=NodesFlow.TextOptionComponent("Min Points Count"),
            ),
            NodesFlow.Node.Option(
                name="min_points_cnt", option_component=NodesFlow.IntegerOptionComponent(min=2, default_value=2)
            ),
            NodesFlow.Node.Option(
                name="classes_mapping_text",
                option_component=NodesFlow.TextOptionComponent("Classes Mapping"),
            ),
            NodesFlow.Node.Option(
                name="classes_mapping",
                option_component=NodesFlow.InputOptionComponent(),
            ),
        ]
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        classes_mapping = json.loads(options["classes_mapping"])
        return {
            "settings": {
                "classes_mapping": classes_mapping,
                "min_points_cnt": options["min_points_cnt"],
            }
        }
