# Box Filtering

*No addon config required*

This add on computes the **Inter Quartile Range** on bounding box areas after the model inference (`post_process`) 
and filters out boxes that fall in upper bound.

```
IQR = Quartile3 – Quartile1 (Inter Quartile Range)
Lower Bound: (Quartile1 - 1.5 * IQR)
Upper Bound: (Quartile3 + 1.5 * IQR)
```

This addon has been implemented as workaround to object detectors that were trained on data that annotate multiple objects with one big bounding box (incorrect annotations). 

# Debug
Example of object initialization and `post_process` execution:
```python
from vsdkx.addon.box_filtering.processor import BigBoxFilteringProcessor
addon_on_config = {
  'class': 'vsdkx.addon.box_filtering.processor.BigBoxFilteringProcessor'
  }
model_config = {
    'classes_len': 1, 
    'filter_class_ids': [0], 
    'input_shape': [640, 640], 
    'model_path': 'vsdkx/weights/ppl_detection_retrain_training_2.pt'
    }
    
 model_settings = {
    'conf_thresh': 0.5, 
    'device': 'cpu', 
    'iou_thresh': 0.4
    }
box_filter_processor = BigBoxFilteringProcessor(addon_on_config, model_settings, model_config)
#post_process execution 
 addon_object = AddonObject(
    frame=np.array(RGB image), #Required RGB image in numpy format
    inference=dict{
                boxes=[array([2007,  608, 3322, 2140]), array([ 348,  348, 2190, 2145])], 
                classes=[array([0], dtype=object), array([0], dtype=object)], 
                scores=[array([0.799637496471405], dtype=object), array([0.6711544394493103], dtype=object)], 
                extra={}}, 
    shared={}
    )
 addon_object = box_filter_processor.post_process(addon_object)
 ```
This step updates the `addon_object.inference.boxes`, `addon_object.inference.scores` and `addon_object.inference.classes` with the filtered bounding boxes, scores and classes. 

 
