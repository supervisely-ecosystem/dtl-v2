<div align="center" markdown>

<img src="https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/73838fba-d57b-4405-9db5-80e3514f9983"/>

# Data Nodes
  
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

| Layers                                                                                                                                                       | Description                                                 | Images | Videos |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|--------|--------|
| **Input**                                                                                                                                                    |                                                             |        |        |
| [Images Project](/src/ui/dtl/actions/input/images_project/README.md#images-project)                                                                          | Select a project with images to process.                    | +      | -      |
| [Videos Project](/src/ui/dtl/actions/input/videos_project/README.md#videos-project)                                                                          | Select a project with videos to process.                    | -      | +      |
| [Input Labeling Job](/src/ui/dtl/actions/input/input_labeling_job/README.md#input-labeling-job)                                                              | Select a labeling job to process.                           | +      | -      |
| **Pixel Level Transformations**                                                                                                                              |                                                             |        |        |
| [Anonymize](/src/ui/dtl/actions/pixel_level_transformations/anonymize/README.md#anonymize)                                                                   | Anonymize objects on data.                                  | +      | -      |
| [Blur](/src/ui/dtl/actions/pixel_level_transformations/blur/README.md#blur)                                                                                  | Blur data.                                                  | +      | -      |
| [Contrast Brightness](/src/ui/dtl/actions/pixel_level_transformations/contrast_brightness/README.md#contrast-and-brightness)                                 | Change contrast and brightness of data.                     | +      | -      |
| [Noise](/src/ui/dtl/actions/pixel_level_transformations/noise/README.md#noise)                                                                               | Add noise to data.                                          | +      | -      |
| [Random Color](/src/ui/dtl/actions/pixel_level_transformations/random_color/README.md#random-color)                                                          | Change colors of data.                                      | +      | -      |
| **Spatial Level Transformations**                                                                                                                            |                                                             |        |        |
| [Crop](/src/ui/dtl/actions/spatial_level_transforms/crop/README.md#crop)                                                                                     | Crop data.                                                  | +      | -      |
| [Flip](/src/ui/dtl/actions/spatial_level_transforms/flip/README.md#flip)                                                                                     | Flip data vertically or horizontally.                       | +      | -      |
| [Instance Crop](/src/ui/dtl/actions/spatial_level_transforms/instances_crop/README.md#instances-crop)                                                        | Crop instances in data.                                     | +      | -      |
| [Multiply](/src/ui/dtl/actions/spatial_level_transforms/multiply/README.md#multiply)                                                                         | Multiply objects.                                           | +      | -      |
| [Resize](/src/ui/dtl/actions/spatial_level_transforms/resize/README.md#resize)                                                                               | Resize data.                                                | +      | -      |
| [Rotate](/src/ui/dtl/actions/spatial_level_transforms/rotate/README.md#rotate)                                                                               | Rotate data.                                                | +      | -      |
| [Sliding Window](/src/ui/dtl/actions/spatial_level_transforms/sliding_window/README.md#sliding-window)                                                       | Apply sliding window to data.                               | +      | -      |
| **Annotation Transforms**                                                                                                                                    |                                                             |        |        |
| [Approximate Vector](/src/ui/dtl//actions/annotation_transforms/approx_vector/README.md#approx-vector)                                                       | Approximate vector objects.                                 | +      | -      |
| [Background](/src/ui/dtl//actions/annotation_transforms/background/README.md#background)                                                                     | Add background to data.                                     | +      | +      |
| [Bounding Box](/src/ui/dtl//actions/annotation_transforms/bbox/README.md#bounding-box)                                                                       | Convert object classes to bounding boxes.                   | +      | +      |
| [Bounding Box to Polygon](/src/ui/dtl//actions/annotation_transforms/bbox_to_polygon/README.md#bbox-to-polygon)                                              | Convert bounding boxes to polygons.                         | +      | +      |
| [Bitwise Masks](/src/ui/dtl//actions/annotation_transforms/bitwise_masks/README.md#bitwise-masks)                                                            | Bitwise operations on masks.                                | +      | -      |
| [Change Class Color](/src/ui/dtl//actions/annotation_transforms/change_class_color/README.md#change-class-color)                                             | Change color of the object class.                           | +      | -      |
| [Drop Lines by Length](/src/ui/dtl//actions/annotation_transforms/drop_lines_by_length/README.md#drop-lines-by-length)                                       | Remove lines by length.                                     | +      | -      |
| [Drop Noise](/src/ui/dtl//actions/annotation_transforms/drop_noise/README.md#drop-noise)                                                                     | Remove noise from masks.                                    | +      | -      |
| [Drop Object by Class](/src/ui/dtl//actions/annotation_transforms/drop_object_by_class/README.md#drop-object-by-class)                                       | Remove objects by class.                                    | +      | -      |
| [Duplicate Objects](/src/ui/dtl//actions/annotation_transforms/duplicate_objects/README.md#duplicate-objects)                                                | Duplicate objects.                                          | +      | -      |
| [Image Tag](/src/ui/dtl//actions/annotation_transforms/image_tag/README.md#image-tag)                                                                        | Add tag to data.                                            | +      | -      |
| [Line to Mask](/src/ui/dtl//actions/annotation_transforms/line_to_mask/README.md#line-to-mask)                                                               | Convert lines to masks.                                     | +      | -      |
| [Mask to Lines](/src/ui/dtl//actions/annotation_transforms/mask_to_lines/README.md#mask-to-lines)                                                            | Convert masks to lines.                                     | +      | -      |
| [Mask to Polygon](/src/ui/dtl//actions/annotation_transforms/mask_to_polygon/README.md#mask-to-polygon)                                                      | Convert masks to polygons.                                  | +      | -      |
| [Merge Masks](/src/ui/dtl//actions/annotation_transforms/merge_masks/README.md#merge-masks)                                                                  | Merge few masks of the same object class into a single one. | +      | -      |
| [Objects Filter](/src/ui/dtl//actions/annotation_transforms/objects_filter/README.md#objects-filter)                                                         | Filter data by objects.                                     | +      | -      |
| [Polygon to Mask](/src/ui/dtl//actions/annotation_transforms/polygon_to_mask/README.md#polygon-to-mask)                                                      | Convert polygons to masks.                                  | +      | -      |
| [Rasterize](/src/ui/dtl//actions/annotation_transforms/rasterize/README.md#rasterize)                                                                        | Rasterize objects.                                          | +      | -      |
| [Rename Classes](/src/ui/dtl//actions/annotation_transforms/rename_classes/README.md#rename-classes)                                                         | Rename object classes.                                      | +      | -      |
| [Skeletonize](/src/ui/dtl//actions/annotation_transforms/skeletonize/README.md#skeletonize)                                                                  | Skeletonize masks.                                          | +      | -      |
| [Split Masks](/src/ui/dtl//actions/annotation_transforms/split_masks/README.md#split-masks)                                                                  | Split masks.                                                | +      | -      |
| [Split Videos by Duration](/src/ui/dtl//actions/annotation_transforms/split_videos_by_duration/README.md#split-video-by-duration)                            | Split videos by duration.                                   | -      | +      |
| **Filters and Conditions**                                                                                                                                   |                                                             |        |        |
| [Filter Image by Object](/src/ui/dtl/actions/filters_and_conditions/filter_image_by_object/README.md#filter-images-by-object-classes)                        | Filter Image by Object.                                     | +      | -      |
| [Filter Image by Tag](/src/ui/dtl/actions/filters_and_conditions/filter_image_by_tag/README.md#filter-images-by-tags)                                        | Filter Image by Tag.                                        | +      | -      |
| [Filter Images without Objects](/src/ui/dtl/actions/filters_and_conditions/filter_images_without_objects/README.md#filter-images-without-object-classes)     | Filter Images without Objects.                              | +      | -      |
| [Filter Videos by Duration](/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_duration/README.md#filter-videos-by-duration)                        | Filter Videos by Duration.                                  | -      | +      |
| [Filter Videos by Objects](/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_objects/README.md#filter-videos-by-object-classes)                    | Filter Videos by Objects.                                   | -      | +      |
| [Filter Videos by Tags](/src/ui/dtl/actions/filters_and_conditions/filter_videos_by_tags/README.md#filter-videos-by-tags)                                    | Filter Videos by Tags.                                      | -      | +      |
| [Filter Videos without Annotations](/src/ui/dtl/actions/filters_and_conditions/filter_videos_without_annotation/README.md#filter-videos-without-annotations) | Filter Videos without Annotations.                          | -      | +      |
| [Filter Videos without Objects](/src/ui/dtl/actions/filters_and_conditions/filter_videos_without_objects/README.md#filter-videos-without-object-classes)     | Filter Videos without Objects.                              | -      | +      |
| [IF Action](/src/ui/dtl/actions/filters_and_conditions/if_action/README.md#if-action)                                                                        | Select one of the available conditions and filter data.     | +      | -      |
| **Neural Networks**                                                                                                                                          |                                                             |        |        |
| [Apply NN Inference](/src/ui/dtl/actions/neural_networks/apply_nn_inference/README.md#apply-nn-inference)                                                    | Apply neural network inference.                             | +      | -      |
| [Deploy YOLOv8](/src/ui/dtl/actions/neural_networks/deploy_yolov8/README.md#deploy-yolov8)                                                                   | Deploy pretrained or custom YOLOv8 model.                   | +      | -      |
| **Other**                                                                                                                                                    |                                                             |        |        |
| [Dummy](/src/ui/dtl/actions/other/dummy/README.md#dummy)                                                                                                     | Dummy node. Do nothing. Can be used to merge layers.        | +      | -      |
| [Dataset](/src/ui/dtl/actions/other/dataset/README.md#dataset)                                                                                               | All data will be put into a single dataset.                 | +      | -      |
| **Output**                                                                                                                                                   |                                                             |        |        |
| [Create new Project](/src/ui/dtl/actions/output/create_new_project/README.md#create-new-project)                                                             | Create a new project and save data there.                   | +      | +      |
| [Add to Existing Project](/src/ui/dtl/actions/output/add_to_existing_project/README.md#add-to-existing-project)                                              | Add data to an existing project or dataset.                 | +      | +      |
| [Export Archive](/src/ui/dtl/actions/output/export_archive/README.md#export-archive)                                                                         | Export data to TeamFiles as an archive.                     | +      | +      |
| [Export Archive with Masks](/src/ui/dtl/actions/output/export_archive_with_masks/README.md#export-archive-with-masks)                                        | Export data to TeamFiles as an archive with masks.          | +      | -      |
| [Copy Annotations](/src/ui/dtl/actions/output/copy_annotations/README.md#copy-annotations)                                                                   | Copy annotations from one project to another.               | +      | -      |
| [Create Labeling Job](/src/ui/dtl/actions/output/create_labeling_job/README.md#create-labeling-job)                                                          | Create a labeling job from data.                            | +      | +      |

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

There are several ways to run the application:

<details open>
<summary><b>1. Run App from Ecosystem</b></summary>

![run-from-ecosystem-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/4dc28226-74d6-4603-a282-bdb94270d893)

</details>

<details>
<summary><b>2. Run App from the context menu of the Project</b></summary>

![run-from-project-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/c92ecdc6-c038-4f86-880c-b974183dc6ab)

</details>

<details>
<summary><b>3. Run App from the context menu of the Dataset</b></summary>

![run-from-project-min]()

</details>

<details>
<summary><b>4. Run App from Filters</b></summary>

![run-from-project-min]()

</details>

<!-- <details open>
<summary><b>3. Run App from Team Files</b></summary>

![run-from-teamfiles-min](https://github.com/supervisely-ecosystem/data-nodes/assets/48913536/ae996fcb-b9e0-4b1a-a514-bfab1097b40d)

</details> -->
