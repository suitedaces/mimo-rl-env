Big security vulnerability
Hi,

I've just realised that it is very easy to create a big security vulnerability when using this package to upload files (I almost did this on my site).

Suppose you have JSON body parsing enabled on a POST or PUT route, say '/upload-files', as well as multipart parsing. This is quite easy to do e.g. if you add JSON parsing as global middleware. Suppose it expects the files to be in a field named 'uploads'. Then you can make a POST or PUT request to '/upload-files' with a JSON body that looks something like `{"files": {"uploads": [{"path": "/any/file/path"}]}}`, making the request handler think a file has been uploaded to `/any/file/path`. Now suppose that the handler is set up to copy uploaded files into a public uploads folder. By choosing the path appropriately I can make the server copy any file I like on the server into the public uploads folder and then view its contents. So by using well-known paths of sensitive files I can read private keys, passwords etc. and maybe even gain full access to the server this way.

I haven't tried actually doing this, but I think it's correct (sorry if I'm wrong). In my opinion, it would be better to put the files object on ctx.request instead of ctx.request.body, so that we know it can be trusted.

Thanks.
