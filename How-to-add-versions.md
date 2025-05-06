# How to Update mDirt for new Minecraft Versions
**As of mDirt v2.4**

### `main.py` changes:
- Use `NEW_compile_data.py` to compile the new data json
- Under `setupData()`:
  - Update `dataformat` and `resourceformat` to include new formats
  - Update `self.header` to include new mDirt version
- Update mDirt version in `exportProject()` and `importProject()`
- Under `generateResourcePack()`:
  - Add an `elif self.packVersion == "VERSION"` folder structure
  - Add an `elif self.packVersion == "VERSION"` for generator imports
- Under `generateDataPack()`:
  - Update mDirt version in the `load.mcfunction` generation
  - Add an `elif self.packVersion == "VERSION"` for generator imports

### UI changes:
- In `ui.ui`, update `packVersion` to include new version
- In `ui.ui`, update window name to include new mDirt version
- Export `ui.ui` to `ui.py`
- In `details.ui`, update `packVersion` to include new version
- Export `details.ui` to `details.py`

### Now:
- Add a new version folder under the `src/generation`, and update the generators to fit with the new Minecraft version.