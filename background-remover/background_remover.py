from segment_anything import SamPredictor, sam_model_registry
import numpy as np
import cv2

def remove_background(image, x, y): 
    
    # create sam predictor
    model_path = './sam_vit_b_01ec64.pth'
    sam = sam_model_registry["vit_b"](checkpoint=model_path)
    predictor = SamPredictor(sam)

    # use sam predictor on (image, x, y) to get all masks for location of subject
    predictor.set_image(image)
    masks, scores, logits = predictor.predict(
                                    point_coords=np.asarray([[x, y]]),
                                    point_labels=np.asarray([1]),
                                    multimask_output=True
                                )
    
    C, H, W = masks.shape

    result_mask = np.zeros((H, W), dtype=bool)

    # iterate through all the masks and merge them. For a given point, you can get multiple masks (for person hair, face, scarf, entire person, etc)
    for j in range(C):
        result_mask |= masks[j, :, :]

    result_mask = result_mask.astype(np.uint8)

    # remove background
    # every pixel is white or black in alpha (1 channel), while in the original image there are 3 channels: red, green, blue
    alpha_channel = np.ones(result_mask.shape, dtype=result_mask.dtype) * 255

    alpha_channel[result_mask == 0] = 0

    result_image = cv2.merge((image, alpha_channel))

    return result_image

