from supervisely.app.widgets import NodesFlow

# lj_description_container
# lj_description_sidebar_container
# lj_description_title_preview

# lj_team_container
# lj_team_sidebar_container
# lj_team_preview_container

# lj_settings_classes_list_edit_container
# lj_settings_classes_list_widgets_container
# lj_settings_classes_list_preview

# lj_settings_tags_list_edit_container
# lj_settings_tags_list_widgets_container
# lj_settings_tags_list_preview

# lj_filters_edit_container
# lj_filters_condition_selector_field
# -


def create_settings_options(
    lj_description_container,
    lj_description_sidebar_container,
    lj_description_title_preview,
    lj_team_container,
    lj_team_sidebar_container,
    lj_team_preview_container,
    lj_settings_classes_list_edit_container,
    lj_settings_classes_list_widgets_container,
    lj_settings_classes_list_preview,
    lj_settings_tags_list_edit_container,
    lj_settings_tags_list_widgets_container,
    lj_settings_tags_list_preview,
    lj_filters_edit_container,
    lj_filters_condition_selector_field,
    lj_filters_preview_text,
):
    settings_options = [
        NodesFlow.Node.Option(
            name="Job Description",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=lj_description_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(lj_description_sidebar_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            name="Job Description Preview",
            option_component=NodesFlow.WidgetOptionComponent(lj_description_title_preview),
        ),
        NodesFlow.Node.Option(
            name="Job Team",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=lj_team_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(lj_team_sidebar_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            name="Job Team Preview",
            option_component=NodesFlow.WidgetOptionComponent(lj_team_preview_container),
        ),
        NodesFlow.Node.Option(
            name="Job Classes",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=lj_settings_classes_list_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(
                    lj_settings_classes_list_widgets_container
                ),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            name="Job Classes Preview",
            option_component=NodesFlow.WidgetOptionComponent(lj_settings_classes_list_preview),
        ),
        NodesFlow.Node.Option(
            name="Job Tags",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=lj_settings_tags_list_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(
                    lj_settings_tags_list_widgets_container
                ),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            name="Job Tags Preview",
            option_component=NodesFlow.WidgetOptionComponent(lj_settings_tags_list_preview),
        ),
        NodesFlow.Node.Option(
            name="Job Filters",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=lj_filters_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(
                    lj_filters_condition_selector_field
                ),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            name="Job Filters Preview",
            option_component=NodesFlow.WidgetOptionComponent(lj_filters_preview_text),
        ),
    ]

    return settings_options
