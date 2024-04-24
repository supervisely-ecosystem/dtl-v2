# Move

`Move` layer move items from the source to the destination. Items in the source will be removed after the move operation is completed.

### Settings

<details>
  <summary>JSON view</summary>
<pre>
  {
    "action": "move",
    "src": [
      "$filtered_project_1"
    ],
    "dst": "$move_2",
    "settings": {
      "move_confirmation": true
    }
  },
</pre>
</details>
