# mDirt - A Minecraft Datapack Generator
##### making Datapacks is really tedious
Creating custom Minecraft datapacks can be time-consuming and complex. **mDirt** simplifies this process by providing an easy-to-use tool for generating datapacks with custom features like blocks, items, recipes, and more.

> 🚫 mDirt Development has been haulted for the forseeable future.

---

### 🛠️ **Supported Versions**
- **Minecraft Versions Supported**: 1.21.3, 1.21.4, and 1.21.5  
  - Full compatibility for **1.21.5** has been added.

---

### 🚨 **Version 1.21.5 Support**
We’ve now added official support for **Minecraft 1.21.5**, enabling you to create and export datapacks for the latest Minecraft version. This includes full feature compatibility for blocks, items, recipes, and paintings.

---

### 💻 **How to Use mDirt**

1. **Download and Install**
   - Head over to the [Releases Page](https://github.com/Faith-and-Code-Technologies/mDirt/releases) and download the latest version of **mDirt**. 
   - **Windows Only**: The release contains a pre-packaged binary created using **PyInstaller**, which means you don't need Python or any other dependencies to run the app.
   - Once downloaded, extract the folder and simply **run the executable** (`mDirt.exe`), and you're ready to start generating custom Minecraft datapacks.

2. **Using the Interface**
   - **Tooltips**: Hover over any field to get a description and guide on how to fill it out.
   - **Fill in the Details**: Customize your datapack by entering information such as block names, item properties, recipe details, etc.
   
3. **Generate Your Datapack**
   - Once all fields are filled out, click the **"Generate Pack"** button to create your datapack.
   - mDirt will package everything into a datapack and ready it for export.

4. **Deploying Your Datapack in Minecraft**
  - Place the generated datapack into your world’s **datapacks** folder, and place the generated resourcepack into the **resourcepacks** folder.
    - Be sure to enable the resourcepack!
  - After generating the datapack, use the following commands in Minecraft to get your custom features:
    - **Blocks**: `/function YOURNAMESPACE:give_blocks`
    - **Items**: `/function YOURNAMESPACE:give_items`
    - **Paintings**: `/function YOURNAMESPACE:give_paintings`

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
| **Enchantments** | ❌ -      | ❌ 0%     | ❌ 0%     |

---

### 🚀 **Coming Soon**

- **KoreUI**
  - We have created a Python package that converts JSON Schemas to a PySide6 UI. With this system, we will be able to support Advancements, Loot Tables, Predicates, and so much more.
  - Please stay tuned for the implementation - manually creating JSON files that are thousands of lines long will take some time.

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
