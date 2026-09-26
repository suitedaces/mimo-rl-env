[BUG] KeyError: 'filenameEnc'
I get the following error when I try to sync my photo library:

```
Traceback (most recent call last):
  File "/app/./src/main.py", line 8, in <module>
    sync.sync()
  File "/app/src/sync.py", line 521, in sync
    photos_stats = _perform_photos_sync(config, api, sync_state, photos_sync_interval)
  File "/app/src/sync.py", line 258, in _perform_photos_sync
    sync_photos.sync_photos(config=config, photos=api.photos)
  File "/app/src/sync_photos.py", line 412, in sync_photos
    _sync_albums_by_configuration(
  File "/app/src/sync_photos.py", line 498, in _sync_albums_by_configuration
    _sync_all_albums_except_filtered(
  File "/app/src/sync_photos.py", line 571, in _sync_all_albums_except_filtered
    sync_album_photos(
  File "/app/src/album_sync_orchestrator.py", line 63, in sync_album_photos
    download_tasks = _collect_album_download_tasks(
  File "/app/src/album_sync_orchestrator.py", line 120, in _collect_album_download_tasks
    download_info = collect_download_task(
  File "/app/src/photo_download_manager.py", line 128, in collect_download_task
    if file_size not in photo.versions:
  File "/usr/local/lib/python3.10/site-packages/icloudpy/services/photos.py", line 709, in versions
    version = {"filename": self.filename}
  File "/usr/local/lib/python3.10/site-packages/icloudpy/services/photos.py", line 656, in filename
    self._master_record["fields"]["filenameEnc"]["value"],
KeyError: 'filenameEnc'
```

In my case I had a GoPro video with no filename that had gotten in my photos library by mistake and once I removed it the sync worked.
