require-context-role incorrectly requires elements to be direct children of their context element
Given the example markup for a [Bootstrap nav](https://getbootstrap.com/docs/5.2/components/navs-tabs/#javascript-behavior):
```html
<ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home-tab-pane" type="button" role="tab" aria-controls="home-tab-pane" aria-selected="true">Home</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile-tab-pane" type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false">Profile</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="contact-tab" data-bs-toggle="tab" data-bs-target="#contact-tab-pane" type="button" role="tab" aria-controls="contact-tab-pane" aria-selected="false">Contact</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="disabled-tab" data-bs-toggle="tab" data-bs-target="#disabled-tab-pane" type="button" role="tab" aria-controls="disabled-tab-pane" aria-selected="false" disabled>Disabled</button>
  </li>
</ul>
<div class="tab-content" id="myTabContent">
  <div class="tab-pane fade show active" id="home-tab-pane" role="tabpanel" aria-labelledby="home-tab" tabindex="0">...</div>
  <div class="tab-pane fade" id="profile-tab-pane" role="tabpanel" aria-labelledby="profile-tab" tabindex="0">...</div>
  <div class="tab-pane fade" id="contact-tab-pane" role="tabpanel" aria-labelledby="contact-tab" tabindex="0">...</div>
  <div class="tab-pane fade" id="disabled-tab-pane" role="tabpanel" aria-labelledby="disabled-tab" tabindex="0">...</div>
</div>
```

`ember-template-lint@4.14.0` issues the errors:
```
  2:2  error  Use of presentation role on <li> detected. Semantic elements should not be used for presentation.  no-invalid-role
  5:2  error  Use of presentation role on <li> detected. Semantic elements should not be used for presentation.  no-invalid-role
  8:2  error  Use of presentation role on <li> detected. Semantic elements should not be used for presentation.  no-invalid-role
  11:2  error  Use of presentation role on <li> detected. Semantic elements should not be used for presentation.  no-invalid-role
  3:117  error  You have an element with the role of "tab" but it is missing the required (immediate) parent element of "[tablist]". Reference: https://www.w3.org/TR/wai-aria-1.1/#tab.  require-context-role
  6:116  error  You have an element with the role of "tab" but it is missing the required (immediate) parent element of "[tablist]". Reference: https://www.w3.org/TR/wai-aria-1.1/#tab.  require-context-role
  9:116  error  You have an element with the role of "tab" but it is missing the required (immediate) parent element of "[tablist]". Reference: https://www.w3.org/TR/wai-aria-1.1/#tab.  require-context-role
  12:118  error  You have an element with the role of "tab" but it is missing the required (immediate) parent element of "[tablist]". Reference: https://www.w3.org/TR/wai-aria-1.1/#tab.  require-context-role
```

In general, my understanding is that the Bootstrap sample markup is typically fairly well designed with accessibility needs in mind, so I'm surprised to see that it fails these accessibility checks.  

More specifically, I believe that the `require-context-role` is too rigid in its enforcement as the [ARIA required context role](https://www.w3.org/WAI/standards-guidelines/act/rules/ff89c9/proposed/#background) rule explains that there need not exist a direct DOM parent-child relationship:
> Being a child in the [accessibility tree](https://www.w3.org/TR/act-rules-aspects/#input-aspects-accessibility) is different from being a child in the DOM tree. Some DOM nodes have no corresponding node in the [accessibility tree](https://www.w3.org/TR/act-rules-aspects/#input-aspects-accessibility) (for example, because they are marked with role="presentation"). A child in the [accessibility tree](https://www.w3.org/TR/act-rules-aspects/#input-aspects-accessibility) can thus correspond to a descendant in the DOM tree. Additionally, the use of aria-owns attribute can change the tree structure to something which is not a subtree of the DOM tree.

A similar point was raised in https://github.com/ember-template-lint/ember-template-lint/issues/626#issuecomment-1136968659 regarding the MDN documentation.
