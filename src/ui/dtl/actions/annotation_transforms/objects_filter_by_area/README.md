# Objects Filter

`Objects Filter by Area` layer allows filtering objects by area size. You can compare area size in pixels by `less` or `greater` comparison and apply one of the following actions: `delete`, `keep` or `add tags`.

### Settings

- **Classes** - Select classes to filter by area size.
- **Area size** - Object area in pixels.
- **Comparator** - Comparison type: `less` or `greater`.
- **Action** - Action to apply: `delete`, `keep` or `add tags`.
  - **delete** - Objects that meet the filter criteria will be deleted.
  - **keep** - Objects that meet the filter criteria will be kept, but all other objects will be deleted.
  - **add tags** - Objects that meet the filter criteria will be tagged with the specified tags, no objects will be deleted.
- **Tags** - If `add tags` action is selected, you can select tags that will added to filtered objects.

### Example

Example will be added soon.

### JSON views

<details>
  <summary>Json preview</summary>
<pre>
{
		"action": "objects_filter_by_area",
		"src": {
			"source": [
				"$images_project_1"
			]
		},
		"dst": "$objects_filter_by_area_2",
		"settings": {
			"classes": [
				"shirt",
				"bag"
			],
			"area": 18,
			"comparator": "gt",
			"action": "add_tags",
			"tags_to_add": [
				{
					"name": "some_tag_text",
					"value": "some text"
				},
				{
					"name": "some_tag_num",
					"value": 18
				},
				{
					"name": "some_tag_oneof",
					"value": "value_3"
				},
				{
					"name": "some_tag_none",
					"value": null
				}
			]
		},
		"scene_location": {
			"order_idx": 1,
			"position": {
				"x": 540,
				"y": 140
			}
		}
	}
</pre>
</details>
