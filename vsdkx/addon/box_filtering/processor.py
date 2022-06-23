from vsdkx.core.interfaces import Addon, AddonObject

import numpy as np
import torch
import torchvision


class BigBoxFilteringProcessor(Addon):
    """
    Filters out Big Bounding Boxes from frame
    depending on statistical analysis (Inter Quartile Range)
    """

    def __init__(self, addon_config: dict, model_settings: dict,
                 model_config: dict, drawing_config: dict):
        super().__init__(addon_config, model_settings, model_config,
                         drawing_config)

    def post_process(self, addon_object: AddonObject) -> AddonObject:
        """
        Computes Inter Quartile Range (IQR) on areas of bounding boxes
        and filters out any box that falls into upper bound

        IQR = Quartile3 – Quartile1 (Inter Quartile Range)
        Lower Bound: (Quartile1 - 1.5 * IQR)
        Upper Bound: (Quartile3 + 1.5 * IQR)

        Args:
            addon_object (AddonObject): addon object containing information
            about inference, frame, other addons shared data

        Returns:
            addon_object (AddonObject): same addon object that was passed
            but with filtered bounding boxes, confidence scores and classes
        """

        boxes = addon_object.inference.boxes
        scores = addon_object.inference.scores
        classes = addon_object.inference.classes

        # If only one or no boxes was detected, we don't have to do filtering
        if len(boxes) < 2:
            return addon_object

        areas = torchvision.ops.box_area(torch.tensor(boxes, dtype=torch.float)).cpu().detach().numpy()

        # compute IQR and get upper bound
        q1 = np.percentile(areas, 25, interpolation='midpoint')
        q3 = np.percentile(areas, 75, interpolation='midpoint')
        iqr = q3 - q1
        upper = areas > (q3 + 1.5 * iqr)

        addon_object.inference.boxes = list(np.array(boxes)[~upper])
        addon_object.inference.scores = list(np.array(scores)[~upper])
        addon_object.inference.classes = list(np.array(classes)[~upper])

        return addon_object
