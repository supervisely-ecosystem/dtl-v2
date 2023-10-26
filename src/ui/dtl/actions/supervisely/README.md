# New Project

`New Project` layer stores results of data transformations to a new project in your workspace. Remember that you should specify a name to your output project.

> `New Project` layer doesn't need any other settings (just result project name).

### Settings

- **settings** - `New Project` layer don't need any settings so just leave this field blank.

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
