import tensorflow as tf
from transformers import (
    TFSegformerForSemanticSegmentation,
    SegformerConfig,
    DefaultDataCollator,
)
from datasets import load_from_disk
import os

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "datasets")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

train_ds = load_from_disk(os.path.join(DATASET_DIR, "train"))
val_ds = load_from_disk(os.path.join(DATASET_DIR, "val"))
test_ds = load_from_disk(os.path.join(DATASET_DIR, "test"))


def preprocess_data(examples):
    image = tf.expand_dims(examples["image"], -1)
    mask = tf.expand_dims(examples["mask"], -1)

    # image = tf.image.resize_with_pad(
    #     image,
    #     256,
    #     256,
    # )
    # mask = tf.image.resize_with_pad(mask, 256, 256)

    return {
        "pixel_values": image,
        "labels": mask,
    }


train_ds = train_ds.map(preprocess_data)
val_ds = val_ds.map(preprocess_data)
test_ds = test_ds.map(preprocess_data)


data_collator = DefaultDataCollator(return_tensors="tf")
tf_train_ds = train_ds.to_tf_dataset(
    columns=["pixel_values", "labels"],
    collate_fn=data_collator,
    shuffle=True,
    batch_size=1,
)

config = SegformerConfig.from_pretrained("nvidia/segformer-b0-finetuned-ade-512-512")
model = TFSegformerForSemanticSegmentation.from_pretrained(
    "nvidia/segformer-b0-finetuned-ade-512-512", config=config
)

optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)  # type: ignore
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)  # type: ignore
metrics = ["accuracy"]

# Compile the model
model.compile(optimizer=optimizer, loss=loss, metrics=metrics)  # type: ignore

# Train the model
model.fit(tf_train_ds, epochs=3)  # type: ignore

model.save_pretrained(os.path.join(MODEL_DIR, "segformer-test"))  # type: ignore
