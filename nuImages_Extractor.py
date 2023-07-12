
import sys
from tqdm import tqdm
sys.path.append("F:\\nuscenes-devkit\\python_sdk")
from python_sdk.nuimages.nuimages import NuImages

nuim = NuImages(dataroot='./data/sets/nuimages', version='v1.0-test', verbose=True, lazy=True)
for i in tqdm(range(0, 557715)):

    sample_idx = i
    sample = nuim.sample[sample_idx]
    sample = nuim.get('sample', sample['token'])
    sample_idx_check = nuim.getind('sample', sample['token'])
    assert sample_idx == sample_idx_check
    key_camera_token = sample['key_camera_token']
    #print(key_camera_token)
    nuim.render_image(key_camera_token, annotation_type='objects', with_category=True, with_attributes=True, box_line_width=-1, render_scale=5)