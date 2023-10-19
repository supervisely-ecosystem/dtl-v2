# Supervisely

`Supervisely` layer stores results of data transformations to a new project in your workspace. Remember that you should specify a unique name to your output project.

### Settings

- **settings** - `Supervisely` layer don't need any settings so just leave this field blank.

<details>
  <summary>JSON view</summary>

```json
{
  "action": "supervisely",
  "src": ["$data_1"],
  "dst": "output_project",
  "settings": {}
}
```

</details>
