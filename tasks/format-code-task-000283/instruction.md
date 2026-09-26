New general page: FTC tab gives React warning
<!-- Please use this template when creating an issue. 
- Please check the boxes after you've created your issue.
- Please use the latest version of Yoast SEO.-->

* [ ] I've read and understood the [contribution guidelines](https://github.com/Yoast/wordpress-seo/blob/trunk/.github/CONTRIBUTING.md).
* [ ] I've searched for any related issues and avoided creating a duplicate issue.

### Please give us a description of what happened

### To Reproduce
#### Step-by-step reproduction instructions
1. Enable debug output (`SCRIPT_DEBUG`)
2. Visit Yoast > General
3. Notice the warning in the browser console:
> Warning: Failed prop type: The prop `onDiscard` is marked as required in `UnsavedChangesModal`, but its value is `undefined`. 

The `useBlocker` can return `undefined` for `proceed` (and `reset`) for specific states.
See their type def in the documentation: https://reactrouter.com/en/main/hooks/use-blocker

#### Expected results
1. No prop warnings

#### Actual results
1. Prop warning

### Screenshots, screen recording, code snippet
If possible, please provide a screenshot, a screen recording or a code snippet which demonstrates the bug.

### Technical info
<!-- You can check these boxes once you've created the issue.
- If you are using Gutenberg, Elementor or the Classic Editor plugin, please make sure you have updated to the latest version.
 -->
* If relevant, which editor is affected (or editors): 
- [ ] Block Editor
- [ ] Gutenberg Editor
- [ ] Elementor Editor
- [ ] Classic Editor 
- [ ] Other: <!-- please specify -->

<!-- You can check these boxes once you've created the issue. -->
* Which browser is affected (or browsers): 
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Other: <!-- please specify -->

#### Used versions
* Device you are using:
* Operating system:
* PHP version:
* WordPress version: 
* WordPress Theme:
* Yoast SEO version: 
* <!-- If relevant -->Gutenberg plugin version: 
* <!-- If relevant -->Elementor plugin version: 
* <!-- If relevant -->Classic Editor plugin version: 
* Relevant plugins in case of a bug:
