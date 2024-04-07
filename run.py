from PIL import Image
import os

from base_dir import BASE_DIR, REPO_DIR


# running the preprocessing

def resize_img(path):
    im = Image.open(path)
    im = im.resize((768, 1024))
    im.save(path)


for path in os.listdir(f'{BASE_DIR}/inputs/test/cloth/'):
    resize_img(f'{BASE_DIR}/inputs/test/cloth/{path}')

os.chdir(f'{REPO_DIR}')
os.system(f"rm -rf {BASE_DIR}/inputs/test/cloth/.ipynb_checkpoints")
os.system(f"python cloth-mask.py")
os.chdir(f'{BASE_DIR}')
os.system(f"python {REPO_DIR}/remove_bg.py")
os.system(f"python3 {BASE_DIR}/Self-Correction-Human-Parsing/simple_extractor.py --dataset 'lip' --model-restore '{BASE_DIR}/Self-Correction-Human-Parsing/checkpoints/final.pth' --input-dir '{BASE_DIR}/inputs/test/image' --output-dir '{BASE_DIR}/inputs/test/image-parse'")
os.chdir(f'{BASE_DIR}')
os.system(f"cd openpose && ./build/examples/openpose/openpose.bin --image_dir {BASE_DIR}/inputs/test/image/ --write_json {BASE_DIR}/inputs/test/openpose-json/ --display 0 --render_pose 0 --hand")
os.system(f"cd openpose && ./build/examples/openpose/openpose.bin --image_dir {BASE_DIR}/inputs/test/image/ --display 0 --write_images {BASE_DIR}/inputs/test/openpose-img/ --hand --render_pose 1 --disable_blending true")

model_image = os.listdir(f'{BASE_DIR}/inputs/test/image')
cloth_image = os.listdir(f'{BASE_DIR}/inputs/test/cloth')
pairs = zip(model_image, cloth_image)

with open(f'{BASE_DIR}/inputs/test_pairs.txt', 'w') as file:
    for model, cloth in pairs:
        file.write(f"{model} {cloth}")

# making predictions
os.system(f"python {REPO_DIR}/test.py --name output --dataset_dir {BASE_DIR}/inputs --checkpoint_dir {REPO_DIR}/checkpoints --save_dir {BASE_DIR}/")
os.system(f"rm -rf {BASE_DIR}/inputs")
os.system(f"rm -rf {BASE_DIR}/output/.ipynb_checkpoints")
