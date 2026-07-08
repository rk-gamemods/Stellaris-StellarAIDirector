# Porting and regression checklists

## 4.4.x release checklist

- [ ] Confirm target: 4.4.5 stable/current local install, 4.4.4 rollback, or 4.5 beta.
- [ ] Use descriptor `supported_version="v4.4.*"` for stable 4.4.
- [ ] Verify no local + Workshop duplicate of same mod.
- [ ] Run with only this mod enabled.
- [ ] Check `error.log` clean or known benign only.
- [ ] Check localisation in English.
- [ ] Run `reload text` after localisation changes.
- [ ] Test new game start.
- [ ] Test save/load.
- [ ] Test multiplayer/checksum if claiming compatibility.

## 4.4 Nomads/Arkship regression checklist

Run these if the mod touches economy, colonies, planets, wars, diplomacy, UI, starbases, automation, or AI:

- [ ] Normal settled empire start.
- [ ] Nomadic Empire start.
- [ ] Arkship colony receives expected modifiers.
- [ ] Capital-scope assumptions hold or fail safely.
- [ ] Country with no normal colonies does not crash scripts.
- [ ] Waystation UI opens with mod enabled.
- [ ] Wayline modifiers do not double-stack unexpectedly.
- [ ] Contract creation/cancellation does not break events.
- [ ] Nomad total-war ownership transfer does not orphan event targets.
- [ ] Fleet automation UI works if interface files are touched.
- [ ] Situation Log UI works if interface files are touched.

Sources for why: `[S001] [S002] [S004]`

## 4.5 porting checklist

Required for mods touching pops/factions/ethics/jobs/species/UI/AI:

- [ ] Search for `pop_has_ethic`.
- [ ] Search for `pop_group_has_ethic`.
- [ ] Search for old faction parameters.
- [ ] Replace with `pop_ethic_amount` / `pop_ethic_percentage` where appropriate.
- [ ] Evaluate `pop_force_add_ethic`, `pop_force_remove_ethic`, `pop_force_transfer_ethic`.
- [ ] Update UI displays to percentage-based ethics/factions.
- [ ] Test old saves only if claiming migration; otherwise mark save-incompatible.
- [ ] Create separate `port-4.5` branch.

Source: `[S004]`

## Load-order compatibility checklist

- [ ] Identify every vanilla key overridden.
- [ ] Identify every other-mod key overridden.
- [ ] Run Irony conflict solver.
- [ ] Create compatibility patch for duplicate object keys.
- [ ] Avoid relying on filename-only conflict checks.
- [ ] Document required playset order.
- [ ] Test with source mods above patch.
- [ ] Re-test after every upstream mod update.

Sources: `[S011] [S012]`

## Debug packet checklist for Codex

- [ ] Game version and checksum.
- [ ] Active playset order.
- [ ] Full mod tree.
- [ ] All changed files.
- [ ] Vanilla reference files for touched paths.
- [ ] `error.log`.
- [ ] `game.log`.
- [ ] Steps to reproduce.
- [ ] Expected behavior.
- [ ] Actual behavior.
- [ ] Whether Ironman is on.

## LLM bridge safety checklist

- [ ] Save parser treats save as untrusted input.
- [ ] API keys in env vars, not committed files.
- [ ] No arbitrary console command generation.
- [ ] Whitelisted action schema.
- [ ] Fog-of-war filter if applicable.
- [ ] Human approval for destructive actions.
- [ ] Audit log for every LLM recommendation/action.
- [ ] Local/offline mode tested.
- [ ] Network egress restricted when local-only mode intended.

Source: `[S016]`
