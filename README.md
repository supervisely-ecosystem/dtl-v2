<div align="center" markdown>

<img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/73838fba-d57b-4405-9db5-80e3514f9983"/>

# ML Pipelines
  
<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/data-nodes)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/data-nodes)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/data-nodes.png)](https://supervisely.com)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/data-nodes.png)](https://supervisely.com)

</div>

## Overview

This application is a versatile tool designed for data transformation tasks (like filtering and augmentation). It allows you to create and manage Data transformation workflows by leveraging graphical nodes with settings.

## Available Layers

| Layers                                                                                                                                                                                                                      | Description                                                 | Images | Videos |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|--------|--------|
| **Input**                                                                                                                                                                                                                   |                                                             |        |        |
| [Images Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/input/images_project/README.md#images-project)                                                                          | Select a project with images to process.                    | +      | -      |
| [Videos Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/input/videos_project/README.md#videos-project)                                                                          | Select a project with videos to process.                    | -      | +      |
| [Input Labeling Job](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/input/input_labeling_job/README.md#input-labeling-job)                                                              | Select a labeling job to process.                           | +      | -      |
| [Filtered Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/input/filtered_project/README.md#filtered-project)                                                                    | Predefined project with filtered images.                    | +      | -      |
| **Pixel Level Transformations**                                                                                                                                                                                             |                                                             |        |        |
| [Anonymize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/pixel_level_transformations/anonymize/README.md#anonymize)                                                                   | Anonymize objects on data.                                  | +      | -      |
| [Blur](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/pixel_level_transformations/blur/README.md#blur)                                                                                  | Blur data.                                                  | +      | -      |
| [Contrast Brightness](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/pixel_level_transformations/contrast_brightness/README.md#contrast-and-brightness)                                 | Change contrast and brightness of data.                     | +      | -      |
| [Noise](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/pixel_level_transformations/noise/README.md#noise)                                                                               | Add noise to data.                                          | +      | -      |
| [Random Color](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/pixel_level_transformations/random_color/README.md#random-color)                                                          | Change colors of data.                                      | +      | -      |
| **Spatial Level Transformations**                                                                                                                                                                                           |                                                             |        |        |
| [Crop](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/crop/README.md#crop)                                                                                     | Crop data.                                                  | +      | -      |
| [Flip](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/flip/README.md#flip)                                                                                     | Flip data vertically or horizontally.                       | +      | -      |
| [Instance Crop](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/instances_crop/README.md#instances-crop)                                                        | Crop instances in data.                                     | +      | -      |
| [Multiply](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/multiply/README.md#multiply)                                                                         | Multiply objects.                                           | +      | -      |
| [Resize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/resize/README.md#resize)                                                                               | Resize data.                                                | +      | -      |
| [Rotate](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/rotate/README.md#rotate)                                                                               | Rotate data.                                                | +      | -      |
| [Sliding Window](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/spatial_level_transforms/sliding_window/README.md#sliding-window)                                                       | Apply sliding window to data.                               | +      | -      |
| **ImgAug Augmentations**                                                                                                                                                                                                    |                                                             |        |        |
| [ImgAug.ImgCorruptlike Noise](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/corruptlike/noise.md)                                                                          | ImgAug imgcorruptlike Noise augmentators.                   | +      | -      |
| [ImgAug.ImgCorruptlike Blur](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/corruptlike/blur.md)                                                                            | ImgAug imgcorruptlike Blur augmentators.                    | +      | -      |
| [ImgAug.ImgCorruptlike Weather](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/corruptlike/weather.md)                                                                      | ImgAug imgcorruptlike Weather augmentators.                 | +      | -      |
| [ImgAug.ImgCorruptlike Color](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/corruptlike/color.md)                                                                          | ImgAug imgcorruptlike Color augmentators.                   | +      | -      |
| [ImgAug.ImgCorruptlike Compression](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/corruptlike/compression.md)                                                              | ImgAug imgcorruptlike Compression augmentators.             | +      | -      |
| [ImgAug.Geometric Elastic Transformation](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/imgaug_augs/geometric/elastic_transformation/README.md#pixelate)                               | ImgAug geometric Elastic Transformation augmentator.        | +      | -      |
| **Annotation Transforms**                                                                                                                                                                                                   |                                                             |        |        |
| [Approximate Vector](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/approx_vector/README.md#approx-vector)                                                       | Approximate vector objects.                                 | +      | -      |
| [Background](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/background/README.md#background)                                                                     | Add background to data.                                     | +      | +      |
| [Bounding Box](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/bbox/README.md#bounding-box)                                                                       | Convert object classes to bounding boxes.                   | +      | +      |
| [Bounding Box to Polygon](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/bbox_to_polygon/README.md#bbox-to-polygon)                                              | Convert bounding boxes to polygons.                         | +      | +      |
| [Bitwise Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/bitwise_masks/README.md#bitwise-masks)                                                            | Bitwise operations on masks.                                | +      | -      |
| [Change Class Color](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/change_class_color/README.md#change-class-color)                                             | Change color of the object class.                           | +      | -      |
| [Drop Lines by Length](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/drop_lines_by_length/README.md#drop-lines-by-length)                                       | Remove lines by length.                                     | +      | -      |
| [Drop Noise](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/drop_noise/README.md#drop-noise)                                                                     | Remove noise from masks.                                    | +      | -      |
| [Drop Object by Class](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/drop_object_by_class/README.md#drop-object-by-class)                                       | Remove objects by class.                                    | +      | -      |
| [Duplicate Objects](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/duplicate_objects/README.md#duplicate-objects)                                                | Duplicate objects.                                          | +      | -      |
| [Image Tag](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/image_tag/README.md#image-tag)                                                                        | Add tag to data.                                            | +      | -      |
| [Line to Mask](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/line_to_mask/README.md#line-to-mask)                                                               | Convert lines to masks.                                     | +      | -      |
| [Mask to Lines](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/mask_to_lines/README.md#mask-to-lines)                                                            | Convert masks to lines.                                     | +      | -      |
| [Mask to Polygon](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/mask_to_polygon/README.md#mask-to-polygon)                                                      | Convert masks to polygons.                                  | +      | -      |
| [Merge Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/merge_masks/README.md#merge-masks)                                                                  | Merge few masks of the same object class into a single one. | +      | -      |
| [Objects Filter](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/objects_filter/README.md#objects-filter)                                                         | Filter data by objects.                                     | +      | -      |
| [Polygon to Mask](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/polygon_to_mask/README.md#polygon-to-mask)                                                      | Convert polygons to masks.                                  | +      | -      |
| [Rasterize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/rasterize/README.md#rasterize)                                                                        | Rasterize objects.                                          | +      | -      |
| [Rename Classes](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/rename_classes/README.md#rename-classes)                                                         | Rename object classes.                                      | +      | -      |
| [Skeletonize](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/skeletonize/README.md#skeletonize)                                                                  | Skeletonize masks.                                          | +      | -      |
| [Split Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/split_masks/README.md#split-masks)                                                                  | Split masks.                                                | +      | -      |
| [Split Videos by Duration](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl//actions/annotation_transforms/split_videos_by_duration/README.md#split-video-by-duration)                            | Split videos by duration.                                   | -      | +      |
| **Filters and Conditions**                                                                                                                                                                                                  |                                                             |        |        |
| [Filter Image by Object](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_image_by_object/README.md#filter-images-by-object-classes)                        | Filter Image by Object.                                     | +      | -      |
| [Filter Image by Tag](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_image_by_tag/README.md#filter-images-by-tags)                                        | Filter Image by Tag.                                        | +      | -      |
| [Filter Images without Objects](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_images_without_objects/README.md#filter-images-without-object-classes)     | Filter Images without Objects.                              | +      | -      |
| [Filter Videos by Duration](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_duration/README.md#filter-videos-by-duration)                        | Filter Videos by Duration.                                  | -      | +      |
| [Filter Videos by Objects](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_objects/README.md#filter-videos-by-object-classes)                    | Filter Videos by Objects.                                   | -      | +      |
| [Filter Videos by Tags](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_tags/README.md#filter-videos-by-tags)                                    | Filter Videos by Tags.                                      | -      | +      |
| [Filter Videos without Annotations](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_videos_without_annotation/README.md#filter-videos-without-annotations) | Filter Videos without Annotations.                          | -      | +      |
| [Filter Videos without Objects](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/filter_videos_without_objects/README.md#filter-videos-without-object-classes)     | Filter Videos without Objects.                              | -      | +      |
| [IF Action](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/filters_and_conditions/if_action/README.md#if-action)                                                                        | Select one of the available conditions and filter data.     | +      | -      |
| **Neural Networks**                                                                                                                                                                                                         |                                                             |        |        |
| [Apply NN Inference](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/neural_networks/apply_nn_inference/README.md#apply-nn-inference)                                                    | Apply neural network inference.                             | +      | -      |
| [Deploy YOLOv8](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/neural_networks/deploy_yolov8/README.md#deploy-yolov8)                                                                   | Deploy pretrained or custom YOLOv8 model.                   | +      | -      |
| [Deploy MMDetection](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/neural_networks/deploy_mmdetection/README.md#deploy-mmdetection)                                                    | Deploy pretrained or custom MMDetection model.              | +      | -      |
| **Other**                                                                                                                                                                                                                   |                                                             |        |        |
| [Dummy](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/other/dummy/README.md#dummy)                                                                                                     | Dummy node. Do nothing. Can be used to merge layers.        | +      | -      |
| [Dataset](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/other/dataset/README.md#dataset)                                                                                               | All data will be put into a single dataset.                 | +      | -      |
| **Output**                                                                                                                                                                                                                  |                                                             |        |        |
| [Output Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/output_project/README.md#output_project)                                                                         | Save data to a new or existing project.                     | +      | -      |
| [Create new Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/create_new_project/README.md#create-new-project)                                                             | Create a new project and save data there.                   | +      | +      |
| [Add to Existing Project](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/add_to_existing_project/README.md#add-to-existing-project)                                              | Add data to an existing project or dataset.                 | +      | +      |
| [Export Archive](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/export_archive/README.md#export-archive)                                                                         | Export data to TeamFiles as an archive.                     | +      | +      |
| [Export Archive with Masks](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/export_archive_with_masks/README.md#export-archive-with-masks)                                        | Export data to TeamFiles as an archive with masks.          | +      | -      |
| [Copy Annotations](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/copy_annotations/README.md#copy-annotations)                                                                   | Copy annotations from one project to another.               | +      | -      |
| [Create Labeling Job](https://github.com/supervisely-ecosystem/data-nodes/blob/master/src/ui/dtl/actions/output/create_labeling_job/README.md#create-labeling-job)                                                          | Create a labeling job from data.                            | +      | +      |

#### Key features:

- **Transform Data:** Apply a wide variety of data transformation operations to images within a project. These transformations include rotation, cropping, blurring, resizing, and many more.

  ![transform-data](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/58d857fe-91af-413b-995b-20c674d72a9f)

- **Use Neural Networks:** Apply deployed models on your data to perform object detection, instance segmentation, and other tasks. You can use any of the neural network models available in the Supervisely Ecosystem, or train your custom models.
  
  ![apply-nn](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/9f715cf2-9106-47d0-bda3-500d2508f3b8)

- **Enhance Data:** Improve the quality and usability of your image data by adjusting contrast, brightness, and noise levels.

- **Object-Level Manipulation:** Perform operations on individual objects or instances within images, such as cropping, duplicating, or changing their color classes.

  ![object-transforms](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/34294f35-b720-4941-9e19-5fce70be9c33)

- **Customize Workflows:** Create complex data transformation workflows by combining multiple transformation nodes to meet your specific requirements.

- **Node Documentation:** Detailed documentation is available for each transformation node, explaining how to use it effectively. These guides provide step-by-step instructions and examples for each node, making it easy for users to understand and leverage the full power of the application.

  ![node-docs](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/6d5d1c8a-9a72-4827-9869-714b98b2e418)

- **Save & Load Presets:** Save your customized transformation workflows as presets for future use. This feature allows you to store and reuse your preferred configurations quickly.

  ![load-preset](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/5cd9ebb7-0fd5-4901-a1d3-9ecee38b629f)

- **Output Flexibility:** Choose from multiple export options to save your transformed data in a format that best suits your needs.

  ![merge-projects](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/1baaedff-3d02-46bb-a307-d690036509d2)

## How To Run

There are several ways to run the application, depending on your needs and preferences:

<details open>
<summary><b>1. Run App from Ecosystem</b></summary>

![run-from-ecosystem](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/f9d5ab6d-68e0-40d4-96a4-571eea41a383)

</details>

<details>
<summary><b>2. Run App from the context menu of the Project</b></summary>

![run-from-project](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/1df4ad60-4969-4c2a-b2bb-6cb9032fa13c)

</details>

<details>
<summary><b>3. Run App from the context menu of the Dataset</b></summary>

![run-from-dataset](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/ec9b955e-8abc-4908-821c-768eb7bcdd68)

</details>

<details>
<summary><b>4. Run Pipeline from Project</b></summary>

![run-pipeline-from-project](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/0bbf3f31-2a03-4f7c-b8a1-38eeaa314a99)

</details>

<details>
<summary><b>5. Run Pipeline from Dataset</b></summary>

![run-pipeline-from-dataset](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/0a2da1c9-97ae-4d44-b087-f24657fb0370)

</details>

<details>
<summary><b>6. Run Pipeline with Filters</b></summary>

![run-pipeline-from-filters](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/1bf0e32c-8af7-44f5-8fa8-921320cedb95)

</details>

<!-- <details open>
<summary><b>3. Run App from Team Files</b></summary>

![run-from-teamfiles-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/ae996fcb-b9e0-4b1a-a514-bfab1097b40d)

</details> -->
