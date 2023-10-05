# Objects Filter

`Objects Filter` layer deletes annotations less (or greater) than specified size or percentage of image area.

### Settings

Objects can be filtered in 3 ways: by class names, by area percentage and by bounding box size.

#### Option 1 Name filter

- **filter_by** - key to specify filters
  - **names** - list of classes to filter

<details>
  <summary>Case: names</summary>

Delete annotations of classes which not present in names.

```json
{
  "action": "objects_filter",
  "src": ["$data_1"],
  "dst": "$sample2",
  "settings": {
    "filter_by": {
      "names": ["Class A", "Class C"]
    }
  }
}
```

</details>

#### Option 2 Area percent filter

- **filter_by** - key to specify filters
  - **polygon_sizes** - key to specify size or percentage to filter by
    - **filtering_classes** - list of classes to filter
    - **action** - action to perform, only "delete" is supported
    - **comparator** - type of comparison, "less" or "greater"
    - **area_size** - key to specify area size to filter by
      - **percent** - percentage of image area that annotation should have to be considered

<details>
  <summary>Case: area percent</summary>

Delete annotations of classes from filtering_classes that have area (in percentage of image area) less than specified value of area_size.

Use comparator = greater to delete annotations which area is greater than defined.

```json
{
  "action": "objects_filter",
  "src": ["$data_1"],
  "dst": "$sample2",
  "settings": {
    "filter_by": {
      "polygon_sizes": {
        "filtering_classes": ["person"],
        "area_size": {
          "percent": 5
        },
        "action": "delete",
        "comparator": "less"
      }
    }
  }
}
```

</details>

#### Option 3 Bounding box size filter

- **filter_by** - key to specify filters
  - **polygon_sizes** - key to specify size or percentage to filter by
    - **filtering_classes** - list of classes to filter
    - **action** - action to perform, only "delete" is supported
    - **comparator** - type of comparison, "less" or "greater"
    - **area_size** - key to specify area size to filter by
      - **width** - label bounding box width, less (or greater)
      - **height** - label bounding box height, less (or greater)

<details>
  <summary>Case: bounding box size</summary>

Delete annotations of classes from filtering_classes that have some side (determined by the annotation bounding box) less than specified value of width or height correspondingly.

Use comparator = greater to delete annotations which some side is greater than defined.

```json
{
  "action": "objects_filter",
  "src": ["$data_1"],
  "dst": "$sample2",
  "settings": {
    "filter_by": {
      "polygon_sizes": {
        "filtering_classes": ["person"],
        "area_size": {
          "width": 10,
          "height": 40
        },
        "action": "delete",
        "comparator": "less"
      }
    }
  }
}
```

</details>
