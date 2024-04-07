import os
from base_dir import BASE_DIR

def make_dir():
  os.system(
    f"cd {BASE_DIR} && mkdir inputs && cd inputs && mkdir test && cd test && mkdir cloth cloth-mask image image-parse openpose-img openpose-json"
    )
  os.system(
    f"cd {BASE_DIR} && mkdir output"
    )