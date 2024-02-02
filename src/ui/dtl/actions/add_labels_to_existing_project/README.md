# Add Labels to Existing Project

`Add Labels to Existing Project` is a `save` node that adds only labels from the input project to the target project by matching the dataset and image names. Any modifications to the images will not be applied to the target project images.

### How to use:

* **When Datasets and Images Match by Name:** If there's an image in your target project that shares its name with an image from the input project, what happens next depends on your chosen settings. You can either add new labels to the existing image in the target project or replace its current labels with the ones from the input project.

* **Matching Images by Name Only:** If both the input and target projects are working with a single dataset (either because they only contain one or you've selected just one), then images will be matched and processed based solely on their names.

* **What Happens to Unmatched Images:** If an image from the input project doesn't have a matching name in the target project, it will not be processed.

* **Handling Images of Different Sizes:** If two images share the same name across the input and target projects but differ in size, the node will not process them.

* **Modifying Existing Annotations:** If you're using layers that modify labels or image size, the node will automatically adjust annotation to fit the size of the original image in the target project.

* **Dealing with Duplicate Projects and the 'Replace' Option:** If you have two input projects that contain the same dataset names and identical images, and you choose the 'replace' option, the labels from the second project will overwrite the labels from the first project in the target project. We don't recommend using the 'replace' option in this case.

### Settings

- **Select project** - select the target project and dataset(s):
    - `Project` - select the project
    - `Select all datasets` - if this option is enabled, all datasets from the selected project will be used
    - `Dataset` - select one or more datasets from the selected project
- **Select how to add labels** - select how to add labels to the project. Option `Replace` will replace the labels in the target project with the labels from the source project. Option `Merge` will merge the labels from the source project and the target project.
- **Backup target project** - if this option is enabled, the target project will be backed up before the transformation process starts

### JSON views

<details>
  <summary>JSON Preview</summary>
  <pre>
{
	"action": "add_labels_to_existing_project",
	"src": [
		"$data_1"
	],
	"dst": "34747",
	"settings": {
		"project_id": 34747,
		"dataset_ids": [
			84993
		],
		"add_option": "merge",
		"backup_target_project": true
	}
}
  </pre>
</details>
