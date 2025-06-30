from PIL import Image, ImageTk
import cv2
import numpy as np

# 裁剪透明边缘
def crop_transparent_edges(image_pil: Image.Image):
  # print(image_pil.mode)
  
  # arr = np.array(image_pil)
  # alpha = arr[:, :, 3]
  # print('alpha', alpha)
  # threshold = 50

  # mask = alpha < threshold 
  # print(not np.any(mask))
  # if not np.any(mask):
  #   return image_pil
  #   # return {
  #   #   "image": image_pil,
  #   #   "offset": (0, 0)
  #   # }
  
  bbox = image_pil.getbbox()
  if bbox:
    cropped = image_pil.crop(bbox)
    # cropped.show()
    return cropped
  else:
    return image_pil

  # return {
  #     "image": cropped,
  #     "offset": (x0, y0)
  # }

# 图片匹配
def match_template(big_image, small_image):
  result = crop_transparent_edges(small_image)
  cropped_img = result['image']
  offset_x, offset_y = result['offset']
  match_result = cv2.matchTemplate(
    cv2.cvtColor(np.array(big_image), cv2.COLOR_RGB2BGR),
    cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR),
    cv2.TM_CCOEFF_NORMED
  )
  in_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)

  return {
    "cropped_img": cropped_img,
    "x": max_loc[0] - offset_x,
    "y": max_loc[1] - offset_y
  }
  
# 可能需要裁剪的图片和psd中每个图层进行比较
# 用元组保存，匹配度和对应图层
# 最好返回匹配度最高的
def get_match_degree(big_image: Image.Image, small_image: Image.Image)-> float:
  match_result = cv2.matchTemplate(
    cv2.cvtColor(np.array(big_image), cv2.COLOR_RGB2BGR),
    cv2.cvtColor(np.array(small_image), cv2.COLOR_RGB2BGR),
    cv2.TM_CCOEFF_NORMED
  )
  
  
  in_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
  
  return max_val
  
  