# Filter Videos by Tag Action

`Filter video by Tag Action` layer is used to route videos down either the "True" or "False" branch, depending on specific tag inclusion and exclusion criteria. Users can define tag and filtering condition either "with tag" or "without tag". 

# Settings

- **Tag** - Represents the tag by which videos would be filtered
  - **Name** - Tag Meta Name
  - **Value** - Tag Value
- **Condition** - Filtering condition: either with or without tag

### JSON views

<details>
  <summary>With Tag with None value type</summary>

```json
{
    "action": "filter_video_by_tag",
    "src": [
        "$data_1"
    ],
    "dst": [
        "$filter_video_by_tag_2__true",
        "$filter_video_by_tag_2__false"
    ],
    "settings": {
        "tag": {
            "name": "animal present",
            "value": null
        },
        "condition": "with"
    }
}
```

</details>

<details>
  <summary>Without Tag with String value type</summary>

```json
{
    "action": "filter_video_by_tag",
    "src": [
        "$data_1"
    ],
    "dst": [
        "$filter_video_by_tag_2__true",
        "$filter_video_by_tag_2__false"
    ],
    "settings": {
        "tag": {
            "name": "object",
            "value": "car",
        },
        "condition": "without"
    }
}
```

</details>
