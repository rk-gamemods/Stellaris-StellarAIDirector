# Stellar AI Director Economic Relief Channel Audit

Date: 2026-07-09

Target: Stellaris 4.4.5-forward design with 4.4.4 load compatibility.

This is a preliminary capability audit, not a closed list. The Director should
rank every eligible relief channel by retained value, time to effect,
repeatability, diplomatic cost, and whether AI initiation is actually exposed
to script.

| state | channel | priority | current capability | decision |
| --- | --- | ---: | --- | --- |
| overflow | high-value investment | 1 | Economic plans, budgets, research, colony, fleet, and megastructure gates are scriptable. | Use first when legal and safe. |
| overflow | speculative investment | 2 | Scaling/optional subplans and low-priority construction routes are scriptable. | Prefer to destroying capped production. |
| overflow | storage expansion | 2 | Vanilla country_near_tangible_resource_cap fires at 90% of the mods-included cap; Gigas Kugelblitz stages add 50K, 150K, and 500K storage. | Enable the safe Kugelblitz route under near-cap pressure. |
| overflow | bilateral resource trade | 3 | action_offer_trade_deal exists, but deal composition/initiation is engine-side. NAI defines expose stockpile-over/under and fraction preferences. | Preserve and observe; do not claim a scripted offer was sent. |
| overflow | market sale | 4 | Director can value and execute a sale with market_resource_price. | Sell immediately above the fixed reserve and 90% of actual storage cap; never discard production at 100%. |
| mild shortage | domestic income repair | 1 | Economic-plan income targets and runway gates are scriptable. | Keep relative repair active until earned income and operating float are both safe. |
| mild shortage | new-upkeep suppression | 2 | Budgets, construction eligibility, megastructure/fleet gates, and some policy/edict weights are scriptable. | Block avoidable new liabilities in the short resource. |
| hard shortage | temporary market bridge | 1 | NAI.AI_ALLOWED_TO_BUY is script-exposed only as a resource allow-list; actual purchase timing/amount is engine-side. | Leave emergency access available, but never let bought stockpile satisfy the earned-income gate. |
| deep deficit | fleet docking/war exit | 1 | Strategic need is clear; a verified general-purpose script consumer that orders ordinary AI fleets to dock or negotiates peace for economy relief has not yet been found. | Audit before implementation. |
| deep deficit | fleet disbanding | 2 | Destructive fleet effects may exist, but upkeep attribution and safe ship selection are not yet proven. | Do not destroy assets without source-proven attribution and strict last-resort gates. |
| deep deficit | building or megastructure liability reduction | 2 | Construction suppression is proven; general safe deactivation/dismantling and upkeep attribution are not. | Audit object-specific options before any destructive automation. |
| deep deficit | territory/subject restructuring | 3 | Diplomacy and subject systems expose many actions, but no general safe liquidation policy is proven. | Last resort only after a dedicated strategic audit. |
| any shortage | enclave/caravaneer/event relief | opportunistic | Enclave and caravaneer events contain lump-sum and monthly resource effects, but availability and AI choice are event-specific. | Treat as opportunistic income, not a dependable recovery plan. |
| any shortage | subject/federation transfers | opportunistic | Agreement terms can create recurring transfers, but negotiation, legality, and timing are relationship-specific. | Include in later diplomacy audit; never assume immediate availability. |

## Installed-source evidence

- C:/Steam/steamapps/common/Stellaris/common/defines/00_defines.txt:
  NAI.AI_ALLOWED_TO_BUY, AI_ALLOWED_TO_SELL, and bilateral trade thresholds.
- C:/Steam/steamapps/common/Stellaris/common/diplomatic_actions/00_actions.txt:
  action_offer_trade_deal legality; no data-defined resource composition.
- C:/Steam/steamapps/common/Stellaris/common/scripted_triggers/00_scripted_triggers.txt:
  country_near_tangible_resource_cap uses resource_stockpile_percent at 0.9.
- research/mod-source-snapshots/2026-07-04/1121692237-gigastructural-engineering-more-44/common/megastructures/zz_c_kugelblitz.txt:
  stage storage modifiers of 50,000, 150,000, and 500,000.
- C:/Steam/steamapps/common/Stellaris/events/caravaneer_events.txt and
  events/overlord_enclaves_events.txt: case-specific lump-sum/monthly resource
  gains and costs.

This Markdown file is support/research evidence and has no standalone rendered
counterpart.
