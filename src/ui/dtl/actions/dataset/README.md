# Dataset

`Dataset` layer places every image that it sees to the dataset with a specified name.

### Settings

- **rule** — rule for dataset creation. Possible values: `save_original`. If `save_original` is selected, then dataset will keep it's original name.
- **name** — name of the dataset.

Use only `rule` or only `name` field.

### Example. Split dataset by classes

In this example we used `If` layer to split images by classes and `Dataset` layer to save them to different datasets.
For `whale` class dataset name will be `whales`, for other classes dataset name will use `save_original` rule and original dataset name will be preserved.

![dataset](https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/653b46ab-2627-40eb-86ce-c1bf821d2f08)

### JSON views

<details>
  <summary>save original dataset name</summary>
<pre>
{
  "action": "dataset",
  "src": ["$if_9__true"],
  "dst": "$dataset_10",
  "settings": {
    "rule": "save_original"
  }
}
</pre>
</details>

<details>
  <summary>set new dataset name</summary>
<pre>
{
  "action": "dataset",
  "src": ["$if_9__true"],
  "dst": "$dataset_10",
  "settings": {
    "name": "whales"
  }
}
</pre>
</details>
