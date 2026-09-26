TensorBoardLogger and ModelCheckpoint are not using the same folder by default
## 🐛 Bug
(master branch)
By default, the TensorBoardLogger writes logs into `lightning_logs/0` but ModelCheckpoint writes checkpoint into `lightning_logs/version_0`.
