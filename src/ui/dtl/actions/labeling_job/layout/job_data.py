# from src.ui.dtl.utils import (
#     create_save_btn,
#     get_set_settings_button_style,
#     get_set_settings_container,
#     get_text_font_size,
# )
# from supervisely.app.widgets import Button, Container, Text, Input, TextArea, Field, SelectDataset


# def create_job_data_widgets():
#     # SIDEBAR SETTINGS
#     lj_dataset_selector = SelectDataset(compact=True, size="small")
#     lj_dataset_selector_field = Field(
#         title="Select Dataset",
#         description=(
#             "Labeler will be asked to annotate images from selected dataset. "
#             "You can select multiple datasets — "
#             "in this case new labeling job will be created for each dataset."
#         ),
#         content=lj_dataset_selector,
#     )

#     lj_dataset_save_btn = create_save_btn()
#     lj_dataset_sidebar_container = Container(
#         [
#             lj_dataset_selector_field,
#             lj_dataset_save_btn,
#         ]
#     )
#     # ----------------------------

#     # PREVIEW
#     lj_dataset_name_preview = Text("Title:", "text", font_size=get_text_font_size())
#     # ----------------------------

#     # LAYOUT
#     lj_dataset_text = Text("Data", status="text", font_size=get_text_font_size())
#     lj_dataset_edit_btn = Button(
#         text="EDIT",
#         icon="zmdi zmdi-folder",
#         button_type="text",
#         button_size="small",
#         emit_on_click="openSidebar",
#         style=get_set_settings_button_style(),
#     )

#     lj_dataset_container = get_set_settings_container(lj_dataset_text, lj_dataset_edit_btn)
#     # ----------------------------

#     return (
#         # sidebar
#         lj_dataset_selector,
#         lj_dataset_selector_field,
#         lj_dataset_save_btn,
#         lj_dataset_sidebar_container,
#         # preview
#         lj_dataset_name_preview,
#         # layout
#         lj_dataset_text,
#         lj_dataset_edit_btn,
#         lj_dataset_container,
#     )
