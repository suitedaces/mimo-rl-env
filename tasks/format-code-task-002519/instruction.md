TypeError: unsupported type for timedelta days component: NoneType
I'm getting an error when running deleterr on both the latest and develop tags.

```bash
2024-04-02 18:23:51 - INFO :: deleterr.py :: deleterr : Running version 
2024-04-02 18:23:51 - INFO :: deleterr.py :: deleterr : Log level set to INFO
2024-04-02 18:23:51 - INFO :: config.py :: deleterr : Running in dry-run mode, no changes will be made.
2024-04-02 18:23:51 - INFO :: deleterr.py :: deleterr : Processing radarr instance: 'Radarr'
2024-04-02 18:23:51 - INFO :: media_cleaner.py :: deleterr : Processing library 'Movies'
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/app/app/deleterr.py", line 111, in <module>
    main()
  File "/app/app/deleterr.py", line 107, in main
    Deleterr(config)
  File "/app/app/deleterr.py", line 32, in __init__
    self.process_radarr()
  File "/app/app/deleterr.py", line 42, in process_radarr
    saved_space += self.media_cleaner.process_library_movies(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/media_cleaner.py", line 212, in process_library_movies
    movie_activity = self.get_movie_activity(library, movies_library)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/media_cleaner.py", line 58, in get_movie_activity
    return self.tautulli.get_activity(library, movies_library.key)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/modules/tautulli.py", line 45, in get_activity
    min_date = self._calculate_min_date(library_config)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/app/modules/tautulli.py", line 65, in _calculate_min_date
    unwatched_threshold_date = datetime.now() - timedelta(
                                                ^^^^^^^^^^
TypeError: unsupported type for timedelta days component: NoneType
```
