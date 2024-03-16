# -*- coding:utf-8 -*-
import random
from enum import IntEnum

angle = ["view from above", "view from behind", "view from below", "view from side", "straight-on", "pov", "dutch angle"]

depth = ["atmospheric perspective", "wide angle", "panorama", "perspective", "vanishing point", "wide shot"]

body_framing = ["face", "portrait", "upper body", "lower body", "cowboy shot", "close-up", "half body",
                "3/4 shot", "feet out of frame", "profile"]

focus = ["ass focus", "back focus", "breast focus", "eye focus", "face focus", "hip focus", "navel focus",
         "pectoral focus", "thigh focus"]

beautifier = ["young", "cute", "monster", "japanese", "school", "fox", "demon", "cat", "magical", "18yo", "short",
              "extremely detailed beautiful", "dragon", "young cute beautiful 18-year-old", "little", "pure innocent",
              "irresistable", "slim", "portrait of stunning beauty", "mature", "slender", "german",
              "21years old pretty hungarian", "pretty", "teenage", "sexy", "colorful beautiful", "european", "elf", "kawaii",
              "fitness", "vampire", "blonde", "a beautiful young", "MILF", "fashion"]

legwear_main = ["thighhighs", "fishnets", "kneehighs", "over-kneehighs"]

legwear_style = ["aran", "bow", "cross-laced", "fishnet", "fluffy", "frilled", "knit", "lace", "lace-up",
                 "latex", "bell", "o-ring", "pleated", "ribbed", "ribbon", "seamed", "back-seamed",
                 "front-seamed", "side-seamed", "see-through", "shiny", "side-tie", "spiked", "studded", "toeless",
                 "bridal", "stirrup", "trimmed", "fur-trimmed", "lace-trimmed", "ribbon-trimmed", "zipper",
                 "animal ear", "torn", "mismatched", "naked"]

legwear_color = ["red", "black", "blue", "grey", "white", "gradient", "multicolored", "two-tone", "flesh-colored", "nude"]

dress_color = ["black", "blue", "pink", "purple", "white", "multicolored", "two-tone", "red"]

dress_type = [
    "armored dress", "backless dress", "crinoline", "collared dress", "frilled dress", "fur-trimmed dress",
    "half-dress", "halter dress", "highleg dress", "high-low skirt", "hobble dress", "impossible dress",
    "lace-trimmed dress", "latex dress", "layered dress", "long dress", "off-shoulder dress", "pleated dress",
    "plunging neckline dress",
    "ribbed dress", "ribbon-trimmed dress", "short dress", "side slit dress", "taut dress", "see-through dress",
    "sleeveless dress", "strapless dress", 'cake dress', 'china dress', 'coat dress', 'cocktail dress', 'denim dress',
    'dirndl', 'evening gown', 'flowing dress', 'funeral dress', 'gown', 'mermaid dress', 'negligee', 'nightgown',
    'pencil dress', 'pinafore dress', 'sailor dress', 'santa dress', 'sundress', 'sweater dress', 'tennis dress',
    'trapeze dress', 'tube dress', 'vietnamese dress', 'wedding dress']

top_shirts = [
    "collared shirt", "college shirt", "dress shirt", "flapper shirt", "gym shirt", "rash guard", "t-shirt", "v-neck",
    "impossible shirt"]

top_coat = ['duffel coat', 'fur coat', 'fur-trimmed coat', 'long coat', 'overcoat', 'peacoat', 'raincoat',
            'yellow raincoat', 'transparent raincoat', 'trench coat', 'winter coat']

top_sweater = ['sweater', 'pullover', 'turtleneck', 'sleeveless turtleneck', 'sweater dress', 'ribbed sweater',
               'aran sweater']

top_others = ["tank top", "tube top", "bandeau", "underbust", "vest", "sweater vest", "waistcoat", "camisole",
              "crop top"]

uniforms = ["apron", "armor", "armored dress", "bikini armor", "band uniform", "cape", "capelet", "hood",
            "shoulder cape", "cassock", "cheerleader", "costume", "ghost costume", "gym uniform", "buruma",
            "habit", "harem outfit", "loincloth", "hazmat suit", "hev suit", "kigurumi", "maid",
            "miko", "nontraditional miko", "military uniform", "overalls", "pajamas", "pilot suit", "plugsuit",
            "sailor (naval uniform)", "santa costume", "school uniform", "serafuku (sailor uniform)",
            "sailor dress", "gakuran", "meiji schoolgirl uniform", "shosei", "suit", "business suit",
            "pant suit", "skirt suit", "tuxedo", "track suit", "sweatpants", "sweater", "tutu", "waitress"]

bodysuits = ["bikesuit", "racing suit", "bodystocking", "bodysuit", "jumpsuit", "short jumpsuit", "leotard",
             "strapless leotard", "playboy bunny", "swimsuit", "competition swimsuit", "slingshot swimsuit",
             "school swimsuit", "bikini", "leaf bikini", "string bikini", "micro bikini", "side-tie bikini bottom",
             "lowleg bikini", "thong bikini", "venus bikini", "sports bikini", "tankini", "criss-cross halter",
             "swim briefs (speedo)", "jammers", "legskin", "rash guard", "robe", "bathrobe", "open robe", "kesa",
             "romper", "sarong", "tunic", "unitard"]

traditional_clothes = ["chinese clothes", "changpao", "china dress", "fengguan", "hanfu", "longpao",
                       "tangzhuang", "dirndl", "japanese clothes", "fundoshi", "yamakasa", "hakama",
                       "hakama skirt",
                       "hakama short skirt", "hakama pants", "kimono", "furisode", "layered kimono", "short kimono",
                       "uchikake (wedding kimono)", "yukata", "haori", "happi", "chanchanko", "dotera", "hanten",
                       "kimono skirt", "miko", "nontraditional miko", "sarashi", "Midriff sarashi", "Chest sarashi",
                       "Budget sarashi", "Undone sarashi", "straw cape (mino)", "mino boushi", "tabi", "tasuki",
                       "korean clothes"]

bottom_skirts = ["bubble skirt", "belt skirt", "bikini skirt", "bow skirt", "checkered skirt",
                 "denim skirt", "frilled skirt", "grass skirt", "hakama short skirt", "half-skirt",
                 "high-low skirt", "hoop skirt", "kimono skirt", "layered skirt", "long skirt",
                 "microskirt", "miniskirt", "overskirt", "plaid skirt", "pleated skirt", "pencil skirt",
                 "showgirl skirt", "side-tie skirt", "skirt suit", "skirt set", "spank skirt", "suspender skirt"]

bottom_pants = ['plaid pants', 'pinstripe pants', 'bell-bottoms', 'capri pants', 'harem pants', 'jeans',
                'leather pants', 'pant suit', 'detached pants', 'pants rolled up', 'tight pants', 'single pantsleg']

bottom_shorts = ['shorts', 'bike shorts', 'denim shorts', 'dolphin shorts', 'gym shorts', 'lowleg shorts',
                 'micro shorts', 'short shorts', 'shorts under skirt']

clothes_trim = ["flower trim", "frills", "gold trim", "lace trim", "ribbon trim", "silver trim"]

bSize = ["large breasts", "medium breasts", "huge breasts", "gigantic breasts"]

expression_emo = ["annoyed", "blush", "bored", "closed eyes", "confused", "crazy", "cry", "disappointed", "disdain",
                  "disgust", "despair", "drunk", "envy", "evil", "flustered", "furrowed brow", "guilt", "nervous",
                  "one eye closed", "rape face", "sleepy", "wince"]

expression_sexual = ["afterglow", "ahegao", "fucked silly", "aroused", "naughty face", "torogao"]

expression_smile = ["smile", "light smile", "seductive smile", "evil smile", "slight smile", "cute smile", "shy smile",
                    "sweet smile", "happy smile", "naughty smile", "beautiful smile", "sexy smile", "kind smile"]

expression_smug = ['doyagao', 'smirk', 'smug', 'troll face']

hairColor = ["platinum hair", "raven black hair", "purple hair", "pink hair", "aqua hair", "blonde hair", "blue hair",
             "red hair", "brown hair", "green hair", "grey hair", "multicolored hair", "bleached hair", "gradient hair",
             "two-tone hair"]

hair_style = ["colored inner hair", "pixiecut hairstyle", "expressive hair", "floating hair", "messy_hair",
              "shiny_hair", "wet hair", "hair strand", "crystals texture hair", "wavy hair", "ponytail"]

hairLength = ["long", "shaved", "buzzcut", "short", "medium"]

hair_others = ["bangs", "hair between eyes", "blunt bangs", "side blunt bangs"]

eye_wear = ["bookish glasses", "steampunk goggles", "sunglasses"]

eyeColor = ["hazel", "green", "brown", "black", "grey", "purple", "pink",
            "red", "ice", "white", "sapphire", "turquoise", "amethyst", "aquamarine", "ruby", "coral",
            "peach", "gold", "dark brown", "jade", "teal", "ice blue", "light blue", "blue", "grey-blue",
            "amber"]

eye_others = ["eyelashes", "big eyes", "dark eyeliner", "bright eyes", "red eyeshadow", "beautiful detailed eyes"]

# Except for headwear, earrings, neck ornaments, other ornaments (hand ornaments, waist, foot ornaments, chest ornaments, hip, foot) random combination
hair_accessories = ["hair ornament", "hair tie", "hairband", "hair ribbon", "flower hair ornament",
                    "star hair ornament", "bell hair ornament", "butterfly hair ornament", "feather hair ornament",
                    "leaf hair ornament"]
neck_accessories = [
    "neckerchief", "necklace", "chain necklace", "flower necklace", "pearl necklace", "pendant", "neck ribbon",
    "neck tassel", "charm", "beads", "choker"]

earrings = ["hoop earrings", "stud earrings", "earclip", "earrings", "ear piercing"]

other_accessories = [
    # head
    ["crown", "forehead jewel", "circlet", "head chain", "chain headband", "headpiece", "tiara"],
    # hand
    ["bracelet", "ring", "wedding ring", "red and gold bracelets"],
    # arms
    ["wristband", "arm belt", "wrist cuffs"],
    # leg
    ["leg belt", "leg ribbon", "leg chain", "leg wrap", "thigh strap", "thigh ribbon", "o-ring thigh strap", "leg ring",
     "leg ornament"],
    # foot
    ["anklet", "ankle band", "ankle ring", "ankle buckle", "ankle nail", "ankle bracelet"],
    # Waist waist, navel piercing is excellent, and several other effects are almost the same    
    ["waist ribbon", "waist jewelry", "waist chain", "waist rope", "navel piercing", "sash", "narrow waist"],
    # torso and others
    ["boutonniere", "brooch", "corsage", "suspenders", "tassel", ],
]

shoes_boots = ['boots', 'ankle boots', 'platform boots', 'knee boots', 'high heel boots', 'lace-up boots',
               'rubber boots', 'thigh boots', 'cowboy boots', 'jackboots']

shoes_high_heels = ["stilletto heels"]

shoes_sandals = ['sandals', 'clog sandals', 'cross-laced sandals', 'flip-flops', 'gladiator sandals', 'geta', 'okobo',
                 'waraji', 'zouri']

shoes_slippers = ['slippers', 'animal slippers', 'ballet slippers', 'crocs', 'uwabaki']

background_view = ["cityscapes", "landscape", "architecture", "barg kalifa dubai", "nature", "machu pichu", "outdoors", 
                   "indoors", "messy room", "seascape", "shrine", "pagoda", "temple", "far out space", "east asian architecture", "japanese garden"]

place = ["ancient greece", "alien planet", "spaceship", "american farm", "hell",
         "high school", "locker room", "bedroom", "dungeon", "castle", "classroom", "bathroom",
         "public park", "church", "closet", "toilet stall", "laboratory", "prison cell", "living room",
         "bathtub", "library", "stage", "kitchen", "office", "infirmary",
         "fitting room", "hotel room", "onsen", "pool", "skyscraper", "shrine", "rooftop", "restaurant",
         "windmill", "hospital", "apartment", "field", "bridge", "poolside", "street", "path",
         "garden", "ferris wheel", "otaku room", "conservatory", "fountain", "pier", "village", "beach", "cave",
         "mountain", "forest", "countryside", "desert", "jungle", "ocean", "river", "lake", "waterfall",
         "island"]

#### pose There are many types

pose_base = ["kneeling", "lying", "sitting", "standing"]
pose_base_child = {
    "kneeling": ["on one knee"],
    "lying": ['crossed legs', 'fetal position', 'on back', 'on side', 'on stomach'],
    "sitting": ["butterfly sitting", "crossed legs", "figure four sitting", "indian style", "hugging own legs",
                "lotus position", "seiza", "sitting on lap", "sitting on person", "straddling", "thigh straddling",
                "upright straddle", "wariza", "yokozuwari"],
    "standing": ["balancing", "crossed legs", "legs apart", "standing on one leg"]
}
pose_whole = ["all fours", "reclining", "squatting", "stretching", "yoga"]
pose_legs = ["crossed legs", "legs up", "leg up", "spread legs", "crossed ankles", "outstretched leg", "watson cross"]
pose_arms = ["arms behind back", "arms behind head", "arms up", "arm up", "arm support", "arm at side"]
pose_hands = ["hand on own ear", "hand on headwear", "hand on own chest", "hands on own hips", "hand on own shoulder",
              "breast hold", "breast lift", "breasts squeezed together", "arm between breasts", "hand in bra",
              "nipple tweak", "hands on ass", "hand between legs"]

# These tags don't imply nudity, but are related to some other tags above.
pose_touching_clothes = ['adjusting clothes', 'clothes grab', 'apron grab', 'collar grab', 'necktie grab', 'skirt grab',
                         'collar tug', 'dress tug', 'shirt tug', 'skirt tug', 'wringing clothes']

jobs = ["catgirl", "young innocent", "slut", "princess", "succubus", "mother superior",
        "librarian", "schoolgirl", "cheerleader", "prostitute", "kitsune", "kyuubi", "magic girl",
        "mage", "demon", "angel", "student", "elf", "fairy", "fox girl", "goddess", 'alchemist',
        'bartender', 'butler', 'croupier', 'dentist', 'dj', 'doctor', 'dominatrix', 'flight attendant',
        'florist', 'geisha', 'maid', 'miko', 'nun', 'nurse', 'school nurse', 'office lady',
        'prostitution', 'sailor', 'stripper', 'teacher', 'waitress', 'witch', "mermaid", "vampire", "dancer",
        "dominatrix", "female pervert", "gyaru", "idol"]

######## Objects ##########

objects_list = [
    # religion symbols
    ["mandala", "srivatsa", "cross", "star and crescent", "star of david", "dharmachakra", "om", "ankh", "bagua",
     "ichthys", "kaaba", "padma", "pentagram", "allah", "amsden’s circle"],
    # flower and some nice objects
    ["flower", "ice flower", "fire flower", "black lotus", "lunar tear", "silk flower", "petals", "lily", "poppy",
     "rose", "tulip", "snowdrop", "dandelion"],
    # element
    ["ice", "fire", "water", "lightning", "wind"],
    ["metal", "wood", "stone", "sand", "glass", "fur", "feather", "blood", "gold", "steam", "smoke", "crystal",
     "bubble", "foam", "ash", "mercury"],
    # chain
    ["chain jewelry", "chain collar", "chain leash", "chainlink fence", "pinheadchains", "chain piercing"],
    # Fantasy and elements
    ["arcane", "celestial", "aether", "crystalline", "aurora", "ember", "sylph", "obsidian", "radiance", "verdant",
     "ecliptic", "nebula"],
    # confusion
    ["chaos", "disorderly", "pandemonium", "tumultuous", "havoc", "entropy", "disarray"],
    # hell
    ["hell", "abyssal", "infernal", "damnation", "purgatorial", "tartarean", "hades", "sheol", "perdition",
     "underworldly", "gehenna"],
]

suffix_beautiful = ["radiant", "ethereal", "luminous", "vivid", "glowing", "elemental", "celestial", "pristine",
                    "splendid", "enchanting", "charming", "elegant", "gorgeous", "aesthetic", "exquisite", "beautiful",
                    "whimsical", "fantastical", "enigmatic", "quixotic", "surreal", "peculiar", "imaginative"]

day_time = ["evening", "night", "morning", "sunrise", "sunset", "twilight", "moonlit night"]

weather = ["blizzard", "blue sky", "cloudy sky", "fog", "rain", "snow", "mist"]

body_status = ["wet", "sweat"]

body_with = ["zentangle", "entangled", "chained", "bondage", "handcuffs", "leash", "ribbon bondage", "braid"]

body_desc_list = ["perfect body", "slim body", "perfect female body", "slender body", "soaked body", "steaming body"]

body_skin = ["shiny skin", "smooth skin", "soft skin", "glowing skin", "flawless skin", "porcelain skin",
             "luminous skin"]

details = ["elaborate", "ornate", "intricate", "detailed", "fine", "refined",
           "complicated", "convoluted", "extensive", "exhaustive", "far-reaching", "informative",
           "in-depth", "thorough", "step-by-step", "exact", "precise", "exquisite", "lavish",
           "sumptuous", "opulent", "luxurious", "intricately designed", "grandiose", "stately",
           "splendid", "magnificent", "precious", "dazzling", "imperceptible detail", "fantasy illustration"]

image_techniques = ["bloom", "bokeh", "caustics", "chiaroscuro", "diffraction spikes", "depth of field", "film grain",
                    "foreshortening", "gradient", "lens flare", "motion blur",
                    ]

light_effects = ["cinematic lighting", "soft lighting", "perfect lighting", "volumetric lighting", "dramatic lighting",
                 "natural lighting", "sunlight", "rim lighting", "studio lighting", "beautiful lighting",
                 "sidelighting", "light on face", "natural volumetric lighting and best shadows", "neon lights",
                 "vivid vibrant glowing neon toxic colors"]

color_list = ["colorful", "vibrant colors", "vivid colors", "bright colors", "pastel colors", "neon colors"]

############ sexual collection ############

sexual_lingerie = ['lingerie', 'babydoll', 'bodystocking', 'bra', 'bustier', 'camisole', 'chemise', 'corset',
                   'fishnets', 'garter straps', 'garter belt', 'lace', 'nightgown', 'panties', 'boyshort panties',
                   'strapless bottom', 'teddy', 'thong', 'g-string', 'pearl thong']
sexual_crotchless = ['crotchless', 'crotchless panties', 'crotchless pants', 'crotchless swimsuit',
                     'crotchless pantyhose', 'crotchless leotard', 'crotchless bloomers', 'crotchless buruma']
sexual_ass_cutout = ['ass cutout', 'assless swimsuit', 'backless panties', 'backless pants']
sexual_breastless = ['breastless clothes', 'nippleless clothes', 'cupless bikini', 'cupless bra']
sexual_miscellaneous = ["anal ball wear", "maebari", "pasties"]
sexual_common = ["revealing clothes", "see-through", "cleavage"]

############ uncensored collection ############

uncensored_list = ["convenient leg", "hair over breasts", "hair over crotch", "hair over one breast", "covering face"]


##### nsfw/sex collection ############

class SexActType(IntEnum):
    SEX = 1
    STIMULATION = 2
    GROUP = 3
    TENTACLES = 4


sex_act_stimulation = ["footjob", "feet", "armpit", "grinding", "kneepit", "paizuri", "thigh", "handjob",
                       "masturbation", "oral"]

sex_act_group = ["love train", "cooperative fellatio", "cooperative footjob", "cooperative breast smother", "orgy",
                 "reverse spitroast", "spitroast", "teamwork", "MMF threesome", "FFM threesome"]

sex_act_tentacles = []

sex_category = [
    ["groping", "handjob", "masturbation", "tail", "oral", "hug and suck",
     "licking testicle", "sitting on face", "sitting on face"],
    ["group sex", "bisexual", "bisexual female", "daisy chain", "gangbang", "double penetration",
     "triple penetration" "love train", "cooperative fellatio", "cooperative footjob", "multiple breast smother",
     "orgy", "reverse spitroast", "spitroast", "teamwork", "threesome"],
    ["after sex", "after anal", "after buttjob", "after fellatio", "after fingering",
     "after insertion", "after masturbation", "after oral", "after paizuri", "after rape", "after urethral",
     "after vaginal", "afterglow", "clothed after sex", "anal", "double anal", "imminent anal", "pegging",
     "clothed sex", "guided penetration", "happy sex", "imminent penetration", "implied sex",
     "sex from behind", "skull fucking", "penis in eye", "underwater sex",
     "vaginal", "after vaginal", "double vaginal", "imminent vaginal"],
    ["cum", "cum on body", "cum on breasts", "cum on clothes", "cum on eyewear", "cum on food", "ejaculation", "ejaculating while penetrated", "pull out", "facial", "autofacial"]
]

sex_positions_reload = [
    "view from behind, pov", "breast grab, pov", "grabbing own breast", "cheek bulge:1.4, fellatio", "lying, pov",
    "lying, on side, pov", "lying, leg up, on side, pov",
    "cowgirl position, pov", "squatting cowgirl position, pov",
    "doggystyle, pov, from side, standing", "doggystyle, fellatio", "fellatio, pov, from side",
    "imminent penetration, missionary, cowgirl position, squatting cowgirl position",
    "Jack'O Challenge, sex from behind, deep penetration", "licking penis, tongue, open mouth",
    "lying, leg lift, lef up, on side", "missionary, pov, legs up", "paizuri, penis",
    "piledrive position", "prone bone, from side", "suspended congress", "standing, split legs, leg lift",
    "x-ray cervix, cross-section, internal cumshot, cum",
    "aftersex, ass, cum in pussy, cum in face, fellatio, missionary, buttjob",
    "guided breast grab, pov, guiding hand, breast grab, holding another's wrist",
]

sex_place = ["mountain", "bathtub", "bedroom", "classroom", "bathroom", "public park", "office"]

sex_man_type = ["1boy", "a water elemental"]

nude_list = [
    # Any clothes
    ["clothing aside", "clothes down", "open clothes", "revealing clothes", "see-through", "unbuttoned", "undressing",
     "unfastened", "untied", "untying", "unzipped", "unzipping"],
    # Misc / Specific exposures that could fit multiple categories below
    ["bikini bottom aside", "bikini pull", "cape lift", "lifting covers", "open bikini", "open bra", "open kimono",
     "robe slip", "strap lift", "strap pull", "strap slip", "swimsuit aside", "one-piece swimsuit pull", "open towel",
     "towel slip", "male underwear pull"],
    # Exposed chest
    ["center opening", "open coat", "open collar", "dress pull", "open hoodie", "open jacket", "leotard pull",
     "kimono down", "kimono pull", "pajamas pull", "open robe", "shirt aside", "topless male", "no shirt",
     "open shirt", "shirt lift", "shirt pull", "shirt slip", "sweater lift", "top pull", "open vest"],
    # Exposed breasts
    ["breastless clothes", "one breast out", "breast slip", "breasts out", "bra lift", "no bra", "bra pull", "topless"],
    # Exposed parts of breasts
    ["backboob", "cleavage", "cleavage cutout", "sideboob", "underboob", "underboob cutout"],
    # Exposed nipples
    ["areola slip", "nipple slip", "nippleless clothes", "nipples", "nipple piercing", "nipple chain",
     "nipple jewelry"],
    # Exposed torso
    ['back cutout', 'backless outfit', 'bare back', 'frontless outfit', 'midriff', 'navel cutout', 'side cutout',
     'sideless outfit', 'stomach cutout', 'waist cutout'],
    # Focus on exposed legs or feet
    ["barefoot", "bare legs", "dress lift", "hip vent", "leg cutout", "thigh cutout", "side slit", "no pants",
     "shoe pull", "sock pull", "zettai ryouiki"],
    # Focus on exposed ass or crotch
    ["ass cutout", "bottomless", "buruma pull", "buruma aside", "clitoris slip", "clothing aside", "crotch cutout",
     "dress aside", "leotard aside", "hakama pull", "kimono lift", "yukata lift", "no panties", "panties aside",
     "pants pull", "open pants", "pants pull", "panty lift", "panty pull", "pussy peek", "pantyhose pull",
     "shorts aside", "shorts, open", "shorts pull", "skirt around one leg", "skirt around ankles", "open skirt",
     "skirt pull", "skirt lift", "swimsuit aside", "bikini bottom aside"],
    # Dressing / Covering body parts
    ['covering', 'covering anus', 'covering ass', 'covering breasts', 'covering crotch', 'covering head',
     'covering own ears', 'covering one eye', 'covering own eyes', 'covering face', 'covering mouth', 'nude cover'],
]

# Specific clothes or ornaments being worn as exceptions
nude_clothes = ["clothesnaked apron", "nearly naked apron", "naked bandage", "naked cape", "naked capelet",
                "naked cloak", "naked coat", "naked hoodie", "naked jacket", "naked overalls",
                "naked ribbon", "naked robe", "naked scarf", "naked sheet", "naked shirt", "naked suspenders",
                "naked tabard", "naked towel", "underwear only"]

panties_list = ["bow panties", "crotch seam", "frilled panties", "side-tie panties", "string panties",
                "stained panties", "wet panties", "backless panties", "c-string", "crotchless panties",
                "loose panties", "micro panties", "lowleg panties", "highleg panties"]


def get_realistic_prompt():
    if get_config_value_by_key("is_realistic"):
        return "(realistic, photorealistic), "
    else:
        return ""


def get_angle_and_image_composition():
    current_prompt = ""
    if check_config_value_is_not_none("angle"):
        current_prompt = get_assignment_prompt("angle")
    else:
        if get_config_value_by_key("dynamic_mode"):
            current_prompt = current_prompt + "dynamic angle, "
        else:
            current_prompt = current_prompt \
                             + get_standard_prompt(angle)
            if check_chance(0.7):
                current_prompt = current_prompt + get_standard_prompt(depth)

    if check_config_value_is_not_none("body_framing"):
        current_prompt = current_prompt \
                         + get_assignment_prompt("body_framing")
    else:
        current_prompt = current_prompt \
                         + get_standard_prompt(body_framing)

    return current_prompt


def get_focus_prompt():
    current_prompt = ""
    if check_config_value_is_not_none("assign_focus_on"):
        current_prompt = get_assignment_prompt("assign_focus_on")
    elif get_config_value_by_key("add_focus"):
        current_prompt = current_prompt \
                         + get_standard_prompt(focus)
    return current_prompt


def get_girl_desc_prompt():
    if check_config_value_is_not_none("assign_girl_description"):
        return get_assignment_prompt("assign_girl_description")

    girl_cnt = get_config_value_by_key("girl_cnt")
    prompt = "1girl, "
    if girl_cnt == 0:
        return ""
    elif girl_cnt == 1:
        pass
    elif 1 < girl_cnt <= 5:
        prompt = f"{girl_cnt}girls, "
    elif girl_cnt == 6:
        prompt = "6+girls, "
    elif girl_cnt > 6:
        prompt = "multiple girls, "
    if get_config_value_by_key("add_girl_beautyful"):
        return prompt + get_random_from_list(beautifier) + " girl, "

    return prompt


def get_face_expression():
    expression_type = FaceExpression.SMILE
    expression_index = 3
    current_prompt = ""
    if check_config_value_is_not_none("assign_expression"):
        return get_assignment_prompt("assign_expression")

    if check_config_value_is_not_none("face_expression"):
        expression_type = get_config_value_by_key("face_expression")

    if expression_type == FaceExpression.RANDOM:
        expression_index = random.randint(1, 4)
    else:
        expression_index = expression_type

    if expression_index == FaceExpression.SMILE:
        current_prompt = current_prompt \
                         + get_standard_prompt(expression_smile)
    elif expression_index == FaceExpression.EMOTIONS:
        current_prompt = current_prompt \
                         + get_standard_prompt(expression_emo)
    elif expression_index == FaceExpression.SEXUAL:
        current_prompt = current_prompt \
                         + get_standard_prompt(expression_sexual)
    elif expression_index == FaceExpression.SMUG:
        current_prompt = current_prompt \
                         + get_standard_prompt(expression_smug)

    return current_prompt


def get_pose_prompt():
    if check_config_value_is_not_none("assign_pose"):
        return get_assignment_prompt("assign_pose")

    if get_config_value_by_key("dynamic_mode"):
        return "dynamic pose, "

    current_prompt = ""
    pose_type = PoseType.BASE

    if check_config_value_is_not_none("pose_type"):
        pose_type = get_config_value_by_key("pose_type")

    if pose_type == PoseType.BASE:
        base_pose = get_random_from_list(pose_base)
        current_prompt = current_prompt \
                         + base_pose + ", "

        if pose_base_child[base_pose] is not None and check_chance(0.5):
            base_child_list = pose_base_child[base_pose]
            base_child = get_random_from_list(base_child_list)
            current_prompt = current_prompt \
                             + base_child + ", "
    elif pose_type == PoseType.WHOLE:
        current_prompt = current_prompt + get_standard_prompt(pose_whole)

    sub_index = random.randint(-1, 3)
    if sub_index == -1:
        pass
    elif sub_index == 0:
        current_prompt = current_prompt + get_standard_prompt(pose_legs)
    elif sub_index == 1:
        current_prompt = current_prompt + get_standard_prompt(pose_arms)
    elif sub_index == 2:
        current_prompt = current_prompt + get_standard_prompt(pose_hands)
    elif sub_index == 3:
        current_prompt = current_prompt + get_standard_prompt(pose_touching_clothes)

    return current_prompt


def get_legwear_prompt():
    current_prompt_leg = ""

    if check_config_value_is_not_none("assign_leg_wear"):
        current_prompt_leg = "("
        if check_config_value_is_not_none("leg_wear_color"):
            current_prompt_leg = current_prompt_leg \
                                 + get_config_value_by_key("leg_wear_color") + " and "
        current_prompt_leg = current_prompt_leg + get_random_from_list(legwear_style) + " "
        current_prompt_leg = current_prompt_leg \
                             + get_config_value_by_key("assign_leg_wear") \
                             + ":{:.2f}".format(make_prompt_strong_scale) \
                             + "), "
        # return get_assignment_prompt("assign_leg_wear")
        return current_prompt_leg

    legwear_type = LegWearType.PANTYHOSE
    has_assign_color = False

    if check_config_value_is_not_none("leg_wear"):
        legwear_type = get_config_value_by_key("leg_wear")

    if legwear_type == LegWearType.ASNULL:
        return ""
    elif legwear_type == LegWearType.RANDON:
        legwear_type = get_random_from_list(
            [LegWearType.PANTYHOSE, LegWearType.BARE, LegWearType.THIGHHIGHS, LegWearType.KNEEHIGHS,
             LegWearType.OVERKNEEHIGHS, LegWearType.SOCKS])

    current_prompt_leg = current_prompt_leg + "("
    if legwear_type != LegWearType.BARE:
        if check_config_value_is_not_none("leg_wear_color"):
            current_prompt_leg = current_prompt_leg \
                                 + get_config_value_by_key("leg_wear_color") \
                                 + " and "
            has_assign_color = True
        else:
            if get_config_value_by_key("disable_all_color") is False:
                current_prompt_leg = current_prompt_leg \
                                     + get_random_from_list(legwear_color) + " and "

    if legwear_type != LegWearType.BARE:
        current_prompt_leg = current_prompt_leg + get_random_from_list(legwear_style) + " "

    if legwear_type == LegWearType.SOCKS:
        current_prompt_leg = current_prompt_leg \
                             + "socks"
    elif legwear_type == LegWearType.PANTYHOSE:
        current_prompt_leg = current_prompt_leg \
                             + "pantyhose"
    elif legwear_type == LegWearType.KNEEHIGHS:
        current_prompt_leg = current_prompt_leg \
                             + "kneehighs"
    elif legwear_type == LegWearType.OVERKNEEHIGHS:
        current_prompt_leg = current_prompt_leg \
                             + "over-kneehighs"
    elif legwear_type == LegWearType.THIGHHIGHS:
        current_prompt_leg = current_prompt_leg \
                             + "thighhighs"
    elif legwear_type == LegWearType.BARE:
        current_prompt_leg = current_prompt_leg \
                             + "bare legs"

    if has_assign_color and legwear_type != LegWearType.BARE:
        current_prompt_leg = current_prompt_leg \
                             + ":{:.2f}".format(make_prompt_strong_scale)

    current_prompt_leg = current_prompt_leg + "), "

    return current_prompt_leg


def get_shoes_prompt():
    current_prompt = ""
    if check_config_value_is_not_none("assign_shoes"):
        current_prompt = "("
        if check_config_value_is_not_none("shoes_color"):
            current_prompt = current_prompt + get_config_value_by_key("shoes_color") + " "
        current_prompt = current_prompt \
                         + get_config_value_by_key("assign_shoes") \
                         + ":" \
                         + "{:.2f}".format(make_prompt_strong_scale) \
                         + "),"

        return current_prompt

    has_assign_color = False

    shoes_type = FootWearType.HIGHHEELS
    if check_config_value_is_not_none("shoes_type"):
        shoes_type = get_config_value_by_key("shoes_type")

    if shoes_type == FootWearType.ASNULL:
        return ""

    if shoes_type != FootWearType.BARE:
        if check_config_value_is_not_none("shoes_color"):
            current_prompt = current_prompt \
                             + "(" + get_config_value_by_key("shoes_color") \
                             + " "
            has_assign_color = True

    if shoes_type == FootWearType.HIGHHEELS:
        current_prompt = current_prompt \
                         + get_random_from_list(shoes_high_heels)
    elif shoes_type == FootWearType.BOOTS:
        current_prompt = current_prompt \
                         + get_random_from_list(shoes_boots)
    elif shoes_type == FootWearType.SANDALS:
        current_prompt = current_prompt \
                         + get_random_from_list(shoes_sandals)
    elif shoes_type == FootWearType.SLIPPERS:
        current_prompt = current_prompt \
                         + get_random_from_list(shoes_slippers)
    elif shoes_type == FootWearType.BARE:
        current_prompt = current_prompt \
                         + "bare foot"

    if has_assign_color:
        current_prompt = current_prompt \
                         + ":{:.2f}".format(make_prompt_strong_scale) \
                         + "), "
    else:
        current_prompt = current_prompt + ", "
    return current_prompt


def get_ribbon_others():
    current_ribbon_others = ""
    if get_config_value_by_key("cloth_trim"):
        current_ribbon_others = current_ribbon_others + get_standard_prompt(clothes_trim, True)
    return current_ribbon_others


def get_body_with_prompt():
    if get_config_value_by_key("body_with"):
        return get_standard_prompt(body_with, True)
    else:
        return ""


def get_body_status_prompt():
    if get_config_value_by_key("body_status"):
        if get_config_value_by_key("sex_mode") or get_config_value_by_key("nsfw_type") != NSFWType.NOTNSFW:
            body_status.append("cum on body")
            return get_standard_prompt(body_status, True)
        else:
            return get_standard_prompt(body_status, True)
    else:
        return ""


def get_body_description_prompt():
    current_prompt = ""
    if get_config_value_by_key("body_description"):
        current_prompt = current_prompt + get_standard_prompt(body_desc_list)
        current_prompt = current_prompt + "narrow waist, chest jewel, navel, "
    return current_prompt


def get_body_skin_prompt():
    current_prompt = ""
    if get_config_value_by_key("body_skin"):
        current_prompt = current_prompt + get_standard_prompt(body_skin)
        return current_prompt
    else:
        return current_prompt


def get_accessories_mix_prompt():
    random_times = 1
    random_times = get_config_value_by_key("accessories_random_tims")
    if random_times <= 0:
        return ""

    current_accessories_mix = ""
    is_sex = get_config_value_by_key("sex_mode")
    is_nude = get_config_value_by_key("nsfw_type") == NSFWType.NUDE

    random_list = other_accessories.copy()

    if is_sex is not True:
        current_accessories_mix = "("
    if is_nude or is_sex:
        random_list.append(["nipple chain", "nipple piercing"])

    if random_times > len(random_list):
        random_times = len(random_list)
    select_index_list = random_list_no_repeat_number(len(random_list), random_times)
    for v in select_index_list:
        current_accessories_mix = current_accessories_mix \
                                  + get_standard_prompt(random_list[v - 1])

    current_accessories_mix = remove_comma_space(current_accessories_mix)

    if is_sex:
        current_accessories_mix = current_accessories_mix + ", "
    else:
        current_accessories_mix = current_accessories_mix + "), "
    return current_accessories_mix


def get_objects_mix_prompt():
    random_times = get_config_value_by_key("object_random_times")
    if random_times > len(objects_list):
        random_times = len(objects_list)
    current_prompt = ""

    if random_times <= 0:
        return current_prompt
    else:
        select_index_list = random_list_no_repeat_number(len(objects_list), random_times)
        for v in select_index_list:
            current_prompt = current_prompt \
                             + get_standard_prompt(objects_list[v - 1])
        return current_prompt


def get_suffix_beautiful_prompt():
    random_times = get_config_value_by_key("suffix_words_random_times")
    current_prompt = ""
    if random_times <= 0:
        return current_prompt
    else:
        if random_times > len(suffix_beautiful):
            random_times = len(suffix_beautiful)
        select_index_list = random_list_no_repeat_number(len(suffix_beautiful), random_times)
        for v in select_index_list:
            current_prompt = current_prompt \
                             + suffix_beautiful[v - 1] + ", "
        return current_prompt


def get_breasts_size_prompt():
    if check_config_value_is_not_none("breasts_size"):
        size_value = get_config_value_by_key("breasts_size")
        if size_value == "nil" or size_value == "null" or size_value == "none":
            return ""
        return get_config_value_by_key("breasts_size") + " breasts, "
    else:
        return get_standard_prompt(bSize)


def get_panties_prompt():
    current_prompt = ""

    if get_config_value_by_key("panties"):
        if check_config_value_is_not_none("assign_panties"):
            current_prompt = get_assignment_prompt("assign_panties")
        else:
            current_prompt = get_standard_prompt(panties_list)
    return current_prompt


def get_nsfw_prompt():
    nsfw = ""
    if get_config_value_by_key("is_nsfw"):
        nsfw = "(nsfw), "
    return nsfw


def get_uncensored_prompt():
    is_uncensored = get_config_value_by_key("is_uncensored")
    current_prompt = ""
    if is_uncensored:
        current_prompt = "uncensored, "
        current_prompt = current_prompt + get_standard_prompt(uncensored_list)

    return current_prompt


def get_body_wear_prompt():
    body_wear_output = get_pose_prompt()

    nsfw_type = NSFWType.NOTNSFW
    body_wear = BodyWearType.RANDOM
    top_wear = TopWearType.RANDOM
    bottom_wear = BottomWearType.RANDOM

    if check_config_value_is_not_none("nsfw_type"):
        nsfw_type = get_config_value_by_key("nsfw_type")

    if check_config_value_is_not_none("body_wear"):
        body_wear = get_config_value_by_key("body_wear")
    if check_config_value_is_not_none("top_wear"):
        top_wear = get_config_value_by_key("top_wear")
    if check_config_value_is_not_none("bottom_wear"):
        bottom_wear = get_config_value_by_key("bottom_wear")

    if nsfw_type == NSFWType.NUDE:
        body_wear_output = get_body_nude_prompt(body_wear_output)
    elif nsfw_type == NSFWType.SEXUAL:
        body_wear_output = get_body_sexual_prompt(body_wear_output)
    else:
        if check_config_value_is_not_none("assign_body_clothes"):
            return body_wear_output + get_assignment_prompt("assign_body_clothes")

        i = int(body_wear)
        if i == 6:
            i = random.randint(1, 5)

        if i == BodyWearType.DRESS:
            body_wear_output = body_wear_output + "("
            if get_config_value_by_key("disable_all_color") is True:
                body_wear_output = body_wear_output \
                                   + get_random_from_list(dress_type) \
                                   + "), "
            else:
                body_wear_output = body_wear_output \
                                   + get_random_from_list(dress_color) \
                                   + " and " \
                                   + get_random_from_list(dress_type) \
                                   + "), "
        elif i == BodyWearType.UNIFORM:
            body_wear_output = body_wear_output \
                               + get_standard_prompt(uniforms)
        elif i == BodyWearType.BODYSUIT:
            body_wear_output = body_wear_output \
                               + get_standard_prompt(bodysuits)
        elif i == BodyWearType.TRADITIONAL:
            body_wear_output = body_wear_output \
                               + get_standard_prompt(traditional_clothes)
        elif i == BodyWearType.CUSTOM:
            body_wear_output = body_wear_output \
                               + get_top_wear_prompt(top_wear) \
                               + get_bottom_wear_prompt(bottom_wear)

    body_wear_output = body_wear_output \
                       + get_body_skin_prompt() \
                       + get_body_description_prompt() \
                       + get_legwear_prompt() \
                       + get_body_with_prompt() \
                       + get_ribbon_others() \
                       + get_shoes_prompt() \
                       + get_panties_prompt() \
                       + get_focus_prompt()

    return body_wear_output


def get_body_sexual_prompt(body_wear_output):
    # convert sexual_common list to sting with ", "
    sexual_common_str = "("
    sexual_tmp_list = [sexual_lingerie, sexual_crotchless, sexual_ass_cutout, sexual_breastless,
                       sexual_miscellaneous]
    sexual_common_str = sexual_common_str + get_random_from_list(sexual_common) + ", "
    body_wear_output = body_wear_output + sexual_common_str
    sexual_random_times = len(sexual_tmp_list)
    sexual_random_times = get_config_value_by_key("sexual_list_random_index_times")
    if sexual_random_times > len(sexual_tmp_list):
        sexual_random_times = len(sexual_tmp_list)
    elif sexual_random_times <= 0:
        sexual_random_times = 0
    if sexual_random_times > 0:
        select_list = random_list_no_repeat_number(len(sexual_tmp_list), sexual_random_times)
        for v in select_list:
            body_wear_output = body_wear_output + get_standard_prompt(sexual_tmp_list[v - 1])
    body_wear_output = remove_comma_space(body_wear_output)
    body_wear_output = body_wear_output + "), "
    return body_wear_output


def get_body_nude_prompt(body_wear_output):
    if get_config_value_by_key("nude_strong"):
        body_wear_output = body_wear_output + "(nipples, pussy, "
    else:
        body_wear_output = body_wear_output + "("
    nude_random_times = 1
    body_wear_output = body_wear_output + \
                       "completely nude, " + \
                       get_standard_prompt(nude_clothes, False, True)
    if get_config_value_by_key("is_simple_nude") is not True:
        body_wear_output = body_wear_output \
                           + get_standard_prompt(nude_list[0]) \
                           + get_standard_prompt(pose_touching_clothes)
    nude_random_times = get_config_value_by_key("nude_list_random_index_times")
    if nude_random_times > len(nude_list) - 1:
        nude_random_times = len(nude_list) - 1
    elif nude_random_times <= 0:
        nude_random_times = 0
    if nude_random_times > 0:
        select_list = random_list_no_repeat_number(len(nude_list) - 1, nude_random_times)
        for v in select_list:
            body_wear_output = body_wear_output + get_standard_prompt(nude_list[v])
    body_wear_output = remove_comma_space(body_wear_output)
    body_wear_output = body_wear_output + "), "
    return body_wear_output


def get_top_wear_prompt(type_value):
    top_wear_output = ""
    """
    SHIRTS = 1
    COAT = 2
    SWEATER = 3
    OTHERS = 4
    RANDOM = 5
    """
    index = int(type_value)
    if index == 5:
        index = random.randint(1, 4)
    if index == TopWearType.SHIRTS:
        top_wear_output = get_standard_prompt(top_shirts)
    elif index == TopWearType.COAT:
        top_wear_output = get_standard_prompt(top_coat)
    elif index == TopWearType.SWEATER:
        top_wear_output = get_standard_prompt(top_sweater)
    elif index == TopWearType.OTHERS:
        top_wear_output = get_standard_prompt(top_others)

    return top_wear_output


def get_bottom_wear_prompt(type_value):
    bottom_wear_output = ""
    """
    PANTS = 1
    SKIRT = 2
    SHORT = 3
    RANDOM = 4
    """
    index = int(type_value)
    if index == 4:
        index = random.randint(1, 3)
    if index == BottomWearType.SHORT:
        bottom_wear_output = get_standard_prompt(bottom_shorts)
        bottom_wear_output = bottom_wear_output \
                             + get_legwear_prompt()
    elif index == BottomWearType.SKIRT:
        bottom_wear_output = get_standard_prompt(bottom_skirts)
        bottom_wear_output = bottom_wear_output \
                             + get_legwear_prompt()
    elif index == BottomWearType.PANTS:
        bottom_wear_output = get_standard_prompt(bottom_pants)
    return bottom_wear_output


def get_hair_prompt():
    prompt = ""
    has_hair_length = get_config_value_by_key("add_hair_length")
    if has_hair_length:
        prompt = prompt + get_random_from_list(hairLength)

    enable_hair_color_random = get_config_value_by_key("hair_color")
    target_hair_color = get_assignment_prompt("assign_hair_color")

    if target_hair_color != "":
        if has_hair_length:
            prompt = prompt + " and " + get_config_value_by_key("assign_hair_color") + " hair, "
        else:
            prompt = prompt + get_config_value_by_key("assign_hair_color") + " hair, "
    else:
        if has_hair_length:
            if enable_hair_color_random:
                prompt = prompt + " and " + get_standard_prompt(hairColor)
            else:
                prompt = prompt + " hair, "
        else:
            if enable_hair_color_random:
                prompt = prompt + get_standard_prompt(hairColor)
            else:
                pass

    return prompt


def get_hair_eyes_prompt():
    current_prompt = ""
    current_prompt = get_face_expression() \
                     + get_breasts_size_prompt() \
                     + get_hair_prompt()

    if get_config_value_by_key("add_hair_style"):
        current_prompt = current_prompt \
                         + get_standard_prompt(hair_style)
        if check_chance(0.6):
            current_prompt = current_prompt + get_standard_prompt(hair_others)

    if get_config_value_by_key("enable_eye_color"):
        current_prompt = current_prompt \
                         + get_random_from_list(eyeColor) \
                         + " eyes, "
        if check_chance(0.5):
            current_prompt = current_prompt + get_standard_prompt(eye_others)
    return current_prompt


def get_job_prompt():
    if check_config_value_is_not_none("assign_profession"):
        return get_assignment_prompt("assign_profession")
    else:
        return get_random_from_list(jobs) + ", "


def get_place_prompt():
    if check_config_value_is_not_none("place"):
        return get_assignment_prompt("place")
    else:
        if get_config_value_by_key("sex_mode"):
            return get_standard_prompt(sex_place, False, True)
        else:
            if check_chance(0.5):
                return get_standard_prompt(place)
            else:
                return get_standard_prompt(background_view)


def get_user_additional_prompt():
    target_prompt = ""
    if check_config_value_is_not_none("additional_prompt"):
        target_prompt = target_prompt + get_assignment_prompt("additional_prompt")
    return target_prompt


def get_starting_prompt():
    target_prompt = ""
    if get_config_value_by_key("use_starting"):
        # masterpiece, 
        target_prompt = "best quality, absurdres, "
    return target_prompt


def get_colors_prompt():
    if get_config_value_by_key("add_colors"):
        return get_standard_prompt(color_list)
    return ""


def get_bottom_prompt():
    target_prompt = ""
    if get_config_value_by_key("enable_light_effect"):
        target_prompt = target_prompt + get_standard_prompt(light_effects)
    if get_config_value_by_key("enable_image_tech"):
        target_prompt = target_prompt + get_standard_prompt(image_techniques)

    if get_config_value_by_key("add_hair_accessories"):
        target_prompt = target_prompt + get_standard_prompt(hair_accessories)
    if get_config_value_by_key("add_neck_accessories"):
        target_prompt = target_prompt + get_standard_prompt(neck_accessories)
    if get_config_value_by_key("add_earrings"):
        target_prompt = target_prompt + get_standard_prompt(earrings)
    if get_config_value_by_key("add_detail_suffix"):
        target_prompt = target_prompt + "jewelry, ultra-detailed, 8k, "

    if get_config_value_by_key("enable_day_weather"):
        target_prompt = target_prompt \
                        + get_standard_prompt(day_time) \
                        + get_standard_prompt(weather)

    target_prompt = target_prompt \
                    + get_body_status_prompt() \
                    + get_accessories_mix_prompt() \
                    + get_objects_mix_prompt() \
                    + get_suffix_beautiful_prompt()

    if get_config_value_by_key("has_girl_desc"):
        # finely detailed beautiful eyes and detailed face
        target_prompt = target_prompt + "extremely detailed eyes and face, extremely delicate and beautiful girl, beautiful face, "

    target_prompt = target_prompt + get_colors_prompt()

    return target_prompt


########## Sex Mode ##########
def get_s_girl_desc():
    return "1 " + get_random_from_list(beautifier) + " girl, "


def get_s_man_type_prompt():
    if get_config_value_by_key("man_random") is not True:
        return "1boy, "
    else:
        return get_standard_prompt(sex_man_type)


def get_s_position():
    current_prompt = "("
    current_prompt = current_prompt + get_random_from_list(sex_positions_reload) + "), "
    return current_prompt


def get_s_act_sex_prompt():
    prompt = get_realistic_prompt() \
             + get_s_position() \
             + "(" + get_s_girl_desc() \
             + get_s_man_type_prompt() \
             + "sex), " \
             + "vaginal, penis, blush, pussy, pussy juice, tong, penetration, " \
             + get_s_bottom_prompt()

    return prompt


def get_s_act_group_prompt():
    prompt = get_realistic_prompt() + "("
    r_value = get_random_from_list(sex_act_group)
    prompt = prompt \
             + r_value \
             + ", group sex), " \
             + get_s_position() \
             + "vaginal, penis, blush, pussy, pussy juice, tong, penetration, " \
             + get_s_bottom_prompt()
    return prompt


def get_s_act_tentacles_prompt():
    prompt = get_realistic_prompt() + \
             "(" + get_s_girl_desc() \
             + get_random_from_list(sex_act_tentacles) + ", " \
             + get_s_position() \
             + ")," \
             + "vaginal, blush, pussy, pussy juice, " \
             + get_s_bottom_prompt()

    return prompt


def get_s_bottom_prompt():
    return get_standard_prompt(expression_sexual) \
        + get_breasts_size_prompt() \
        + get_standard_prompt(hair_accessories) \
        + get_standard_prompt(neck_accessories) \
        + get_standard_prompt(earrings) \
        + get_place_prompt() \
        + get_legwear_prompt() \
        + get_panties_prompt() \
        + get_ribbon_others() \
        + get_shoes_prompt() \
        + get_accessories_mix_prompt() \
        + "nude, jewelry, chain, ribbon, best quality, absurdres, ultra-detailed, 8k, " \
        + "\n\n"


def get_assignment_prompt(the_assignment):
    the_value = get_config_value_by_key(the_assignment).lower()
    # check the_value, if is like nil, null, none, then return ""
    if the_value == "nil" or the_value == "null" or the_value == "none" or the_value == "空" or the_value == "":
        return ""
    else:
        return "(" + get_config_value_by_key(the_assignment) + "), "


def get_standard_prompt(target_list, strong=False, chance_toggle=False):
    if strong:
        return "(" \
            + get_random_from_list(target_list) \
            + ":{:.2f}".format(random.uniform(1.1, 1.21)) \
            + "), "
    else:
        if chance_toggle:
            if check_chance(0.5):
                return get_random_from_list(target_list) + ", "
            else:
                return ""
        else:
            return get_random_from_list(target_list) + ", "


def get_random_from_list(list):
    i = random.randint(0, len(list) - 1)
    return list[i]


def check_chance(threshold=0.5):
    probability = random.random()
    # print(probability)

    # If the random number is greater than or the threshold, execute operation A
    if probability < threshold:
        return False
    else:
        return True


def random_list_no_repeat_number(max_int, count):
    result = []
    nums = list(range(1, max_int + 1))
    for _ in range(count):
        idx = random.randint(0, len(nums) - 1)
        result.append(nums.pop(idx))
    return result


def remove_comma_space(string):
    index = string.rfind(", ")
    if index != -1:
        string = string[:index] + string[index + 2:]
    return string


def check_config_value_is_not_none(the_key):
    the_value = project_config[the_key]
    if the_value is not None:
        # check if the value is string, if it is, check if it is not empty
        # check if the value is list, if it is, check if it is not empty
        if isinstance(the_value, str):
            if the_value != "":
                return True
            else:
                return False
        elif isinstance(the_value, list):
            if len(the_value) > 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_config_value_by_key(the_key):
    return project_config[the_key]


class FaceExpression(IntEnum):
    EMOTIONS = 1
    SEXUAL = 2
    SMILE = 3
    SMUG = 4
    RANDOM = 5


class BodyWearType(IntEnum):
    DRESS = 1
    UNIFORM = 2
    BODYSUIT = 3
    TRADITIONAL = 4
    CUSTOM = 5
    RANDOM = 6
    ASNULL = 7


class BottomWearType(IntEnum):
    PANTS = 1
    SKIRT = 2
    SHORT = 3
    RANDOM = 4


class TopWearType(IntEnum):
    SHIRTS = 1
    COAT = 2
    SWEATER = 3
    OTHERS = 4
    RANDOM = 5


class PoseType(IntEnum):
    BASE = 1
    WHOLE = 2


class FootWearType(IntEnum):
    BOOTS = 1
    HIGHHEELS = 2
    SANDALS = 3
    SLIPPERS = 4
    BARE = 5
    ASNULL = 6


class LegWearType(IntEnum):
    SOCKS = 1
    KNEEHIGHS = 2
    OVERKNEEHIGHS = 3
    THIGHHIGHS = 4
    PANTYHOSE = 5
    BARE = 6
    ASNULL = 7
    RANDON = 8


class NSFWType(IntEnum):
    NUDE = 1
    SEXUAL = 2
    NOTNSFW = 3


make_prompt_strong_scale = 1.331

project_config = {
    # Perspective & Location
    "angle": "",  # null is disabled
    "body_framing": "",
    "assign_focus_on": "",  # null is disabled
    "add_focus": False,
    "face_expression": FaceExpression.SMILE,
    "pose_type": PoseType.BASE,
    "place": "",
    "dynamic_mode": False,  # Whether to turn on the dynamic mode, use Agle, Pose, View in dynamic mode
    # Body wearing
    "breasts_size": "",  # null is disabled
    "body_wear": BodyWearType.DRESS,
    "top_wear": TopWearType.SHIRTS,
    "bottom_wear": BottomWearType.SKIRT,
    "leg_wear": LegWearType.ASNULL,
    "panties": False,
    "shoes_type": FootWearType.ASNULL,
    "body_with": True,
    "body_status": True,
    "body_description": False,
    "body_skin": False,
    "cloth_trim": True,

    # Color, just give color
    "leg_wear_color": "",
    "shoes_color": "",
    "hair_color": False,
    "enable_eye_color": True,
    "disable_all_color": True,
    # Specify Prompt directly, this will directly skip other configuration, and automatically deepen the weight of Prompt
    "assign_pose": "",  # null is disabled
    "assign_profession": "",  # null is disabled
    "assign_expression": "",
    "assign_shoes": "",
    "assign_leg_wear": "",
    "assign_body_clothes": "",
    "assign_panties": "",
    "assign_girl_description": "",
    "assign_hair_color": "",  # Specify hair color

    # Decoration, items, adjectives
    "accessories_random_tims": 3,  # max:6 NOTE：For some models, how to appear these prOMPTs may affect the perspective effect
    "object_random_times": 0,  # max: 6
    "suffix_words_random_times": 0,  # Sabbage dotted random number

    # nsfw/sexual/nude
    "nsfw_type": NSFWType.NUDE,
    "sexual_list_random_index_times": 2,  # max:5
    "nude_list_random_index_times": 1,  # max:9
    "is_nsfw": False,
    "is_uncensored": False,
    "is_simple_nude": False,
    "nude_strong": False,  # Whether to strengthen NUDE, add nipple and pussy

    # sex
    "sex_mode": False,
    "sex_type": SexActType.SEX,
    "man_random": False,

    # Character description
    "girl_cnt": 1,  # Number of characters
    "has_girl_desc": False,  # Whether to add ultra -long girl descriptions, it seems that most of them do not need
    "add_girl_beautyful": True,  # Girl prefix description
    "add_hair_length": True,  # Whether to add a long description
    "add_hair_style": False,  # Whether to add hairstyle description
    "add_hair_accessories": False,  # Whether to add hair accessories description
    "add_neck_accessories": False,  # Whether to add neck decoration description
    "add_earrings": False,  # Whether to add earrings description

    # Other configuration
    "is_realistic": True,
    "use_starting": True,  # Do you use a spell to start?
    "add_detail_suffix": False,  # Whether to add detail description
    "add_colors": False,
    "additional_prompt": "",
    "enable_day_weather": False,  # Whether to enable the weather
    "enable_light_effect": True,  # Light effect
    "enable_image_tech": False,  # Image technology

    # lora & embeddings
    "lora": [],  # x
    "lyco": [],  # y
    "lora_weights_random": True,
    "embeddings": [],  # z
    "models_order": ['xyz'],  # lora, lyco, embeddings 输出顺序xyz
}
