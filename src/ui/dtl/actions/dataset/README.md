# Dataset

`Dataset` layer places every image that it sees to the dataset with a specified name.

### Settings

**rule** — rule for dataset creation. Possible values: `save_original`. If `save_original` is selected, then dataset will keep it's original name. Use only `rule` or only `name` field.
**name** — name of the dataset. Use only `rule` or only `name` field.

<details>
  <summary>JSON view</summary>

```json
{
  "action": "dataset",
  "src": ["$data_1"],
  "dst": "$dataset_2",
  "settings": {
    "name": "New Dataset"
  }
}
```

</details>
