### 1.11.0 <!-- 08/09/24 -->

- Add `Scale` input to **Texturizer** group
- Add **Set Viewport Color** checkbox
  - When selected, this changes the **Viewport Color**, **Metallic** and **Roughness** of the material.
  - When unselected, this resets them to Blender default.
  - If a material already exists, clicking its panel button will apply the current **Set Viewport Color** settings.

### 1.10.0 <!-- 07/06/24 -->

- Consolidate **Steel Roughness** group from 10 outputs to 5, sorted from low (`0.05`) roughness to high (`0.5`)
- Make **Energy Conservation** group optional for Blender versions 4 and up
- Code refactoring

### 1.9.1 <!-- 04/25/24 -->

- Add new materials
  - **QMM High-Alloy Stainless Steel**
  - **QMM Nickel-Vanadium Steel**
- Change **QMM Carbon Steel New** `Roughness` range to `0.2 - 0.4`
- Remove category **More Steel** and move materials into new **Alloys** sub-categories
  - **Carbon Steel**
  - **Stainless Steel**
  - **Alloy Steel**
  - **Specialty Steel**

### 1.9.0 <!-- 04/20/24 -->

- Add new category **More Steel**
- Add new materials
  - **QMM Carbon Steel New**
  - **QMM Carbon Steel Weathering**
  - **QMM 304 Common Stainless Steel**
  - **QMM 316 High-Chromium Stainless Steel**
  - **QMM 4140 Alloy Steel**
  - **QMM 4340 Alloy Steel**
  - **QMM Case-Hardened Steel A**
  - **QMM Case-Hardened Steel B**
  - **QMM Manganese Steel**
  - **QMM Tool Steel**
  - **QMM Spring Steel**
  - **QMM Structural Steel**
  - **QMM A36 Structural Steel**
  - **QMM A572 Structural Steel**
  - **QMM HSLA Steel**
  - **QMM Maraging Steel**
  - **QMM Free-Machining Steel**
  - **QMM Galvanized Steel**
  - **QMM Weathering Steel**
  - **QMM Virgin Weathering Steel**
- Update **Car Paint**
  - Change `Metal Flake > Scale` to `4096`
- Disable `This material already exists` alert

### 1.8.2 <!-- 03/29/24 -->

- Update **Metal Flake** group
  - Add `Blue Mask` output
  - Change `Scale` to `4096`

### 1.8.1 <!-- 03/27/24 -->

- 4.1 Bugfix: Set `socket_type` on Group Nodes

### 1.8.0 <!-- 03/14/24 -->

- Add new materials
  - **Car Paint**
- Add new groups
  - **Metal Flake** group with `Scale` and `Strength` outputs. This affects **Car Paint**.
- Tweaks to **Mithryl**
- Rename **Cinnabar** > **Cinnabar Lacquer**

### 1.7.0 <!-- 01/20/24 -->

- Add new materials
  - **Cinnabar**
  - **Mithryl**
- Add new groups
  - **Uneven Roughness** group with `Roughness` and `Mask` outputs. This affects **Cinnabar**.
- Remove materials
  - **Red Metal**

### 1.6.0 <!-- 10/29/23 -->

- Blender 4.0 Compatibility Update

### 1.5.8 <!-- 02/04/23 -->

- Add new material
  - **Silicon**
- Add new groups
  - **Anisotrophy X** group with `To Roughness` and `To Bump` outputs. This affects **Aluminium**.
  - **Steel Roughness** group with `Roughness` outputs for multiple types of Steel, sorted by most commonly used. This affects **Steel**.
- Add new category
  - **Minor Metals**
  - Re-sort materials
- Update **Energy Conservation v5** group
  - Rename **Diffuse (Base)** > **Reflectivity**
  - Rename **Specular Custom** > **Edge Tint**
- Update **Reflectivity**, **Edge Tint**, and `Roughness` of metals
  - Colors calculated using equations from Ole Gulbrandsen's [**Artist Friendly Metallic Fresnel**](https://www.jcgt.org/published/0003/04/03)
  - Python version: [**reflectivity_edge_tint.py**](https://github.com/don1138/blender-scripts/blob/main/reflectivity_edge_tint.py)
- Refactor code and rename files
  - Move classes for **Copper**, **Gold**, **Silver**, **Tin** and **Titanium** into **MakeMetal.py**
  - Remove suffix **GroupNode** from file names

### 1.5.7 <!-- 02/01/23 -->

- Update **Energy Conservation** group to **v5**
  - Add `Roughness`
  - Add **Fresnel CCP** group
- Update `diffuse color`, `specular color`, `roughness`, and `IOR` on most materials
- Rename **Chrome** to **Chromium**
- Bugfix
  - Broken links in **Asphalt** and **Asphalt Bleached**

### 1.5.6 <!-- 01/23/23 -->

- Bugfix
  - Broken color link in **Texturizer** group
- Code refactoring
  - **Red Metal**
- Spell check
  - From *Dialectric* to *Dielectric*

### 1.5.5 <!-- 01/10/23 -->

- Switch **PrincipledBSDF** light scattering to `MULTI_GGX`
- Update **Energy Conservation** node group
  - Calculate **Auto Specular Color** by **Linear Mapping** (`2 * (R, G, B)`) of **Diffuse Color**
  - Remove **Auto Specular Color** `Saturation` slider.
    - **Metal** color = **Auto Specular Color**
    - **Dielectric** color = **Auto Specular Color** with HSV `value` set to `0.01`
- Update **Color Mix** shader nodes
  - Add Blender 3.4.0 version test to switch between `ShaderNodeMixRGB` and `ShaderNodeMix`
  - This affects all materials that use a mix node

### 1.5.4 <!-- 12/24/22 -->

- Bugfix: Correct **Energy Conservation** node group connections

### 1.5.3 <!-- 12/22/22 -->

- Update **Energy Conservation** node group
  - New option to use an auto-generated specular (AGS) color, which is calculated from the diffuse color
  - New inputs:
    - **Custom/Auto switch** toggles between user-defined and AGS color
    - **Metal/Dielectric switch** toggles HSV value of AGS between metal `(0.99)` and dielectric `(0.01)` settings
    - **Saturation input** adjusts saturation of AGS
- Organize layout of RGB nodes inside color node groups
  - **Copper Colors**
  - **Gold Colors**
  - **Silver Colors**
  - **Titanium Colors**
- Code refactoring & cleanup

### 1.5.2 <!-- 12/15/22 -->

- Code refactoring
- PEP8 formatting

### 1.5.1 <!-- 12/14/22 -->

- Add names to node groups
  - **Copper Colors**
  - **Gold Colors**
  - **Silver Colors**
  - **Titanium Colors**
  - **Canistrophy**
  - **Energy Conservation**
  - **Texturizer**
- Add node groups to asset browser file
  - **Canistrophy**
  - **Energy Conservation**
  - **Specular**
  - **Texturizer**
- Rename **QMM Glass Hack** to **QMM Glass**
- Tweaks to
  - **QMM Glass**
  - **QMM Rubber Cutting Mat**
- Code refactoring

### 1.5.0 <!-- 10/17/22 -->

- UI localized/internationalized
  - **Chinese**
  - **Danish**
  - **Dutch**
  - **Finnish**
  - **French**
  - **German**
  - **Hungarian**
  - **Indonesian**
  - **Italian**
  - **Japanese**
  - **Polish**
  - **Portuguese**
  - **Portuguese (Brazilian)**
  - **Russian**
  - **Slovak**
  - **Spanish**
  - **Swedish**
  - **Ukrainian**
- Add new colors to **Color** group nodes
  - **Gold Colors**
    - **Chaos Harvest**
  - **Titanium Colors**
    - **Chaos Titanium**
- Edit **Canistrophy** Group
  - Add **Master Scale** input

### 1.4.9 <!-- 10/16/22 -->

- Add new material
  - **Nickel**
- Update `IOR`
  - **Gold**
  - **Silver**
- Edit **Canistrophy** Group
  - Fix effect to object orientation
  - Add `XYZ` and `XY Only` output options
- Rename **Cinnabar** to **Red Metal** since Cinnabar isn't a metal
- Tweaks to ALL materials except:
  - **Glass Hack**
  - **Rubber Cutting Mat**

### 1.4.8 <!-- 10/15/22 -->

- Update `Base Color`
  - **Copper**
  - **Gold**
  - **Silver**
- Update `IOR`
  - **Iron**
- Update `Base Color` and `IOR`
  - **Platinum**
  - **Zinc**
- Bugfix: **Color** group not connecting in Fresnel materials
  - **Copper (Fresnel)**
  - **Gold (Fresnel)**
  - **Silver (Fresnel)**

### 1.4.7 <!-- 9/27/22 -->

- Add new materials
  - **Tin**
  - **Zinc**
- Add **Displacement** to **Asphalt** and **Asphalt Bleached**
- Add **Canisotrophy** group with `To Roughness` output. This affects **Tin**.
- Replace **Specular** group with **Energy Conservation** group (via [**Christopher 3D**](https://www.youtube.com/watch?v=kgORQ5tMe2I))
  - Inputs
    - `IOR`
    - `Diffuse (Base)` Color
    - `Specular` Color
  - Outputs
    - `Color` - **Fresnel** mix of all inputs
    - `Specular`
    - `Clearcoat` - `Specular` value x10
    - `IOR`
  - This affects ALL materials, both metal and dialectic, except:
    - **Gold** and **Silver** because: IOR value is too low
    - **Gold (Fresnel)**, **Silver (Fresnel)**, and **Copper (Fresnel)** because: not compatable with node setup
    - **Glass Hack** because: not relevant
- Code cleanup

### 1.4.6 <!-- 8/10/22 -->

- New color values from [**physicallybased.info**](https://physicallybased.info/)
  - Set `Base Color` to new values
    - **Aluminium**
    - **Copper**
    - **Gold**
    - **Iron**
    - **Lead**
    - **Mercury**
    - **Platinum**
    - **Silver**
    - **Titanium**
  - Add new colors to **Color** group nodes
    - **Copper Colors**
      - **PBM Copper**
    - **Gold Colors**
      - **Harvest Gold**
      - **PBM Gold**
    - **Silver Colors**
      - **PBM Silver**
  - Sort colors in **Color Groups**
    - All colors after **Base Name** color sorted from lightest to darkest
  - Add **Color** group nodes to Asset Browser file
    - **Colors Copper**
    - **Colors Gold**
    - **Colors Silver**
    - **Colors Titanium**

### 1.4.5 <!-- 7/20/22 -->

- Rename material
  - **QMM Mercury Liquid** to **QMM Mercury**
- Update materials
  - **Cinnabar**
    - Add **Vermillion** Color Ramp
  - **Glass Hack**
    - Change `Transparent Shader > Color` to `F3F3FF`
- Reorder **Noble Metals** submenu
  - Alphabetize **Palladium** and **Platinum**
- Bugfix (Bump Node input assignment)
  - **Asphalt**
  - **Asphalt Bleached**
  - **Plaster**

### 1.4.4 <!-- 5/05/22 -->

- Add new material
  - **Cinnabar**

### 1.4.3 <!-- 5/01/22 -->

- Change **Add-On Updater** to manual install

### 1.4.2 <!-- 4/30/22 -->

- Update **Texturizer** node group
  - Change color/noise color mix from `OVERLAY` to `MULTIPLY`
  - 1 new input
    - **Roughness**
  - 4 new outputs
    - **Rough Ceiling** - Map Range from min (roughness - 0.1) to max (roughness)
    - **Roughness** - Noise (green channel) mixed (overlay) with roughness value
    - **Rough Floor** - Map Range from min (roughness) to max (roughness + 0.1)
    - **Height**

### 1.4.1 <!-- 4/26/22 -->

- Add new material
  - **Wall Paint**
- Tweaked layout of links in add-on preferences
- Tried to un-f*ck **Add-On Updater** install. Failed.

### 1.4.0 <!-- 4/22/22 -->

- Add new materials
  - **Asphalt**
  - **Asphalt Bleached**
  - **Palladium**
  - **Platinum**
  - **Titanium Polished**
- Remove redundant materials
  - **Copper Max**
  - **Pale Gold**
  - **Pale Silver**
  - **Silver Max**
- Rename materials
  - **Brass Metallic** > **Brass**
  - **Copper Min** > **Copper**
  - **Silver Min** > **Silver**
  - **Titanium** > **Titanium Textured**
- Revise material
  - **Plaster** - material color can now be changed by **PCOY**, **MCMC**, **HG71**, and **F58** add-ons.

### 1.3.8 <!-- 4/14/22 -->

![Blender QMM Extended Color Groups](https://github.com/don1138/blender-qmm/blob/main/imx/qmm-color-groups.png)

- Add new color to **Copper Color Node** group
  - **Dontnod Copper** <!-- #FAD0C0 -->
- Add **Titanium Color Node** group with 7 color choices. This affects **Titanium**. <!-- https://www.color-name.com/search/titanium -->
  - **Titanium** <!--#C1BAB1 -->
  - **Pale Titanium** <!--#CEC8C2 -->
  - **Dark Titanium** <!--#878681 -->
  - **Metallic Titanium** <!--#7A7772 -->
  - **Titanium White** <!--#F3F4F7 -->
  - **Titanium Frost** <!--#B0AFA9 -->
  - **Titanium Blue** <!--#5B798E -->
- Add **Texturizer Node** group with `Color` and `Normal` outputs. This affects **Titanium**.
- Update  `Roughness` values
  - **Titanium**

### 1.3.7 <!-- 4/01/22 -->

- Update IOR values
  - **Aluminium**
  - **Iron**
  - **Titanium**

### 1.3.6 <!-- 3/23/22 -->

- Add new color to **Gold Color Node** group
  - **Pirate Gold** <!-- #AE8403 -->

### 1.3.5 <!-- 3/14/22 -->

- Update `Roughness` values
  - **Aluminium**
  - **Brass**
  - **Bronze**
  - **Chrome**
  - **Copper (Fresnel)**
  - **Copper Min**
  - **Copper Max**
  - **Gold**
  - **Pale Gold**
  - **Gold (Fresnel)**
  - **Iron**
  - **Lead**
  - **Silver (Fresnel)**
  - **Silver Min**
  - **Silver Max**
  - **Steel**
  - **Titanium**

### 1.3.4 <!-- 1/02/22 -->

![Blender QMM Extended Color Groups](https://github.com/don1138/blender-qmm/blob/main/imx/qmm-extended-color-groups.png)

- **Bugfix:** Change node group output type from `Float` to `Color`
- Add **Gold Color** group with 9 color choices. This affects **Gold**, **Pale Gold**, and **Gold (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Gold_(color) -->
  - **Gold** <!-- #D4AF37 -->
  - **Pale Gold** <!-- #FFE39D -->
  - **Golden Gold** <!-- #FFD700 -->
  - **Old Gold** <!-- #CFB53B -->
  - **Golden Yellow** <!-- #FFDF00 -->
  - **Golden Poppy** <!-- #FCC200 -->
  - **Crayola Gold** <!-- #E6BE8A -->
  - **Vegas Gold** <!-- #C5B358 -->
  - **Satin Sheen Gold** <!-- #CBA135 -->
- Add **Silver Color** group with 10 color choices. This affects **Silver Min**, **Silver Max**, **Pale Silver**, and **Silver (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Silver_(color) -->
  - **Silver** <!--#AAA9AD -->
  - **Pale Silver** <!--#FCFAF5 -->
  - **Basic Silver** <!--#C0C0C0 -->
  - **Crayola Silver** <!--#C9C0BB -->
  - **Silver Pink** <!--C4AEAD -->
  - **Silver Sand** <!--#BFC1C2 -->
  - **Silver Chalice** <!--#ACACAC -->
  - **Roman Silver** <!--#838996 -->
  - **Old Silver** <!--#848482 -->
  - **Sonic Silver** <!--#757575 -->

### 1.3.3 <!-- 12/30/21 -->

- **Bugfix: Specular** group was being added twice
- Add **Copper Color** group with 5 color choices. This affects **Copper Min**, **Copper Max**, and **Copper (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Copper_(color) -->
  - **Copper** <!-- #B87333 -->
  - **Pale Copper** <!-- #DA8A67 -->
  - **Copper Red** <!-- #CB6D51 -->
  - **Copper Penny** <!-- #AD6F69 -->
  - **Copper Rose** <!-- #996666 -->

### 1.3.2 <!-- 12/29/21 -->

- Combine `IOR/Specular` math nodes into **Specular** group

### 1.3.1 <!-- 12/21/21 -->

- Move material files into subfolders

### 1.3.0 <!-- 12/15/21 -->

- Blender 3.0 compatability
- Update node input IDs to new settings
- Connect `IOR` value node to **Principled BSDF** `IOR` input

### 1.2.3 <!-- 12/15/21 -->

- Shorten material var names (material_aluminium > m_aluminium)
- Change `bl_category` from **QMM** to **MAT**

### 1.2.2 <!-- 8/12/21 -->

- UILayout tweaks to QMM panel
- UILayout tweaks to Additional Resources in preferences panel

### 1.2.1 <!-- 7/24/21 -->

- Add links to Additional Resources to preferences panel

### 1.2.0 <!-- 7/14/21 -->

- Add new materials
  - **Chrome**
  - **Lead**
  - **Lead Rough**
- Split Base Metals & Alloys into 2 sub-menus
- Set Metallic and Roughness on Viewport Display
- Misc. Code Cleanup

### 1.1.1 <!-- 7/8/21 -->

- Add Tooltips to buttons
- Set IOR value on all Principled BDSF nodes
- Add "IOR" label to Value node on chain connected to Principled BSDF Specular input

### 1.1.0 <!-- 6/17/21 -->

- Add new material
  - **Tinted Plaster**

### 1.0.0

- Add [**CG Cookie's Addon Updater**](https://github.com/CGCookie/blender-addon-updater) system
- Correct version numbering system
- Misc. code cleanup

### 0.0.4 <!-- 3/22/21 -->

- Add new materials
  - **Pale Gold Metallic**
  - **Pale Silver Metallic**
  - **Rubber Cutting Mat**
- Add `QMM` prefix to classes to resolve naming conflict with other shader addons

### 0.0.3 <!-- 3/21/21 -->

- Move categories into sub-panels
- Change **Category** to `Material`
- Change Blender compatability to 2.83

### 0.0.2 <!-- 3/10/21 -->

- Add error checking: Does the material already exist?

### 0.0.1 <!-- 3/9/21 -->

- Create materials
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
