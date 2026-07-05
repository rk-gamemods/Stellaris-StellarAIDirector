# Local Stellaris Environment

Date checked: 2026-07-04

## Scope

This note records local Stellaris paths, Irony Mod Manager location, and user mod-list preferences for this project. Irony is a Stellaris project tool, not a global Codex tool.

## Local Paths

| Surface | Path | Status |
| --- | --- | --- |
| Steam root | `C:\Steam` | Found from Steam registry keys |
| Steam library file | `C:\Steam\steamapps\libraryfolders.vdf` | Found |
| Stellaris app manifest | `C:\Steam\steamapps\appmanifest_281990.acf` | Found |
| Stellaris install | `C:\Steam\steamapps\common\Stellaris` | Found |
| Steam Workshop Stellaris content | `C:\Steam\steamapps\workshop\content\281990` | Found, 537 workshop item folders observed |
| Paradox Stellaris user folder | `C:\Users\Admin\Documents\Paradox Interactive\Stellaris` | Found |
| Paradox launcher mod folder | `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod` | Found |
| Irony install folder | `C:\Users\Admin\AppData\Local\Programs\Irony Mod Manager` | Found |
| Irony executable | `C:\Users\Admin\AppData\Local\Programs\Irony Mod Manager\IronyModManager.exe` | Found |
| Irony user data | `C:\Users\Admin\AppData\Roaming\Mario` | Found |

Observed Irony executable file version: `1.27.192.32361`.

Observed Irony product version: `1.27.192+7e69c2ddbd`.

Irony `appSettings.json` sets `App.StoragePath` to `%AppData%\Mario`.

## User Mod Preferences

Exclude by default:

- Real Space. User dislikes the UI/readability impact and finds it makes ships harder to see.
- Star Wars themed total conversions and mod sets.

Prioritize for future compatibility research:

- Gigastructural Engineering.
- NSC3.
- Ship/component expansion mods that add endgame items or interact with NSC3.
- UI mods and explicit UI dependency chains, especially dependencies required by NSC3 or other preferred mods.
- Advanced AI mods that can handle major modded technologies and megastructures.
- Performance optimizers that are demonstrably useful and do not create hidden gameplay or compatibility problems.
- Strong space station, starbase defense, planetary defense, planetary weapon, and orbital-bombardment-resistance mods.

## Research Implications

When building the first serious mod list, verify explicit dependency chains from the Steam Workshop pages and local descriptors rather than assuming names from memory. In particular:

- Check whether NSC3 requires or recommends UI Overhaul Dynamic or specific UI compatibility patches.
- Check whether NSC3 and ship/component expansion mods such as Extra Ship Components NEXT have an explicit load-order relationship.
- Check whether Gigastructural Engineering compatibility notes mention NSC3, component mods, AI mods, or UI/topbar resource display patches.
- For AI mods, look for evidence that the AI can use Gigastructural/NSC3/component-mod systems, not only vanilla 4.4 systems.
- For performance mods, separate real performance improvements from behavior throttles that may make the AI or galaxy less active.
- For defensive mods, separate stronger static defenses from mods that make wars stall indefinitely, break AI war logic, or overlap with NSC3/Gigas ship and megastructure balance.
