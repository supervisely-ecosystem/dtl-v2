# Filtered Project

`Filtered Project` layer is a special layer that can be added only via filters menu of the project page. This layer contains information about filtered entities from a project and can be used in the next layers of the transformation process.

## How to use:

1. Select filtered images
2. Press Run pipeline button and select template

![image](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/affba42f-abb7-43ab-8533-a7d6fc3bc212)

> ✅ Don't worry, your original project will remain safe in your workspace. Any changes you make using all the layers will not affect source project, unless you use `Move` layer that will move filtered entities to another project and remove them from the source project.

<details>
  <summary>Specific datasets and classes</summary>
<pre>
    {
        "action": "filtered_project",
        "src": [
            "my_project/*"
        ],
        "dst": "$filtered_project_1",
        "settings": {
            "project_id": 38019,
            "filtered_entities_ids": [
                30449861,
                30449862,
                30449863,
                30449867,
                30449868,
                30449869
            ],
            "classes_mapping": "default",
            "tags_mapping": "default"
        }
    },
</pre>
</details>
