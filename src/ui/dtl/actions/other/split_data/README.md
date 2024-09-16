# Split Data

`Split Data` splits the input data into datasets based on condition.

### Settings

There are 4 ways of splitting the data:

- **percent**: data will be split by the percentage of total images count.

- **number**: data will be split by amount of images.

- **classes**: data will be split based on the presence of objects of annotation classes. Please note that when using this method the final project will likely include more images than the input project.

- **tags**: data will be split based on the presence of image and object tags on the image. Please note that when using this method the final project will likely include more images than the input project.

### Example 1. Split Data by percentage

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: new datasets structure</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original datasets"/> </td>
<td> <img src="xxx" alt="Result datasets"/> </td>
</tr>
</table>

### Example 2. Instance crop & Split Data by classes

<table>
<tr>
<td style="text-align:center; width:50%"><strong>Original datasets</strong></td>
<td style="text-align:center; width:50%"><strong>Result: new datasets structure</strong></td>
</tr>
<tr>
<td> <img src="xxx" alt="Original datasets"/> </td>
<td> <img src="xxx" alt="Result datasets"/> </td>
</tr>
</table>

*in this instance, the amount of images more than doubled: the input project contained 953 images, and the output project contains 2213 images*

<details>
  <summary>JSON view</summary>
<pre>
  "action": "split_data",
  "src": {
    "source": [
      "$images_project_1"
    ]
  },
  "dst": "$split_data_2",
  "settings": {
    "split_method": "classes",
    "split_ratio": 50,
    "split_num": 50
  }
</pre>
</details>
