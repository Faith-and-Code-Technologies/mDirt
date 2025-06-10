<p align="center">
  <img src="assets/icon.png" alt="App Logo" width="500"/>
</p>

# mDirt - A Minecraft Datapack Generator
_making Datapacks is really tedious - mDirt makes it easy._

Creating custom Minecraft datapacks can be time-consuming and complex. **mDirt** simplifies this process by providing an easy-to-use tool for generating datapacks with custom features like blocks, items, recipes, and more.

---

### 🛠️ **Supported Versions**
- **Minecraft Versions Supported**: 1.21.3, 1.21.4, and 1.21.5  
  - Full compatibility for **1.21.5** has been added.

---

### 🚨 **Version 1.21.5 Support**
We’ve now added official support for **Minecraft 1.21.5**, enabling you to create and export datapacks for the latest Minecraft version. This includes full feature compatibility for blocks, items, recipes, and paintings.

---

### 💻 **Getting Started**

1. **[Download the latest release](https://github.com/Faith-and-Code-Technologies/mDirt/releases)**
   - For **Windows only**: Comes with a pre-built executable (`mDirt.exe`)
   - No need for Python or additional dependencies.
   - Extract and run — no installation required.

2. **Use the GUI**
   - Hover over any input for tooltips and guidance.
   - Fill out your datapack elements: blocks, items, structures, equipment, etc.

3. **Generate Your Datapack**
   - Click **“Generate Pack”** to build your datapack and resourcepack.
   - Output is placed in the `exports/` folder inside your mDirt directory.

4. **Deploy in Minecraft**
   - Move the generated **datapack** to `.minecraft/saves/<your-world>/datapacks/`
   - Move the **resourcepack** to `.minecraft/resourcepacks/`
   - Enable the resourcepack in-game.
   - Use commands to give yourself your custom content:
     - `/function YOURNAMESPACE:give_blocks`
     - `/function YOURNAMESPACE:give_items`
     - `/function YOURNAMESPACE:give_paintings`

---

### 📚 Full Documentation

For full setup instructions, tutorials, and feature breakdowns, check out the 👉 **[mDirt Wiki](https://github.com/Faith-and-Code-Technologies/mDirt/wiki)**

---

### 🧩 **Feature Support by Version**
**As of v2.5.1**
---
**Note**: If a feature is not listed for a specific version, that version **does not** support it.

| Feature          | 1.21.3 | 1.21.4 | 1.21.5 |
|------------------|--------|--------|--------|
| **Blocks**       | ✅ 100%   | ✅ 100%   | ✅ 100%   |
| **Items**        | ✅ 80%    | ✅ 80%    | ✅ 80%    |
| **Recipes**      | ✅ 100%   | ✅ 100%   | ✅ 100%   |
| **Paintings**    | ❌ -      | ✅ 100%   | ✅ 100%   |

---

### 🚀 **Coming Soon**

- v3.0
  - As you may know, v3 has been in development for a couple of months. We had been planning on implementing a new system for the backend to make things like Enchantments, Predicates, Loot Tables, etc. possible.
  - But due to the extreme amount of work that will go into that, we have delayed it until v3.1 or v4.0
  - v3.0 is now almost finished, and does still come with some MAJOR changes, and two new features. Stay tuned!

---

### 💡 **Tips & Best Practices**

- **Namespaces**: Please ensure the Namespace the program asks you to define doesn't clash with any other datapack you may be using!
- **Testing**: After generating your datapack, it's always a good idea to test it in a separate Minecraft world before adding it to your main world.
- **Backing Up**: As always, back up your Minecraft world before applying new datapacks, especially when using custom features.

---

### 🙌 **Credits**

- **mDirt** was created by **@TheJupiterDev** and **@JustJoshinDev**.
- Special thanks to **[Admin](https://youtube.com/@WASDBuildTeam)** for his custom block generation method.
  
---

### 🌍 **Get Involved**
We welcome contributions and suggestions! If you have ideas or find bugs, please create an issue or open a pull request on the [GitHub Repository](https://github.com/Faith-and-Code-Technologies/mDirt).

---
