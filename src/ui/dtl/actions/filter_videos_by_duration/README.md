# Filter Video by Duration

`Filter Video by Duration` layer is used to filter videos by the duration.

# Settings

- **Minimum duration** - Minimum duration of the video to filter.
- **Maximum duration** - Maximum duration of the video to filter.
- **Duration unit** - Set duration in frames or seconds of the video.

### JSON views

<details>
  <summary>JSON View</summary>

```json
{
	"action": "filter_video_by_duration",
	"src": [
		"$data_1"
	],
	"dst": [
		"$filter_video_without_objects_2__true",
		"$filter_video_without_objects_2__false"
	],
	"settings": {
		"exclude_classes": [
			"car",
			"pedestrian"
		]
	}
},
```

</details>
