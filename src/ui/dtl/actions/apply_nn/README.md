# Apply NN

`Apply NN` layer is used to apply a neural network to the input data. Layer connects to deployed model such as Serve YOLOv8 app.
You can connect to the model using `CONNECT` button. Once connected, you can configure model settings and select model classes and tags, which will be applied to your data.

<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAACYElEQVR4nO2VPW/TUBSG78LMH4AZiYEJ8ROQEFIxnTJQicGBRKBCL7YT5cMfpHXSUppCgc6MhQExsjCAKhADYyKhpEnsYBaEKDPooEuTyBib+BjsXIRf6RmOFPucx/cjhKRJk+b/yfkPcFZwYCg4AHFwzgFbcOBMbAKjBhAzVmwCCQwPjFQgKOkKOBxuoZPPWnBYfxiZU8/fJSAgt3aJ0vb9Wscfv4FD17cic+Lp218FlDYQufXy7wmwFwYIzA2/wunWfmTm7G/+AowkBGK5RpUEBaKcAb99L8xKIMoZ8Nv3wqwEopwBv30vpGfAE7O5vVvf3AZGRlz8QVKHODPqN+5vNh/gr1Rz4z6MmZWA6ZoBLbB8+x6MuZCjk5f68SdDZgJYyNNJfwb6X7e2vjVBMRq/lZh/3UUNP/+qM3X4gt74aYbw/86jG8dYuzuVaSsT5isbIfowwl+tox/qq3emImlmZImF/BLIaj1UH0Z4AbZMShvUxiZXkAOBF+HOASGkajaBJwg25ZUN4AmCTWl5HYIY2O+hbw1jq0s+oAWKtVsQRM8aQm9gx1YXfUALFIw14AmCjayvAk8QbCStAV7YUu8N7MRqyQVagFbr4GWvb0O3byVWUxdogaWKCTxBsLlWXgGeINgslmoQBNunbKndNTbe57uu2g+0wNXiTQii07Og0xtMatYcG/fzHc/7/EALXCkYwBMEm7yifckrOnCBrH1GC1yW1Cc5SQM+UHfQAjm5cixL1U+XbqgwS7JU/Sgq2hESJRdp+ahIK49EWtnP0iokiXjQcyfy8GnSpCH/RL4DrnKIm4kYFH8AAAAASUVORK5CYII=" style="height: 15px"> Read our post on [Supervisely blog](https://supervisely.com/blog/) to learn how to effectively train and use the deployed model on the YOLOv8 example: [No-code tutorial: train and predict YOLOv8 on custom data](https://supervisely.com/blog/train-yolov8-on-custom-data-no-code/).

Supported models:

- :white_check_mark:[YOLOv5](/ecosystem/apps/yolov5/supervisely/serve)
- :white_check_mark:[YOLOv5 2.0](/ecosystem/apps/yolov5_2.0/serve)
- :white_check_mark:[YOLOv8](/ecosystem/apps/yolov8/serve)
- :white_check_mark:[MMSegmentation](/ecosystem/apps/mmsegmentation/serve)
- :white_check_mark:[MMDetection](/ecosystem/apps/mmdetection/serve)
- :white_check_mark:[MMDetection 3.0](/ecosystem/apps/serve-mmdetection-v3)
- :white_check_mark:[Detectron2](/ecosystem/apps/detectron2/supervisely/instance_segmentation/serve)
- :white_check_mark:[UNet](/ecosystem/apps/unet/supervisely/serve)

### Settings:

- **Connect to Model** - Select the deployed model that will be applied to the data.
- **Сlasses** - Choose model classes that will be labeled on the data. If no classes are selected, no classes will be labeled.
- **Tags** - Choose model tags that will be assigned to the labeled objects. If no tags are selected, no tags will be assigned.
- **Class / Tag name suffix** - Suffix that will be added to the class / tag name if it have conflict with existing class / tag in the project. For example, if the input project has existing class with name `person` and the suffix is `model`, the resulting class name will be `person-model`.
- **Model Settings**
  - **Always use suffix** - If enabled, the suffix will be added to the class / tag name even if there is no conflict.
  - **Resolve conflict method** - Method that will be used to resolve conflict between existing class / tag and the class / tag that will be added by the layer. Available methods:
    - **Merge** - Merge predicted annotation with the existing one.
    - **Replace** - Replace the existing annotation with the one predicted by the model. All existing annotations will be removed.
  - **Inference settings** - Model specific settings in `YAML` format
  - **Apply method** - Method that will be used to apply the model to the data. Available methods:
    - **Full Image** - Model will be applied to the full image.
    - **ROI** - Model will be applied only for ROIs defined by object's bounding box (Coming Soon).
    - **Sliding Window** - Model will be applied to image using sliding window approach (Coming Soon).

<table>
<tr>
<td style="text-align:center; width:33%"><strong>Original image</strong></td>
<td style="text-align:center; width:33%"><strong>YOLOv5 applied (Object Detection)</strong></td>
<td style="text-align:center; width:33%"><strong>YOLOv8 applied (Instance Segmentation)</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/86b76053-a3c4-4d9e-bcbc-c56067c12fdd" alt="Original image" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/e75df2ad-90c7-4e89-b8ab-3c10ad48d17b" alt="YOLOv5 applied (Object Detection)" /> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/9e6cdad4-254b-41f5-a95d-a2e5bea70d15" alt="YOLOv8 applied (Instance Segmentation)" /> </td>
</tr>
</table>

### Examples

<details>
  <summary>JSON view</summary>
<pre>
{
	"action": "apply_nn",
	"src": [
		"$data_1"
	],
	"dst": "$apply_nn_2",
	"settings": {
		"current_meta": {
			"classes": [],
			"tags": []
		},
		"session_id": 47491,
		"model_info": {
			"app_name": "Serve YOLOv8",
			"session_id": 47491,
			"number_of_classes": 80,
			"sliding_window_support": "basic",
			"videos_support": true,
			"async_video_inference_support": true,
			"tracking_on_videos_support": true,
			"async_image_inference_support": true,
			"task type": "object detection"
		},
		"model_meta": {
			"classes": [
				{
					"title": "person",
					"shape": "rectangle",
					"color": "#0F718A",
					"geometry_config": {},
					"hotkey": ""
				},
				{
					"title": "bicycle",
					"shape": "rectangle",
					"color": "#0F148A",
					"geometry_config": {},
					"hotkey": ""
				},
				{
					"title": "car",
					"shape": "rectangle",
					"color": "#8A500F",
					"geometry_config": {},
					"hotkey": ""
				},
                		...
                		...
                		...
				{
					"title": "toothbrush",
					"shape": "rectangle",
					"color": "#8A0F52",
					"geometry_config": {},
					"hotkey": ""
				}
			],
			"tags": [
				{
					"name": "confidence",
					"value_type": "any_number",
					"color": "#0F478A",
					"hotkey": "",
					"applicable_type": "all",
					"classes": []
				}
			]
		},
		"model_settings": {
			"conf": 0.25,
			"iou": 0.7,
			"half": false,
			"max_det": 300,
			"agnostic_nms": false,
			"point_threshold": 0.1
		},
		"model_suffix": "model",
		"model_conflict": "replace",
		"use_model_suffix": true,
		"apply_method": "image",
		"classes": [
			"person",
            "car",
            "sheep",
            "dog",
            "cat",
		],
		"tags": [
			"confidence"
		]
	}
}
</pre>
</details>
