from supervisely.app.widgets import (
    Container,
    Flexbox,
    Text,
    Select,
)
from src.ui.dtl.utils import get_text_font_size

apply_nn_selector_methods = [
    Select.Item("image", "Full Image"),
    Select.Item("roi", "ROI defined by object BBox (Coming Soon)", disabled=True),
    Select.Item("sliding_window", "Sliding Window (Coming Soon)", disabled=True),
]
apply_nn_method_text = Text("Apply Method", font_size=get_text_font_size())
apply_nn_methods_selector = Select(items=apply_nn_selector_methods, size="small")

apply_nn_method_container = Container(
    widgets=[
        apply_nn_method_text,
        Flexbox(
            widgets=[apply_nn_methods_selector],
        ),
    ],
    style="margin-top: 15px;",
    gap=4,
)
