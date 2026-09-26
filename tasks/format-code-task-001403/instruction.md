Traversing array not working
Hi, it looks to me as if in the current version 2.2.0, traversing array nodes does not seem to be working. The following works in version 1.0.7:
`gatsby-config.js`:
```javascript
{
      resolve: 'gatsby-plugin-remote-images',
      options: {
        nodeType: 'PictureCollection',
        imagePath: 'pictures[].url',
        name: 'imageSharp',
      }
    }
```
`gatsby-node.js`:
```javascript
exports.sourceNodes = ({ actions, createNodeId, createContentDigest }) => {
  const { createNode } = actions
  createNode({
    id: createNodeId("testNode1"),
    pictures: [
      { url: "https://unsplash.com/photos/aJnHSrgSWkk/download?force=true" },
      { url: "https://unsplash.com/photos/_qy3tHmhwvk/download?force=true" },
      { url: "https://unsplash.com/photos/k3jEtUmKhJo/download?force=true" },
    ],
    internal: {
      type: "PictureCollection",
      contentDigest: createContentDigest({}),
    },
  })
}
```
So I'm creating a node type `PictureCollection` with an array of `pictures` containing objects with `url`s for `gatsby-plugin-remote-images`. In v1.0.7, this creates new `imageSharp` fields on the `pictures` containing exactly the right data for each picture.

In v2.2.0, a single `imageSharp` field is created on the top level of `PictureCollection` instead, with a value of `null`. There does not seem to be a possibility to query the downloaded images.

I believe this is similar to this issue: https://github.com/graysonhicks/gatsby-plugin-remote-images/issues/37, which is however marked as fixed. Am I doing something wrong or is this still broken?
