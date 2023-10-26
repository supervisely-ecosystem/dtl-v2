# Rename Classes

`Rename Classes` layer change names of the existing classes with given class names.

### Settings

- **classes_mapping** — Select the classes to be renamed and specify the new names for them.

### Example

In this example we will change classes so that they are starting with a capital letter.

<details>
  <summary>JSON view</summary>
```json
{
    "action": "rename",
    "src": [
        "$data_12"
    ],
    "dst": "$rename_22",
    "settings": {
        "classes_mapping": {
            "cat": "Cat",
            "dog": "Dog",
            "horse": "Horse",
            "sheep": "Sheep",
            "squirrel": "Squirrel"
        }
    }
}
```
</details>
