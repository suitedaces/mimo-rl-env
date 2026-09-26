我这边 LeftPanel 的收藏列表有点不稳定：明明已经有 Linux/WSL distro 收藏，有时候面板里就是不显示，尤其跑 Cypress 的时候更明显；另外如果面板隐藏期间改了收藏，再打开看到的还是旧的。能不能让 LeftPanel 每次显示时都按当前收藏内容把 places 和 distributions 展示出来？

Expected outcomes:
- Favorites rendering
  - When the current favorites include Linux/WSL distribution entries, `LeftPanel` should show the corresponding Linux/distribution section and entries when it is rendered, including in Cypress or test-like environments.
  - `LeftPanel` should continue to show the current favorite places from the favorites state when rendered.
- Hidden panel updates
  - If favorite places are changed while `LeftPanel` is hidden, showing/rendering the panel again should reflect the current places rather than a stale earlier list.
  - If favorite distributions are changed while `LeftPanel` is hidden, showing/rendering the panel again should reflect the current distributions rather than a stale earlier list.
- Visibility behavior
  - The panel’s hidden state should affect only its visibility, not whether future renders use the latest favorites data.

Implementation notes:
- The exact component structure, state management approach, and update mechanism are up to the implementer.
- Tests should be able to verify the behavior through the rendered `LeftPanel` UI and existing application state, without relying on a particular internal helper or lifecycle implementation.
