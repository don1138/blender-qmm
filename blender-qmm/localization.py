import bpy

langs = {
    'quick_metal_materials': {
        'en': 'Quick Metal Materials',
        'zh': '快速金属材料'
    },
    'noble_metals': {
        'en': 'Noble Metals',
        'zh': '贵族金属'
    },
    'gold': {
        'en': 'Gold',
        'zh': '黄金'
    },
    'gold_fresnel': {
        'en': 'Gold Fresnel',
        'zh': '菲涅尔金'
    },
    'palladium': {
        'en': 'Palladium',
        'zh': '钯金'
    },
    'platinum': {
        'en': 'Platinum',
        'zh': '铂金'
    },
    'silver': {
        'en': 'Silver',
        'zh': '银'
    },
    'silver_fresnel': {
        'en': 'Silver Fresnel',
        'zh': '菲涅尔银'
    },

    'base_metals': {
        'en': 'Base Metals',
        'zh': '基础金属'
    },
    'aluminium': {
        'en': 'Aluminium',
        'zh': '铝'
    },
    'copper': {
        'en': 'Copper',
        'zh': '铜'
    },
    'copper_fresnel': {
        'en': 'Copper Fresnel',
        'zh': '菲涅尔铜'
    },
    'iron': {
        'en': 'Iron',
        'zh': '铁'
    },
    'lead': {
        'en': 'Lead',
        'zh': '铅'
    },
    'lead_rough': {
        'en': 'Lead Rough',
        'zh': '粗糙铅'
    },
    'nickel': {
        'en': 'Nickel',
        'zh': '镍'
    },
    'tin': {
        'en': 'Tin',
        'zh': '锡'
    },
    'titanium_polished': {
        'en': 'Titanium Polished',
        'zh': '抛光钛'
    },
    'titanium_textured': {
        'en': 'Titanium Textured',
        'zh': '纹理钛'
    },
    'zinc': {
        'en': 'Zinc',
        'zh': '锌'
    },

    'alloys': {
        'en': 'Alloys',
        'zh': '合金'
    },
    'brass': {
        'en': 'Brass',
        'zh': '黄铜'
    },
    'bronze': {
        'en': 'Bronze',
        'zh': '青铜'
    },
    'chrome': {
        'en': 'Chrome',
        'zh': '铬'
    },
    'steel': {
        'en': 'Steel',
        'zh': '钢'
    },

    'extras': {
        'en': 'Extras',
        'zh': '额外的'
    },
    'asphalt': {
        'en': 'Asphalt',
        'zh': '沥青'
    },
    'asphalt_bleached': {
        'en': 'Asphalt Bleached',
        'zh': '白沥青'
    },
    'glass_hack': {
        'en': 'Glass Hack',
        'zh': '玻璃投影'
    },
    'mercury': {
        'en': 'Mercury',
        'zh': '水银'
    },
    'red_metal': {
        'en': 'Red Metal',
        'zh': '红金属'
    },
    'rubber_cutting_mat': {
        'en': 'Rubber Cutting Mat',
        'zh': '橡胶切割垫'
    },
    'tinted_plaster': {
        'en': 'Tinted Plaster',
        'zh': '着色的石膏'
    },
    'wall_paint': {
        'en': 'Wall Paint',
        'zh': '墙面漆'
    },
}


# LOCALIZATION
def loc_str(str_key, def_locale_key='en'):
    if str_key in langs:
        locale_key = bpy.app.translations.locale
        if locale_key in langs[str_key]:
            return langs[str_key][locale_key]
        else:
            return langs[str_key][def_locale_key]
    else:
        return 'ERR: no such string in localization'
