# Stellaris 4.4.x AI War Mechanics Reference

This folder contains the external war-mechanics reference packet imported from
`C:\Users\Admin\Downloads\stellaris_4_4_ai_war_reference.zip` on 2026-07-08.

Use this packet as the focused reference for the AI war-start chain: claims,
casus belli, war goals, diplomatic action gates, personality war fields, war
defines, fleet-use-vs-declaration separation, and passive-galaxy failure modes.

## Files

| Path | Use |
| --- | --- |
| `war_declaration_chain.md` | Full chain from AI war pressure to legal declaration and post-declaration fleet behavior. |
| `war_ai_lever_catalog.csv` | Tabular catalog of war-related levers, prerequisites, interactions, and failure modes. |
| `personality_war_fields.md` | Personality field reference for aggression, bravery, military spending, claim/opinion effects, and fleet preferences. |
| `claims_cb_wargoals_reference.md` | Claims, casus belli, and war-goal prerequisite reference. |
| `war_defines_catalog.csv` | War, claim, declaration-distance, fleet-confidence, and military-operation define catalog. |
| `passive_galaxy_failure_modes.md` | Diagnosis guide for AIs that build fleets but do not fight. |
| `replacement_ai_war_checklist.md` | Checklist for auditing or implementing replacement-AI war behavior without direct forced-war events. |
| `source_inventory.csv` | Source inventory, reliability notes, and uncertainty labels for the packet. |

## Authority

This packet is a focused external research artifact. It complements, but does
not replace, local source inspection.

Before implementing code from this packet, verify the relevant claims against:

1. current local vanilla files under `C:\Steam\steamapps\common\Stellaris`;
2. active-stack winning files and conflict data;
3. generated Stellar AI Director files;
4. static validation and focused tests.

The packet itself labels its strongest file-level source as a public
`HildoYe/game_files` mirror at commit `e6d53157737d29324a41c6598a384af3b4091df1`.
Treat mirror values as research leads until local 4.4.x files and active-stack
load order confirm them.
