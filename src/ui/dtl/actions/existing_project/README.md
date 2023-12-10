# Existing Project

`Existing Project` stores results of data transformations to existing project in your workspace.

### Settings

- **Save options** 
  - **To existing dataset** - choose dataset
  - **Create new dataset** - select name for dataset
  - **Save original datasets structure** - just watch

### Example 1. To existing dataset

Some text

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: keep original datsets structure</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/63a72eec-6851-4e5d-9067-37a0b0e387b5" alt="Original datasets"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/5bc9dee2-3ae7-4f41-8945-927c039c611e" alt="Result datasets"/> </td>
</tr>
</table>

### Example 2. Create new dataset

Some text


<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: set new dataset name</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/63a72eec-6851-4e5d-9067-37a0b0e387b5" alt="Original datasets"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/91af2e74-d5e9-4b4e-b3c4-3248f99ffb12" alt="Result datasets"/> </td>
</tr>
</table>

### Example 3. Copy original datasets structure

Some text

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: keep original datsets structure</strong></td>
</tr>
<tr>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/63a72eec-6851-4e5d-9067-37a0b0e387b5" alt="Original datasets"/> </td>
<td> <img src="https://github.com/supervisely-ecosystem/ml-nodes/assets/79905215/5bc9dee2-3ae7-4f41-8945-927c039c611e" alt="Result datasets"/> </td>
</tr>
</table>

### JSON views

<details>
  <summary>To existing dataset</summary>
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
  <summary>Create new dataset</summary>
<pre>
{
  "action": "dataset",
  "src": ["$if_9__true"],
  "dst": "$dataset_10",
  "settings": {
    "name": "cats and dogs dataset"
  }
}
</pre>
</details>

<details>
  <summary>Copy original datasets structure</summary>
<pre>
{
  "action": "dataset",
  "src": ["$if_9__true"],
  "dst": "$dataset_10",
  "settings": {
    "name": "cats and dogs dataset"
  }
}
</pre>
</details>
