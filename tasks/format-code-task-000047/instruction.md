Windows runner: set Windows component for Docker Desktop to optional
Hey @kichik,

I`m able to build the image for the windows runner in eu-central-1 now without issues.
But what I recognized is that Docker desktop will be installed out of the box.
https://github.com/CloudSnorkel/cdk-github-runners/blob/c64683b62802de1817e173029a6d9a6695fb5fe9/src/providers/image-builders/ami.ts#L254

Docker desktop requires dependent on company size a subscription when it`s installed on windows or mac.

Can we make the installation of docker desktop optional  for the windows runner ?
