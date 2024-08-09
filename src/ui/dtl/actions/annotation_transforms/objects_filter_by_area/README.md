# Objects Filter by Area

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

### Example 1. Add tag by area pixel filter

In this example, we apply the `large_area` and `small_area` tags to objects in an image based on the pixel size of their bounding boxes. Specifically, we tag objects with bounding box areas greater than 10,000 pixels as `large_area` and those with areas less than or equal to 10,000 pixels as `small_area`.

- area_size: `10000px`
- comparator: `greater`
- action: `add_tags` -> `large_area`
>
- area_size: `10000px`
- comparator: `less`
- action: `add_tags` -> `small_area`

<table>
<tr>
<td style="text-align:center; width:50%"><strong>All objects</strong></td>
<td style="text-align:center; width:50%"><strong>Objects with tags by area that are less or greater 10,000 px</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/4654e696-8e99-4959-a025-f4b7c54c0e1f" alt="Original image" /> </td>
<td> <img src="https://github.com/user-attachments/assets/b67559da-dc7c-4e85-9596-9cb32b04d0b1" alt="Filtered objects" /> </td>
</tr>
</table>

### Example 2. Delete objects by area pixel filter

In this example we will delete annotations of classes that have area less than 10,000 pixels of image area.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>All objects</strong></td>
<td style="text-align:center; width:50%"><strong>Objects with area greater than 10,000 px</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/user-attachments/assets/7be58e15-f241-4053-825c-c06711cb7295" alt="Original image" /> </td>
<td> <img src="https://github.com/user-attachments/assets/0dd94609-17ce-4688-aa3e-bcaf15ceb7a5" alt="Filtered objects" /> </td>
</tr>
</table>

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
