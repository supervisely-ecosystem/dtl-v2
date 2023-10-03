# Rename

Layer renames existing classes with given class names.

### Settings

- **Select classes** (select classes to and input new names)

### Example

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
