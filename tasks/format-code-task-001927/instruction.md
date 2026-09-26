## Feature request: shadow augmentation for training

When training docTR models on scanned / clean document images, the trained model often struggles on real-world photos where part of the page is covered by a shadow (hand, phone, lamp, etc.). The training data rarely contains those cases, so the model never learns to be robust to them.

Looking at `doctr.transforms`, there are already a lot of augmentations covering photometric variations (brightness, contrast, saturation, hue, gamma, jpeg quality, gaussian noise, gaussian blur, channel shuffle, ...) and some geometric ones, but there is nothing that simulates a shadow falling on the document.

It would be very useful to have a transform module — in the same style as the existing ones, available for both the PyTorch and TensorFlow backends — that takes an image tensor and returns the same image with a randomly-shaped, randomly-placed darker region on it, so we can drop it into our training `Compose` pipelines alongside the other augmentations.

Ideally the darkening intensity should be configurable (so you can have anything from a faint shade to an almost-black region), and the shape / position should vary from one call to the next so the model sees a diverse set of shadows during training.

Naming-wise, something like `RandomShadow` (mirroring `RandomHorizontalFlip` etc.) exposed from `doctr.transforms` for both backends would fit the existing style.
