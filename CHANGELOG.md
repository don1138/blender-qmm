# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.24.3 - 2026-08-14

### Changed

- Moved the version number into the main panel title.

## 1.24.2 - 2026-08-10

### Changed

- Added version number to the main panel.

## 1.24.1 - 2026-08-10

### Changed

- Changed panel category from **Mat** to **Quick Tools**

## [1.24.0] - 2026-07-15

### Changed

- Updated compatibility for Blender 4.5 LTS and 5.2 LTS
  - Removed compatibility code for Blender versions before 4.0
  - Modernized node-group interface creation
  - Replaced positional standard-node socket indices with named sockets where names are unambiguous
  - Retained positional indices for sockets with duplicated names
  - Replaced legacy node types with their current equivalents
- Preserved the UV texture-coordinate connection in **Anisotrophy X**

### Fixed

- Fixed **Texturizer** Rough Ceiling subtraction
- Removed a duplicate link from **Uneven Roughness**
- Fixed **Cutting Mat** compatibility across Blender 4.5 and 5.2
- Corrected the **Canisotrophy** XY Scale minimum

## [1.23.0] - 2026-07-14

### Changed

- Updated compatibility for Blender 5.2
  - Replaced positional **Principled BSDF** socket indices with named sockets
  - Corrected Bump node connections to the **Normal** input
- Updated minimum supported Blender version to **4.0.0**

### Fixed

- Fixed **Cinnabar Lacquer**
- Fixed **Tinted Plaster**
- Fixed **Asphalt**
- Fixed **Asphalt Bleached**
- Fixed **Car Paint**
- Fixed **Wall Paint**

## [1.22.1] - 2025-12-21

### Fixed

- Replaced deprecated `ShaderNodeSeparateRGB` with feature-detected `ShaderNodeSeparateColor` and explicit RGB mode for Blender 4.x and 5.x compatibility
- Unlinked the `Vector` group input from the `ShaderNodeTexNoise` node

## [1.22.0] - 2025-11-21

### Changed

- Moved `color` and `node` group scripts into new `mats/color` and `mats/nodes` subfolders

## 1.21.1 - 2025-10-31

### Changed

- Updated `bl_info` metadata
  - Changed `doc_url` to point to the GitHub QMM wiki instead of the main site

## [1.21.0] - 2025-10-31

### Changed

- Overhauled UI localization
- Updated supported language list based on active user base:
  - Japanese
  - German
  - French
  - Russian
  - Italian
  - Brazilian Portuguese
  - Spanish
  - Indonesian
  - Chinese Traditional
  - Korean
  - Polish
  - Turkish
  - Dutch
  - Ukrainian
  - Hungarian

### Fixed

- Fixed node selection by translated name in non-English locales
  - Switched node lookups to `bl_idname` for Material Output, Principled BSDF, Mix Shader, and related nodes

## 1.20.0 - 2025-07-13

### Changed

- Updated **Mithryl**
  - Changed color tint from turquoise to **Cosmic Spectrum Green**

### Fixed

- Updated **Principled BSDF** node **Emission** inputs for Blender 4.3 compatibility

## [1.19.0] - 2025-06-03

### Added

- Added **Uneven Roughness** group to all metals

### Removed

- Removed **Addon Updater**

### Fixed

- Fixed error unregistering **QMMSettings**

## [1.18.0] - 2025-01-07

### Added

- Added **QMM Orichalcum**

## [1.17.0] - 2024-12-08

### Changed

- Updated Blender 4.3.0 compatibility for:
  - **Glass.py**
  - **Plaster.py**
- Updated output labels on **Steel Roughness** group node affecting **Steel**

## [1.16.0] - 2024-11-27

### Changed

- Updated Blender 4.3.0 compatibility for:
  - **CarPaint.py**
  - **CuttingMat.py**
  - **Cinnabar.py**

## 1.15.0 - 2024-09-12

### Changed

- Adjusted `Secondary Color` of **Pearlescent Pigment**

## [1.14.0] - 2024-09-10

### Changed

- Adjusted and reactivated IOR values
- Cleaned up miscellaneous nodes

## [1.13.0] - 2024-08-31

### Added

- Added **Pearlescent Pigment** group affecting **Car Paint**

## [1.12.0] - 2024-08-09

### Added

- Added **Set Viewport Color** checkbox
  - When selected, changes the material's **Viewport Color**, **Metallic**, and **Roughness**
  - When unselected, resets them to Blender defaults
  - If a material already exists, clicking its panel button applies the current **Set Viewport Color** settings

## [1.11.0] - 2024-08-03

### Added

- Added `Scale` input to **Texturizer** group

## [1.10.0] - 2024-07-06

### Changed

- Consolidated **Steel Roughness** group from 10 outputs to 5, sorted from low (`0.05`) roughness to high (`0.5`)
- Made **Energy Conservation** group optional for Blender 4 and later
- Refactored code

## 1.9.1 - 2024-04-25

### Added

- Added **QMM High-Alloy Stainless Steel**
- Added **QMM Nickel-Vanadium Steel**
- Added **Alloys** subcategories:
  - **Carbon Steel**
  - **Stainless Steel**
  - **Alloy Steel**
  - **Specialty Steel**

### Changed

- Changed **QMM Carbon Steel New** `Roughness` range to `0.2 - 0.4`
- Moved materials from **More Steel** into the new **Alloys** subcategories

### Removed

- Removed **More Steel** category

## [1.9.0] - 2024-04-20

### Added

- Added **More Steel** category
- Added materials:
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

### Changed

- Updated **Car Paint**
  - Changed `Metal Flake > Scale` to `4096`
- Disabled `This material already exists` alert

## 1.8.2 - 2024-03-29

### Added

- Added `Blue Mask` output to **Metal Flake**

### Changed

- Changed **Metal Flake** `Scale` to `4096`

## 1.8.1 - 2024-03-27

### Fixed

- Added `socket_type` to Group Nodes for Blender 4.1 compatibility

## [1.8.0] - 2024-03-14

### Added

- Added **Car Paint**
- Added **Metal Flake** group with `Scale` and `Strength` outputs affecting **Car Paint**

### Changed

- Updated **Mithryl**
- Renamed **Cinnabar** to **Cinnabar Lacquer**

## 1.7.0 - 2024-01-20

### Added

- Added **Cinnabar**
- Added **Mithryl**
- Added **Uneven Roughness** group with `Roughness` and `Mask` outputs affecting **Cinnabar**

### Removed

- Removed **Red Metal**

## [1.6.0] - 2023-10-29

### Changed

- Added Blender 4.0 compatibility

## [1.5.8] - 2023-02-04

### Added

- Added **Silicon**
- Added **Anisotrophy X** group with `To Roughness` and `To Bump` outputs affecting **Aluminium**
- Added **Steel Roughness** group with `Roughness` outputs for multiple types of steel
- Added **Minor Metals** category

### Changed

- Re-sorted materials
- Updated **Energy Conservation v5**
  - Renamed **Diffuse (Base)** to **Reflectivity**
  - Renamed **Specular Custom** to **Edge Tint**
- Updated **Reflectivity**, **Edge Tint**, and `Roughness` of metals using equations from Ole Gulbrandsen's [**Artist Friendly Metallic Fresnel**](https://www.jcgt.org/published/0003/04/03)
- Refactored code and renamed files
  - Moved classes for **Copper**, **Gold**, **Silver**, **Tin**, and **Titanium** into **MakeMetal.py**
  - Removed suffix **GroupNode** from file names

## [1.5.7] - 2023-02-01

### Added

- Added `Roughness` to **Energy Conservation v5**
- Added **Fresnel CCP** group

### Changed

- Updated `diffuse color`, `specular color`, `roughness`, and `IOR` on most materials
- Renamed **Chrome** to **Chromium**

### Fixed

- Fixed broken links in **Asphalt** and **Asphalt Bleached**

## [1.5.6] - 2023-01-23

### Changed

- Refactored **Red Metal**
- Corrected spelling from *Dialectric* to *Dielectric*

### Fixed

- Fixed broken color link in **Texturizer** group

## [1.5.5] - 2023-01-10

### Changed

- Switched **Principled BSDF** light scattering to `MULTI_GGX`
- Updated **Energy Conservation** node group
  - Calculated **Auto Specular Color** using linear mapping (`2 * (R, G, B)`) of **Diffuse Color**
  - Removed **Auto Specular Color** `Saturation` slider
  - Set **Metal** color to **Auto Specular Color**
  - Set **Dielectric** color to **Auto Specular Color** with HSV `value` set to `0.01`
- Updated **Color Mix** shader nodes
  - Added Blender 3.4.0 version test to switch between `ShaderNodeMixRGB` and `ShaderNodeMix`
  - Affects all materials using a mix node

## [1.5.4] - 2022-12-24

### Fixed

- Corrected **Energy Conservation** node group connections

## [1.5.3] - 2022-12-22

### Added

- Added auto-generated specular color option to **Energy Conservation**
- Added inputs:
  - **Custom/Auto switch**
  - **Metal/Dielectric switch**
  - **Saturation input**

### Changed

- Updated **Energy Conservation** node group
- Organized RGB node layouts inside:
  - **Copper Colors**
  - **Gold Colors**
  - **Silver Colors**
  - **Titanium Colors**
- Refactored and cleaned up code

## 1.5.2 - 2022-12-15

### Changed

- Refactored code
- Applied PEP 8 formatting

## [1.5.1] - 2022-12-14

### Added

- Added names to node groups:
  - **Copper Colors**
  - **Gold Colors**
  - **Silver Colors**
  - **Titanium Colors**
  - **Canistrophy**
  - **Energy Conservation**
  - **Texturizer**
- Added node groups to Asset Browser file:
  - **Canistrophy**
  - **Energy Conservation**
  - **Specular**
  - **Texturizer**

### Changed

- Renamed **QMM Glass Hack** to **QMM Glass**
- Updated:
  - **QMM Glass**
  - **QMM Rubber Cutting Mat**
- Refactored code

## [1.5.0] - 2022-10-17

### Added

- Added UI localization for:
  - Chinese
  - Danish
  - Dutch
  - Finnish
  - French
  - German
  - Hungarian
  - Indonesian
  - Italian
  - Japanese
  - Polish
  - Portuguese
  - Portuguese (Brazilian)
  - Russian
  - Slovak
  - Spanish
  - Swedish
  - Ukrainian
- Added **Chaos Harvest** to **Gold Colors**
- Added **Chaos Titanium** to **Titanium Colors**
- Added **Master Scale** input to **Canistrophy**

## [1.4.9] - 2022-10-16

### Added

- Added **Nickel**
- Added `XYZ` and `XY Only` outputs to **Canistrophy**

### Changed

- Updated `IOR` for:
  - **Gold**
  - **Silver**
- Updated **Canistrophy** to fix the effect to object orientation
- Renamed **Cinnabar** to **Red Metal**
- Updated all materials except:
  - **Glass Hack**
  - **Rubber Cutting Mat**

## [1.4.8] - 2022-10-15

### Changed

- Updated `Base Color` for:
  - **Copper**
  - **Gold**
  - **Silver**
- Updated `IOR` for **Iron**
- Updated `Base Color` and `IOR` for:
  - **Platinum**
  - **Zinc**

### Fixed

- Fixed **Color** group connections in Fresnel materials:
  - **Copper (Fresnel)**
  - **Gold (Fresnel)**
  - **Silver (Fresnel)**

## [1.4.7] - 2022-09-27

### Added

- Added **Tin**
- Added **Zinc**
- Added **Displacement** to **Asphalt** and **Asphalt Bleached**
- Added **Canisotrophy** group with `To Roughness` output affecting **Tin**
- Added **Energy Conservation** group with:
  - `IOR`
  - `Diffuse (Base)` Color
  - `Specular` Color
- Added outputs:
  - `Color`
  - `Specular`
  - `Clearcoat`
  - `IOR`

### Changed

- Replaced **Specular** group with **Energy Conservation**
- Applied **Energy Conservation** to all applicable metal and dielectric materials except:
  - **Gold**
  - **Silver**
  - **Gold (Fresnel)**
  - **Silver (Fresnel)**
  - **Copper (Fresnel)**
  - **Glass Hack**
- Cleaned up code

## [1.4.6] - 2022-08-10

### Added

- Added new color values from [**physicallybased.info**](https://physicallybased.info/)
- Added **PBM Copper** to **Copper Colors**
- Added **Harvest Gold** and **PBM Gold** to **Gold Colors**
- Added **PBM Silver** to **Silver Colors**
- Added color group nodes to Asset Browser:
  - **Colors Copper**
  - **Colors Gold**
  - **Colors Silver**
  - **Colors Titanium**

### Changed

- Updated `Base Color` values for:
  - **Aluminium**
  - **Copper**
  - **Gold**
  - **Iron**
  - **Lead**
  - **Mercury**
  - **Platinum**
  - **Silver**
  - **Titanium**
- Sorted color groups from lightest to darkest after the base color

## [1.4.5] - 2022-07-20

### Changed

- Renamed **QMM Mercury Liquid** to **QMM Mercury**
- Updated **Cinnabar**
  - Added **Vermillion** Color Ramp
- Updated **Glass Hack**
  - Changed `Transparent Shader > Color` to `F3F3FF`
- Reordered **Noble Metals** submenu
  - Alphabetized **Palladium** and **Platinum**

### Fixed

- Fixed Bump Node input assignment for:
  - **Asphalt**
  - **Asphalt Bleached**
  - **Plaster**

## [1.4.4] - 2022-05-05

### Added

- Added **Cinnabar**

## [1.4.3] - 2022-05-01

### Changed

- Changed **Add-On Updater** to manual installation

## [1.4.2] - 2022-04-30

### Added

- Added **Roughness** input to **Texturizer**
- Added outputs:
  - **Rough Ceiling**
  - **Roughness**
  - **Rough Floor**
  - **Height**

### Changed

- Updated **Texturizer**
  - Changed color/noise color mix from `OVERLAY` to `MULTIPLY`

## [1.4.1] - 2022-04-26

### Added

- Added **Wall Paint**

### Changed

- Tweaked layout of links in add-on preferences
- Attempted to repair **Add-On Updater** installation

## [1.4.0] - 2022-04-22

### Added

- Added:
  - **Asphalt**
  - **Asphalt Bleached**
  - **Palladium**
  - **Platinum**
  - **Titanium Polished**

### Changed

- Renamed:
  - **Brass Metallic** to **Brass**
  - **Copper Min** to **Copper**
  - **Silver Min** to **Silver**
  - **Titanium** to **Titanium Textured**
- Updated **Plaster** so its material color can be changed by **PCOY**, **MCMC**, **HG71**, and **F58**

### Removed

- Removed:
  - **Copper Max**
  - **Pale Gold**
  - **Pale Silver**
  - **Silver Max**

## [1.3.8] - 2022-04-14

### Added

- Added **Dontnod Copper** to **Copper Color**
- Added **Titanium Color** group with:
  - **Titanium**
  - **Pale Titanium**
  - **Dark Titanium**
  - **Metallic Titanium**
  - **Titanium White**
  - **Titanium Frost**
  - **Titanium Blue**
- Added **Texturizer** node group with `Color` and `Normal` outputs affecting **Titanium**

### Changed

- Updated **Titanium** `Roughness`

## [1.3.7] - 2022-04-01

### Changed

- Updated IOR values for:
  - **Aluminium**
  - **Iron**
  - **Titanium**

## 1.3.6 - 2022-03-23

### Added

- Added **Pirate Gold** to **Gold Color**

## [1.3.5] - 2022-03-14

### Changed

- Updated `Roughness` values for:
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

## [1.3.4] - 2022-01-02

### Added

- Added **Gold Color** group with:
  - **Gold**
  - **Pale Gold**
  - **Golden Gold**
  - **Old Gold**
  - **Golden Yellow**
  - **Golden Poppy**
  - **Crayola Gold**
  - **Vegas Gold**
  - **Satin Sheen Gold**
- Added **Silver Color** group with:
  - **Silver**
  - **Pale Silver**
  - **Basic Silver**
  - **Crayola Silver**
  - **Silver Pink**
  - **Silver Sand**
  - **Silver Chalice**
  - **Roman Silver**
  - **Old Silver**
  - **Sonic Silver**

### Fixed

- Changed node group output type from `Float` to `Color`

## [1.3.3] - 2021-12-30

### Added

- Added **Copper Color** group with:
  - **Copper**
  - **Pale Copper**
  - **Copper Red**
  - **Copper Penny**
  - **Copper Rose**

### Fixed

- Fixed **Specular** group being added twice

## [1.3.2] - 2021-12-29

### Changed

- Combined `IOR/Specular` math nodes into **Specular** group

## [1.3.1] - 2021-12-21

### Changed

- Moved material files into subfolders

## [1.3.0] - 2021-12-15

### Changed

- Added Blender 3.0 compatibility
- Updated node input IDs
- Connected `IOR` value node to **Principled BSDF** `IOR` input

## 1.2.3 - 2021-12-15

### Changed

- Shortened material variable names
  - Example: `material_aluminium` to `m_aluminium`
- Changed `bl_category` from **QMM** to **MAT**

## [1.2.2] - 2021-08-12

### Changed

- Tweaked UI layout of QMM panel
- Tweaked UI layout of **Additional Resources** in preferences

## [1.2.1] - 2021-07-24

### Added

- Added **Additional Resources** links to preferences panel

## [1.2.0] - 2021-07-14

### Added

- Added:
  - **Chrome**
  - **Lead**
  - **Lead Rough**

### Changed

- Split **Base Metals & Alloys** into two submenus
- Set Metallic and Roughness on Viewport Display
- Cleaned up code

## [1.1.1] - 2021-07-08

### Added

- Added tooltips to buttons
- Added `IOR` label to Value node connected to **Principled BSDF** Specular input

### Changed

- Set IOR value on all Principled BSDF nodes

## 1.1.0 - 2021-06-17

### Added

- Added **Tinted Plaster**

## [1.0.0]

### Added

- Added [**CG Cookie's Addon Updater**](https://github.com/CGCookie/blender-addon-updater)

### Changed

- Corrected version numbering system
- Cleaned up code

## [0.0.4] - 2021-03-22

### Added

- Added:
  - **Pale Gold Metallic**
  - **Pale Silver Metallic**
  - **Rubber Cutting Mat**

### Changed

- Added `QMM` prefix to classes to resolve naming conflicts with other shader add-ons

## [0.0.3] - 2021-03-21

### Changed

- Moved categories into subpanels
- Changed **Category** to `Material`
- Changed Blender compatibility to 2.83

## [0.0.2] - 2021-03-10

### Added

- Added error checking for existing materials

## 0.0.1 - 2021-03-09

### Added

- Created materials:
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

[1.24.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.24.0
[1.23.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.23.0
[1.22.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.22.1
[1.22.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.22.0
[1.21.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.21.0
[1.19.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.19.0
[1.18.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.18.0
[1.17.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.17.0
[1.16.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.16.0
[1.14.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.14.0
[1.13.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.13.0
[1.12.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.12.0
[1.11.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.11.0
[1.10.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.10.0
[1.9.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.9.0
[1.8.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.8.0
[1.6.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.6.0
[1.5.8]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.8
[1.5.7]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.7
[1.5.6]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.6
[1.5.5]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.5
[1.5.4]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.4
[1.5.3]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.3
[1.5.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.1
[1.5.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.5.0
[1.4.9]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.9
[1.4.8]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.8
[1.4.7]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.7
[1.4.6]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.6
[1.4.5]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.5
[1.4.4]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.4
[1.4.3]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.3
[1.4.2]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.2
[1.4.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.1
[1.4.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.4.0
[1.3.8]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.8
[1.3.7]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.7
[1.3.5]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.5
[1.3.4]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.4
[1.3.3]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.3
[1.3.2]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.2
[1.3.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.1
[1.3.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.3.0
[1.2.2]: https://github.com/don1138/blender-qmm/releases/tag/v1.2.2
[1.2.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.2.1
[1.2.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.2.0
[1.1.1]: https://github.com/don1138/blender-qmm/releases/tag/v1.1.1
[1.0.0]: https://github.com/don1138/blender-qmm/releases/tag/v1.0.0
[0.0.4]: https://github.com/don1138/blender-qmm/releases/tag/v0.0.4
[0.0.3]: https://github.com/don1138/blender-qmm/releases/tag/v0.0.3
[0.0.2]: https://github.com/don1138/blender-qmm/releases/tag/v0.0.2