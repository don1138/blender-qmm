### 1.3.2 <!-- 12/30/21 -->
- Bugfix: Specular Group was being added twice
- Added Copper Color node Group with 5 color choices <!-- https://en.wikipedia.org/wiki/Copper_(color) -->
	- **Copper** <!-- #B87333 -->
	- **Pale Copper** <!-- #DA8A67 -->
	- **Copper Red** <!-- #CB6D51 -->
	- **Copper Penny** <!-- #AD6F69 -->
	- **Copper Rose** <!-- #996666 -->

### 1.3.2 <!-- 12/29/21 -->
- Combine IOR/Specular math nodes into Specular Group

### 1.3.1 <!-- 12/21/21 -->
- Move material files into subfolders

### 1.3.0 <!-- 12/15/21 -->
- Blender 3.0 compatability
- Update node input IDs to new settings
- Connect IOR Value node to Principled BSDF IOR input

### 1.2.3 <!-- 12/15/21 -->
- Shorten material var names (material_aluminium > m_aluminium)
- Change `bl_category` from **QMM** to **MAT**

### 1.2.2 <!-- 8/12/21 -->
- UILayout tweaks to QMM panel
- UILayout tweaks to Additional Resources in preferences panel

### 1.2.1 <!-- 7/24/21 -->
- Added links to Additional Resources to preferences panel

### 1.2.0 <!-- 7/14/21 -->
- New Materials
	- **Chrome**
	- **Lead**
	- **Lead Rough**
- Split Base Metals & Alloys into 2 sub-menus
- Set Metallic and Roughness on Viewport Display
- Misc. Code Cleanup

### 1.1.1 <!-- 7/8/21 -->
- Added Tooltips to buttons
- Set IOR value on all Principled BDSF nodes
- Added "IOR" label to Value node on chain connected to Principled BSDF Specular input

### 1.1.0 <!-- 6/17/21 -->
- New Material
	- **Tinted Plaster**

### 1.0.0
- Added [**CG Cookie's Addon Updater**](https://github.com/CGCookie/blender-addon-updater) system
- Corrected version numbering system
- Misc. code cleanup

### 0.0.4 <!-- 3/22/21 -->
- New Materials
	- **Pale Gold Metallic**
	- **Pale Silver Metallic**
	- **Rubber Cutting Mat**
- Add ``QMM`` prefix to classes to resolve naming conflict with other shader addons

### 0.0.3 <!-- 3/21/21 -->
- Move categories into sub-panels
- Change Category to Material
- Change Blender compatability to 2.83

### 0.0.2 <!-- 3/10/21 -->
- Add error checking: Does the material already exist?

### 0.0.1 <!-- 3/9/21 -->
- Create Materials
	- **Aluminium Metallic**
	- **Brass Metallic**
	- **Bronze Metallic**
	- **Copper**
	- **Copper Metallic Min**
	- **Copper Metallic Max**
	- **Glass**
	- **Gold**
	- **Gold Metallic**
	- **Iron Metallic**
	- **Mercury Liquid**
	- **Silver**
	- **Silver Metallic Min**
	- **Silver Metallic Max**
	- **Steel Metallic**
	- **Titanium Metallic**
