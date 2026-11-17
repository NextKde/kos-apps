# Canonical Demo controls

This module packages the required controls from `nextkdeAppDemo/shared/qml` under
`Kos.Demo` so Calendar and Settings use the actual Demo implementations without changing other
apps' legacy `Kos.Ui` module. The baseline QML, GLSL and QSB assets come from the canonical Demo sources;
`upstream-sha256.json` retains the hashes of that synchronized baseline.
`local-patches.json` lists the explicitly maintained application-side changes
pending synchronization with the canonical library. The list records this change series, including its application-source baseline
hashes; earlier extraction adapters (such as the icon facade) retain their
existing provenance. The namespace/build metadata are packaging additions. Preserve the GPL-3.0
license of the parent project and upstream. Prefer updating the canonical Demo first and syncing source/assets and hashes
together. When carrying an application-side fix, list it in `local-patches.json`
without rewriting the original baseline hashes; remove that entry once the
canonical update is synchronized.

Hosts supply geometry, state, theme preferences and real sibling capture sources.
They must not recreate optical layers or animations around these controls. The
liquid controls retain their glass edge on keyboard focus without an accent outline.
Solid keyboard focus remains semantic. Tooltips use the same shared liquid material
at 0.7 coverage, 14 px corners and 11 px opaque secondary text; their capture source
must exclude the popup overlay.
