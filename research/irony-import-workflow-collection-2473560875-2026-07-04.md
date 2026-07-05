# Irony Import Workflow For Steam Collection 2473560875

Date checked: 2026-07-04  
Collection: [4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity](https://steamcommunity.com/sharedfiles/filedetails/?id=2473560875)  
Irony docs checked: [Collection Mods](https://raw.githubusercontent.com/wiki/bcssov/IronyModManager/Collection-Mods.md), [Installed Mods](https://raw.githubusercontent.com/wiki/bcssov/IronyModManager/Installed-Mods.md), [New User Checklist](https://raw.githubusercontent.com/wiki/bcssov/IronyModManager/New-User-Checklist.md)

## Correction

Irony's main **Import** button is not a text-file import for Steam collections. It imports a previously exported Irony collection ZIP, or other supported formats through the nearby additional import options.

For Steam Workshop mods that are already subscribed and installed, the intended workflow is:

1. Let Irony detect installed mods in the **Installed Mods** panel.
2. Create or select an Irony collection.
3. Select/check the desired installed mods so they appear in **Collection Mods**.
4. Copy the desired load-order list to the clipboard.
5. Right-click inside **Collection Mods** and use **Import Mod Order From Clipboard**.
6. Apply the collection to write the load order.

The author's Irony text list is therefore a clipboard load-order aid, not a standalone file import.

## Practical Notes For This Collection

- Use `research/steam-collection-2473560875-irony-mod-list-2026-07-04.txt` as the clipboard order source.
- The list has 116 entries and includes `Fairy Empire Shipset`, which is present in the current Steam collection but missing from the author's 2026-07-02 discussion text list.
- The clipboard order list is corrected to match local Workshop `descriptor.mod` names where Irony requires exact names. The current known corrections are `More Primitives` instead of the Steam title `More Primitives [4.4.x]`, and `Neo-Enigmatic Shipset  - NSC3 Patch` with the descriptor's double-space before the hyphen.
- If all subscribed mods are visible in Irony, avoid the main Import button for this task.
- If a Paradox Launcher playset already contains exactly the collection mods, Irony's additional import menu can import the active Paradox Launcher playset instead.
- If extra subscribed mods are present, keep them out of the first Irony collection baseline until the collection-only list applies cleanly.

## Minimum User Workflow

1. Open Irony and select Stellaris.
2. Create a new collection, for example `Rage000 4.4 Baseline`.
3. In **Installed Mods**, use `research/steam-collection-2473560875-irony-remoteid-filters-2026-07-04.txt` to bulk select the collection mods:
   - paste one chunk into the Installed Mods filter box;
   - click the **Selected** column header checkbox once to select all visible mods;
   - repeat for the next chunk.
4. Open `research/steam-collection-2473560875-irony-mod-list-2026-07-04.txt`, select all, and copy.
5. In Irony's **Collection Mods** panel, right-click and choose **Import Mod Order From Clipboard**.
6. Click **Apply**.
7. Do not run Conflict Solver until the mod list and order look right.

## Faster Bulk Selection

Irony's Installed Mods docs say filtering supports remote IDs and that the header checkbox can enable or disable all visible mods. This avoids manually ticking every mod.

Use the generated remote-ID filter file:

- `research/steam-collection-2473560875-irony-remoteid-filters-2026-07-04.txt`

Try the all-in-one filter first. If Irony's filter box or UI becomes sluggish, use the four chunked filters instead.

## Remaining Pain Point

Irony does not appear to provide a direct "subscribe/import Steam Workshop collection by collection ID" path. Steam subscription and Irony collection/load-order management are separate steps.
