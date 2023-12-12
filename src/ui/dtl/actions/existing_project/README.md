# Existing Project

`Existing Project` stores results of data transformations to existing project in your workspace. If the metadata of the project to which the saving is performed differs from the metadata of the project that has gone through the whole pipeline, then in this case you will be asked to confirm the merge of this data, the metadata of the project to which the saving is performed will take precedence.

### Settings

- **Select Dataset Options** 
    - **Existing Dataset** - select dataset from existing project to save results to
    - **New Dataset** - enter name of new dataset to create in selected project
    - **Keep source structure** - save the results in datasets that repeats datasets structure of the input project

### Example 1. Existing dataset

The results are saved to the selected dataset of an existing project.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Source datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: Existing dataset</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/15288079-77eb-4157-8242-9eee6f87b623" alt="Source project"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/19dead3a-2294-459e-995a-da03cc7532b7" alt="Existing project"/> </td>
</tr>
</table>

### Example 2. New dataset

You will create a new dataset to which all processed files will be saved. If a dataset with the same name exists in the destination project, then the created dataset will be renamed to the same name + `00N`, where `N` is autoincremented.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Source datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: New datset</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/15288079-77eb-4157-8242-9eee6f87b623" alt="Source project"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/e4475360-f444-4c0c-835b-34ed58ea6806" alt="Existing project"/> </td>
</tr>
</table>

### Example 3. Keep source structure

All files will be saved in the selected project in the same structure, with the same dataset names as were stored in the incoming project. If a dataset(s) with the same name exists in the destination project, then the created dataset will be renamed to the same name + `00N`, where `N` is autoincremented.

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Source datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: Keep source structure</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/15288079-77eb-4157-8242-9eee6f87b623" alt="Source project"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/data-nodes/assets/57998637/bce65308-7ca9-4a10-9bb0-0e0f4ca356f8" alt="Existing project"/> </td>
</tr>
</table>

### JSON views

<details>
  <summary>Existing dataset</summary>
  <pre>
    {
        "action": "existing_project",
        "src": ["$data_1 "],
        " dst ": "dst_project_name",
        " settings ": {
            " project_id ": 30496,
            " dataset_name ": null,
            " dataset_id ": 79016,
            " dataset_option ": " existing ",
            " merge_meta ": true
        }
    }
  </pre>
</details>

<details>
  <summary>New dataset</summary>
    <pre>
      {
          "action": "existing_project",
          "src": ["$data_1"],
          "dst": "dst_project_name",
          "settings": {
              "project_id": 30496,
              "dataset_name": "new_dataset",
              "dataset_id": null,
              "dataset_option": "new",
              "merge_meta": true
          }
      }
    </pre>
</details>

<details>
  <summary>Keep source structure</summary>
  <pre>
    {
        "action": "existing_project",
        "src": ["$data_1"],
        "dst": "dst_project_name",
        "settings": {
            "project_id": 30496,
            "dataset_name": null,
            "dataset_id": null,
            "dataset_option": "keep",
            "merge_meta": true
        }
    }
  </pre>
</details>
