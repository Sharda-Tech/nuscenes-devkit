import fiftyone as fo
import fiftyone.zoo as foz
fo.config.dataset_zoo_dir = "./"


dataset = foz.load_zoo_dataset(
    "open-images-v6",
    split="validation",
    label_types=["detections"],
    classes = ["Motorcycle"],
    seed=51,
    shuffle=True,
    dataset_name="kk",
)