# Problem Statement

I can only see Pi-hole Core/Web/FTL update availability as binary sensors right now, so they don’t show up with the rest of Home Assistant’s update entities. Could Pi-hole expose those three as proper update entities, with the current/latest version and a link to the release notes when an update is available?

# Expected outcomes

- Pi-hole exposes three first-class Home Assistant update entities for the Core, Web interface, and FTL components, corresponding to the existing Core Update Available, Web Update Available, and FTL Update Available update indicators.
- Each new update entity reports whether an update is available through the standard Home Assistant update entity state, so the entities can be discovered and displayed with other update entities.
- Each new update entity exposes standard update metadata: `current_version` and `latest_version`.
  - The Core update entity uses Pi-hole’s Core current/latest version data.
  - The Web interface update entity uses Pi-hole’s Web current/latest version data.
  - The FTL update entity uses Pi-hole’s FTL current/latest version data.
- When a latest version is known, each update entity exposes a `release_url` pointing to the release notes for that component’s latest version.
  - Core links to the Pi-hole Core GitHub release tag.
  - Web interface links to the AdminLTE Web interface GitHub release tag.
  - FTL links to the FTL GitHub release tag.
- The update entities have user-facing titles for the component they represent: Pi-hole Core, Pi-hole Web interface, and Pi-hole FTL DNS, and are categorized as diagnostic entities.
- The existing Pi-hole binary sensor update indicators remain available for compatibility, but newly created Core Update Available, Web Update Available, and FTL Update Available binary sensor entities are disabled by default to avoid duplicate update reporting.

# Implementation notes

- Preserve existing Pi-hole integration behavior outside of update reporting.
- The exact internal organization, helper types, and validation location are up to the implementer, as long as the behavior is observable through Home Assistant’s standard update entity model and existing entity registry behavior.
- Handle missing or unavailable Pi-hole version data gracefully instead of failing setup or update entity creation.
