## Can't fetch model files or image files directly via URL with their extension

I'm using Manyfold to manage my 3D model library and wanted to grab files directly by URL — e.g. hitting `/libraries/1/models/2/model_files/3.stl` should give me back the STL contents so I can pipe it into my slicer or link to it from another tool. Same idea for image files attached to a model (`.png`, `.jpg`, etc. — the preview/thumbnail image).

This doesn't work right now. Visiting the model file page in a browser (no extension) shows the HTML page fine, but as soon as I tack on the model file's actual extension, or an image extension for image files, I don't get the file back. The request just doesn't serve any content.

It should be possible to request any supported model file type (STL, OBJ, 3MF, …) or image type by URL and have the raw file streamed back.
