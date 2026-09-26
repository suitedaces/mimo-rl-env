## Problem Statement

Just generated a fresh site with the defaultsite generator and I'm hitting two weird things. First, when I try to use `get_node_trans_by_node_id(id, 'en')` in one of my Twig templates I get an "unknown function" error — tried both with and without `--demosite` and it never seems to be available. Second, running the generator command itself is acting strange around `app/config/config.yml`; the `white_october_pagerfanta` bit isn't being handled sensibly, especially when deciding whether that configuration is already there or still needs to be added. Am I missing a step somewhere?

## Expected Outcomes

- Generated default sites expose the Twig function `get_node_trans_by_node_id(nodeId, lang)` in templates, regardless of whether the demosite option is enabled.
- Calling `get_node_trans_by_node_id(nodeId, lang)` returns the matching available node translation for that node id and language, or `null` when no matching available translation exists.
- The defaultsite generator bases its `white_october_pagerfanta` handling on the existing `app/config/config.yml` configuration.
- When `white_october_pagerfanta` is already present in `app/config/config.yml`, running the generator does not append a duplicate block.
- When `white_october_pagerfanta` is absent from `app/config/config.yml`, running the generator still adds the expected pagerfanta configuration block.

## Implementation Notes

- Keep the fix compatible with both defaultsite generation modes, with and without demosite content.
- The concrete organization of generated Twig extension code, service wiring, and helper methods is up to the implementation as long as the generated site exposes the documented Twig behavior.
- The config handling may be implemented wherever appropriate in the generator flow, but it should preserve existing configuration content and make the pagerfanta decision from the actual existing configuration.
