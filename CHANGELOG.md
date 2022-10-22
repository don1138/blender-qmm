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
- Add new colors to **Color Group** nodes
  - **Gold Colors**
    - **Chaos Harvest**
  - **Titanium Colors**
    - **Chaos Titanium**
- Edit **Canistrophy** Group
  - Add **Master Scale** input

### 1.4.9 <!-- 10/16/22 -->
- Add new material
  - **Nickel**
- Rename **Cinnabar** to **Red Metal** since Cinnabar isn't a metal.
- Edit **Canistrophy** Group
  - Fix effect to object orientation
  - Add `XYZ` and `XY Only` output options
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
- Bugfix: **Color Group** not connecting in Fresnel materials
    - **Copper (Fresnel)**
    - **Gold (Fresnel)**
    - **Silver (Fresnel)**

### 1.4.7 <!-- 9/27/22 -->
- Add new materials
  - **Tin**
  - **Zinc**
- Add **Displacement** to **Asphalt** and **Asphalt Bleached**
- Add **Canisotrophy Group** with `To Roughness` output. This affects **Tin**.
- Replace **Specular Group** with **Energy Conservation Group** (via [Christopher 3D](https://www.youtube.com/watch?v=kgORQ5tMe2I)). This affects ALL materials, both metal and dialectic, except:
    - **Gold** and **Silver** because: IOR value is too low
    - **Gold (Fresnel)**, **Silver (Fresnel)**, and **Copper (Fresnel)** because: not compatable with node setup
    - **Glass Hack** because: not relevant
- Code cleanup

### 1.4.6 <!-- 8/10/22 -->
- new color values from [physicallybased.info](https://physicallybased.info/)
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
  - Add new colors to **Color Group** nodes
    - **Copper Colors**
      - **PBM Copper**
    - **Gold Colors**
      - **Harvest Gold**
      - **PBM Gold**
    - **Silver Colors**
      - **PBM Silver**
  - Sort colors in **Color Groups**
    - All colors after **Base Name** color sorted from lightest to darkest
  - Add **Color Group** nodes to Asset Browser file
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

![Blender QMM Extended Color Groups](https://github.com/don1138/blender-qmm/blob/main/qmm-color-groups.png)

- Add new color to **Copper Color Node Group**
  - **Dontnod Copper** <!-- #FAD0C0 -->
- Add **Titanium Color Node Group** with 7 color choices. This affects **Titanium**. <!-- https://www.color-name.com/search/titanium -->
  - **Titanium** <!--#C1BAB1 -->
  - **Pale Titanium** <!--#CEC8C2 -->
  - **Dark Titanium** <!--#878681 -->
  - **Metallic Titanium** <!--#7A7772 -->
  - **Titanium White** <!--#F3F4F7 -->
  - **Titanium Frost** <!--#B0AFA9 -->
  - **Titanium Blue** <!--#5B798E -->
- Add **Texturizer Node Group** with `Color` and `Normal` outputs. This affects **Titanium**.
- Update  `Roughness` values
  - **Titanium**

### 1.3.7 <!-- 4/01/22 -->

- Update IOR values
  - **Aluminium**
  - **Iron**
  - **Titanium**

### 1.3.6 <!-- 3/23/22 -->

- Add new color to **Gold Color Node Group**
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

![Blender QMM Extended Color Groups](https://github.com/don1138/blender-qmm/blob/main/qmm-extended-color-groups.png)

- **Bugfix:** Change node group output type from `Float` to `Color`
- Add **Gold Color Group** with 9 color choices. This affects **Gold**, **Pale Gold**, and **Gold (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Gold_(color) -->
  - **Gold** <!-- #D4AF37 -->
  - **Pale Gold** <!-- #FFE39D -->
  - **Golden Gold** <!-- #FFD700 -->
  - **Old Gold** <!-- #CFB53B -->
  - **Golden Yellow** <!-- #FFDF00 -->
  - **Golden Poppy** <!-- #FCC200 -->
  - **Crayola Gold** <!-- #E6BE8A -->
  - **Vegas Gold** <!-- #C5B358 -->
  - **Satin Sheen Gold** <!-- #CBA135 -->
- Add **Silver Color Group** with 10 color choices. This affects **Silver Min**, **Silver Max**, **Pale Silver**, and **Silver (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Silver_(color) -->
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

- **Bugfix: Specular Group** was being added twice
- Add **Copper Color Group** with 5 color choices. This affects **Copper Min**, **Copper Max**, and **Copper (Fresnel)**. <!-- https://en.wikipedia.org/wiki/Copper_(color) -->
  - **Copper** <!-- #B87333 -->
  - **Pale Copper** <!-- #DA8A67 -->
  - **Copper Red** <!-- #CB6D51 -->
  - **Copper Penny** <!-- #AD6F69 -->
  - **Copper Rose** <!-- #996666 -->

### 1.3.2 <!-- 12/29/21 -->

- Combine `IOR/Specular` math nodes into **Specular Group**

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
