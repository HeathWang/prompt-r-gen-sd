# -*- coding:utf-8 -*-

import os
import random
import sys
from enum import IntEnum

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from model_manager import (ModelInfo, LoraConfigManager)


class LoraCategory(IntEnum):
    FACE_FASHION = 101,  # ★★★★ 妆容，红唇，成熟
    FACE_GIRL_FRIEND_MIX = 102,  # 女友脸
    FACE_SHOJOVIBE = 103,  # ★★★★ 少女感 13213@16557
    FACE_NWSJ = 104,  # NWSJ 表现不稳定，有的模型脸效果不错
    FACE_JANG_WON = 105,
    FACE_KOREANDOLL = 106,  # 韩国脸，妥妥的表现优异
    FACE_BAD_GIRL = 107,  # 坏女孩
    FACE_KARINA_MAKINA = 108,  # 韩国某个妹子？
    FACE_CHILLOUTMIXSS = 109,  # 专业为CHILLOUT优化的脸，表现不错
    FACE_ONESAMA_SISTER = 110,  # 大姐姐，animate，3d表现也可以
    FACE_HIPOLY_3D = 112,  # 3d人物，兼容尚可
    FACE_CUTE_GIRL_25D = 113,  # ★★★★★ 公主风格，适配性极佳 93386@99567
    FACE_YURISA_CHAN = 114,
    FACE_CM_MIX = 115,  # ★★★★ 混合了fashion，cuteGirl，guofeng, 适应性不错
    FACE_CUTE_GIRL_MIX_TIKTOK = 116,  # ★★★★ 兼容ok
    FACE_ASIAN_GIRLS_FACE = 117,  # ★★★★ 亚洲女孩脸
    FACE_SHANHAIGUANWU = 118,  # 山海观雾，易水寒
    FACE_MengX_girl_mix = 119,  # ★★★★ MengX girl_Mix 118533@137910

    CHARACTER_ST_LOUIS = 201,  # ★★★★★ 圣路易斯
    CHARACTER_YAE_MIKO = 202,  # yae miko 2d，3d表现都可以
    CHARACTER_GIRLS_FRONTLINE_LIGHTING = 203,  # ★★★★ 少女前线_闪电
    CHARACTER_AILI_REAL = 204,  # ★★★★★ 阿狸
    CHARACTER_JIBRIL = 206,  # Jibril No Game No Life
    CHARACTER_KDA = 207,  # KDA (league of legends)
    CHARACTER_MAI_SHIRANUI = 208,  # 不知火舞
    CHARACTER_MOBILE_LEGENDS_ALICE = 209,  # Mobile Legends Alice 𓆩♡𓆪 2d ok,3d不能看。。
    CHARACTER_SHANHAIGUANWU_COS = 211,  # 山海观雾，易水寒cos  
    CHARACTER_SAEKI_SAYOKO = 212,  # ★★★★ Saeki Sayoko, 2d极佳，3d效果一般，需要hires
    CHARACTER_MEIKO = 213,  # ★★★★ Meiko Prison school，监狱学校，黑丝高跟老师
    CHARACTER_lol_Ahri_Spirit_Blossom = 214,  # 英雄联盟_阿狸_灵魂莲华
    CHARACTER_Akiryo_Mai_3d = 215,  # 【Character】Akiryo's Mai
    CHARACTER_Celestine_Lucullus = 216,  # 精灵  Lucullus from Kuroinu， 2d角色
    CHARACTER_Formidable_Swimsuit = 217,  # ★★★★ Formidable (Azur Lane) Swimsuit 可畏 泳装
    CHARACTER_Taihou_All_Skins = 218,  # Taihou (All Skins) 大凤
    CHARACTER_Howe_Pastry_Princess = 220,  # Howe (Pastry Princess) from Azur Lane | 碧蓝航线 豪
    CHARACTER_yae_miko_real = 221,  # 【原神】八重神子 超逼真

    CLOTHES_LIQUID_CLOTHES = 302,  # 液体裙
    CLOTHES_HAREM_DANCER = 304,  # ★★★★ 舞娘服
    CLOTHES_GREEK = 305,  # 希腊裙
    CLOTHES_ST_LOUIS = 312,  # ★★★★ 圣姨裙
    CLOTHES_STLOUIS_CLOTHES_3D = 336,  # ★★★★ 碧蓝航线-圣路易斯 奢华触感
    CLOTHES_SHEER_SKIRT_BEACH_FASHION = 318,  # ★★★ 海滩裙
    CLOTHES_TUTU_GORGEOUS = 319,  # ★★★★ 图图的华丽丽
    CLOTHES_CM_UNDERWEARSTYLE = 320,  # ★★★★ 3d开高清全身图不错
    CLOTHES_JAPANESE_MAID_DRESS = 322,  # 日本女佣服，白丝很赞
    CLOTHES_GLITTER_BEAD_DRESS = 324,  # ★★★★ Glitter bead dress 粉丝性感裙
    CLOTHES_ELEGANT_MATURE_CLOTHING4 = 338,  # ★★★★ Elegant mature clothing S4 类似碎花裙
    CLOTHES_NIGHTDRESS_3D = 327,  # nightdress S2
    CLOTHES_APHRODITE_ROR = 339,  # sexy cosplay costume / Aphrodite 一种性感衣服
    CLOTHES_NAKED_APRON_3D = 340,  # NakedApron
    CLOTHES_yellow_sexy_dress = 347,  # ★★★★★ coat dress 129969@142529

    # leg wear
    CLOTHES_NUDE_PANTYHOSE = 303,  # 肉色全身
    CLOTHES_SEXY_UNDERWEAR = 313,  # ★★★ 渔网袜
    CLOTHES_BLACK_SEE_THROUGH_BODYSUIT = 314,  # ★★★ 全身丝袜
    CLOTHES_TORN_PANTYHOSE = 326,  # ★★★★ 被撕裂的连裤袜【破损黑丝】torn-pantyhose 下面lyco有个类似的
    CLOTHES_XUEGAO_2D = 331,  # ★★★★ 雪糕 (white legwear & feet)
    CLOTHES_OIL_PANTYHOSE_2D = 332,  # GIRL 水润少女 Oil pantyhose 一般？
    CLOTHES_PANTYHOSE_3D = 334,  # ★★★★★ 赞
    CLOTHES_CRYSTALFRUIT_2D = 335,  # ★★★ Crystalfruit ——WHITE AND BLACK STOCKING
    CLOTHES_OIL_PANTYHOSE = 341,  # OIL PANTYHOSE

    CLOTHES_cmmy_body_siut = 343,  # 苍铭明月的情趣服装系列 - body suit
    CLOTHES_cmmy_black_lace_suspenders = 344,  # 苍铭明月的情趣服装系列 - black lace suspenders
    CLOTHES_cmmy_Lingerie_v2 = 345,  # 苍铭明月的情趣服装系列 -
    CLOTHES_cmmy_purple_sexy = 346,  # 苍铭明月的情趣服装系列 - 紫色有货 119899@142295

    # 制服系列
    CLOTHES_PINK_NURSE_UNIFORM = 325,  # ★★★★ 粉色护士制服 3d
    CLOTHES_SEXY_OFFICE_LADY = 328,  # ★★★★ Sexy Office Lady，有黑丝
    CLOTHES_NURSE_UNIFORM_3D = 329,  # ★★★★ nurse_uniform
    CLOTHES_UPSKIRT_NURSE_3D = 330,  # ★★★★ Upskirt nurse
    CLOTHES_UPSKIRT_OL_3D = 333,  # ★★★★ Upskirt office lady
    CLOTHES_NURSE_NUDE_3D = 337,  # Nurse Clothes - Clothes Pack

    # 中国风衣服
    CLOTHES_CHINA_DRESS = 301,
    CLOTHES_OUTFIT_OF_GLORIOUS = 317,  # ★★★ 敞开性感的
    CLOTHES_DUDOU = 315,  # 肚兜
    CLOTHES_DUNHUANG_APSARAS_DUDOU = 321,  # ★★★★ 敦煌仙子肚兜
    CLOTHES_PETAL_CHEONGSAM = 323,  # 汉旗袍
    CLOTHES_QINGHUA = 342,  # 青花 blue-and-white | Chinese ornament
    CLOTHES_cheongsam_with_high_slit = 348,  # cheongsam with a high slit 128508@140717

    # 裙子系列
    DRESS_DEEP_V_NECK = 306,
    DRESS_ELEGANT_MERMAID = 307,
    DRESS_FLORAL_PROM = 308,
    DRESS_FLOUNCE = 309,
    DRESS_LEG_SPLIT = 310,
    DRESS_PUFF = 311,
    CLOTHES_DA_BEAUTY = 360,  # 真实模特秀

    # jk裙
    CLOTHES_CONCEPTSHORTSKIRT_ANIMTE = 361,  # ConceptShortSkirt(for extra shortness)
    CLOTHES_JK_MICRO_SKIRT_3D = 362,  # ★★★★ JK Micro Skirt
    CLOTHES_SEXY_CATHOLIC_SCHOOL_UNIFORM = 363,  # ★★★★★ 👍🏻我理想中的 Sexy Catholic school uniform
    clothes_Sexy_school_uniform = 364,  # Sexy school uniform 129547@142020

    ACCESSORIES_GGX_HEELS = 401,  # ★★★★★ 👍🏻 尖头高跟
    ACCESSORIES_FLORAL_BOW_CRYSTAL_POINTY_HEELS = 410,  # ★★★★ 仙女尖头高跟鞋,动画model更适用
    # 水晶系列
    ACCESSORIES_GEM_STUDDED = 403,  # ★★★ 水晶
    ACCESSORIES_CRYSTAL_TEXTURE = 412,  # 水晶质感
    ACCESSORIES_CRYSTAL_FASHION = 404,  # ★★★ 水晶

    ACCESSORIES_BODYCHAIN = 402,  # ★★★ 身体锁链
    ACCESSORIES_chest_chain = 405,  # 情趣小饰品 胸链 | chest chain
    ACCESSORIES_SNOWFLAKE_FASHION = 406,
    ACCESSORIES_BUBBLESUDS = 407,  # ★★★★ 洗浴泡泡
    ACCESSORIES_NAKED_BANDAGE = 408,  # ★★★ 绑带
    ACCESSORIES_BUTTERFLY_ON_NIPPLES = 409,  # 蝴蝶遮熊

    ACCESSORIES_WOMB_TATTOO_ANIMATE = 414,  # 纹身 animate
    ACCESSORIES_WOMB_TATTOO_REAL = 415,  # ★★★★★ 👍🏻 纹身

    ACCESSORIES_ELEMENT_ICE = 417,  # ★★★ Elemental Series - Ice - FC

    SEXY_MIRROR_SELFIE = 501,  # 对镜子自拍 
    BODY_MASUSU_BREASTANDNIPPLES = 502,  # 更好看的胸部的
    STYLE_DEVIL_ANGEL = 504,
    STYLE_THICK_RED_BOOK = 507,  # 小红书
    STYLE_PERFECT_REALISTIC_SHINY_ANGEL = 505,  # ★★★★ 璀璨天使 82294@108027
    STYLE_PERFECT_REALISTIC_SNOW_ANGEL = 506,  # ★★★★ 冰雪天使 82294@96576
    STYLE_SEE_THROUGH_ANIMATE = 508,  # 风格较重的see-through
    STYLE_CHINESE_STYLE_HUAXIANGRONG = 509,  # ★★★★ 花想容/Chinese style/古风/
    STYLE_ELEGANT_HANFU_RUQUN_STYLE = 510,  # ★★★ 汉服襦裙风格
    STYLE_MULTIPLE_ASSES = 511,  # ★★★★★ Multiple Asses https://civitai.com/models/21856/multiple-asses 
    BODY_HUGE_ASS_ANIMATE = 512,  #
    STYLE_MILKYCHU_ANIMATE = 513,  # Milkychu
    STYLE_DASH = 514,  # ★★★ Dash\恣意 飘逸的风格
    STYLE_TCTH_FAIRY = 515,  # ★★★ TCTH-Fairy 蝴蝶裙子
    BODY_PERFECT_FULL_ROUND_BREASTS_SLIM_WAIST = 503,  # Perfect Full Round Breasts & Slim Waist 61099@120037
    STYLE_DREAMART = 516,  # DreamART Style
    STYLE_outfit_torn = 517,  # 实现衣服等战损的效果  outfit torn clothes
    STYLE_anxiang_L = 518,  # anxiang | 暗香 (fp16/lite)
    STYLE_Twinkling_Twilight_Taproom = 519,  # Twinkling Twilight Taproom 128228@140369
    STYLE_ChihunHentai = 520,  # ChihunHentai/fascinating body Lora #106586@114480

    BACKGROUND_NEBULA_STYLE = 701,  # 星云幻想
    BACKGROUND_CHINESE_STYLE_FUTURE = 702,  # ★★★★ 中国风与未来科技感的结合
    BACKGROUND_HUNDRED_FLOWERS_BREW = 703,  # 百花酿
    BACKGROUND_GLOWING_STARS = 704,  # 发光星星
    BACKGROUND_BUTTERFLY_FLOWERS = 707,  # 🦋和花
    BACKGROUND_Bokeh_Glowing_Dust = 708,  # Bokeh and Glowing Dust 129763@142279

    ANGLE_STRADDLING_INCOMING_KISS = 801,  # ★★★ pov kiss
    ANGLE_ARM_SUPPORT_AND_FROM_BELOW = 802,  # ★★★ pov压迫感

    FUNC_DETAIL_TWEAKER = 901,  # Detail Tweaker LoRA (细节调整LoRA)
    FUNC_DETAIL_ENHANCER = 902,  # Add More Details - Detail Enhancer / Tweaker (细节调整)
    FUNC_AHEGAO = 903,  # Ahegao
    FUNC_ADD_CUMBERSOME = 904,  # Cumbersome / 繁雑度 Concept (With dropout & noise version)
    FUNC_ZOOM_SLIDER = 905,  # Zoom Slider

    POSE_ASS_UP_WAIT_FEET = 602,
    POSE_POV_DOGGY_ANAL = 604,  # 菊花残
    POSE_ALL_FOURS_AND_FROM_ABOVE = 605,  # 爬向你
    POSE_PANTIES_PULLED_ASIDE_FUCK = 606,  # ★★★★★
    POSE_PRESENT_ASS = 607,
    POSE_SIDEWAY_ASS = 608,
    POSE_POV_DOGGY_STYLE_MS = 609,
    POSE_PRONE_ASS_OUT = 610,
    POSE_BUTTJOB_ANIMATED = 611,  # 兼容ok
    POSE_FUCKED_SILLY_FROM_BEHIND_ANIMATE = 612,  # 3d,2.5d表现不好，适用于animate
    POSE_POV_DOGGYSTYLE_1M = 613,  # 2,3d均适用
    POSE_POV_WAIST_GRAB_ANIMATE = 614,  # ★★★★ 适用于动画
    POSE_REVERSE_COWGIRL_WITH_SOLES_FEET = 615,  # 效果不稳定，3d
    POSE_EROPOSE_ALL_FOURS = 616,  # 动画效果可能更好，容易崩脸
    POSE_AMAZON_POSITION_ANIMATE_297 = 603,
    POSE_POV_SQUATTING_COWGIRL_1M = 620,  # POV Squatting Cowgirl LoRA [1 MB]
    POSE_COWGIRL_POSITION_ANIMATE = 621,  # Cowgirl Position, from back
    POSE_POV_SPITROAST_ANIMATE = 622,  # Pov spitroast
    POSE_STANDING_SEX_ANIMATE = 623,  # Standing Sex/ Doggystyle | LoRA
    POSE_THIGH_SEX = 624,  # Thigh Sex
    POSE_XIAOMA_DACHE_2D = 625,  # 效果一般，很难出好图
    POSE_RIDING_SEX_3D = 627,  # 骑乘
    POSE_GUIDED_BREAST_GRAB = 629,  # 抓奈子 Guided Breast Grab
    POSE_HOLDING_WAIST_POV_COWGIRL = 630,  # Holding Waist POV Cowgirl Position
    pose_cowgirl_with_hands_on_knees = 631,  # cowgirl with hands on knees #128170@140297
    pose_POV_Breast_Grab_Cowgirl = 632,  # POV Breast Grab Cowgirl # 111022@138862
    pose_Against_glass_sex = 633,  # Against glass sex #126935@138852

    POSE_BREASTS_ON_GLASS = 601,  # 挤玻璃
    POSE_PUSSY_ON_GLASS = 617,  # ass 挤玻璃
    POSE_ASS_ON_GLASS_9K = 618,
    POSE_ASS_ON_GLASS_2K = 619,

    POSE_SIT_CROSSLEG = 626,  # Sitcrossleg (legs/shoes concept/helper)
    POSE_HUGGING_OWN_LEGS = 628,  # Hugging own legs


class LyCORIS(IntEnum):
    # ★★★★★ 下面几个兼容性都很好，神级pose
    POSE_SAYA_POV_MISSIONARY_STRANGLING = 101,
    POSE_SAYA_POV_MISSIONARY_HOLDING_HANDS = 102,
    POSE_SAYA_POV_MISSIONARY_BREAST_GRAB = 103,
    POSE_SAYA_POV_MISSIONARY_THIGH_GRAB = 104,
    POSE_SAYA_POV_MISSIONARY_TORSO_GRAB = 105,
    POSE_SAYA_POV_MISSIONARY_HOLDING_WRIST = 106,

    POSE_HEADBOARD_ANGLE_UPSIDE_DOWN = 107,
    POSE_SEX_FROM_BEHIND_SMOOTH_ASS = 108,
    POSE_FRONT_VIEW_DOGGYSTYLE_ARMGRAB = 109,  # arm grab
    POSE_PUBLIC_TRAIN_SEX = 110,
    POSE_POV_GROUP_SEX = 111,  # ★★★★★ POV Group Sex | Sex with multiple girls

    STYLE_AGM_STYLE_LOHA = 201,  # ★★★★★ AGM 还有其他很多风格：https://civitai.com/models/94772/agm-style-loha
    STYLE_ABSTRACT_DREAMWAVE = 202,  # ★★★★ 改变画风，很炸裂★★★★★ 62293@94944

    CHARACTER_SLIME_TRANSFORMARTION = 301,  # 史莱姆girl
    CHARACTER_BELIAL_SEVEN_MORTAL_SINS = 306,  # Belial (Seven Mortal Sins) 七宗罪审判大姐姐
    CHARACTER_HYPNOTIZED_HAREM = 307,  # Hypnotized Harem 

    # leader three作者的一些lyco， 兼容性不是太好
    CHARACTER_LEADERTHREE_SAYIKA = 302,
    CHARACTER_LEADERTHREE_SHIMASHIMA = 303,  # Re:shimashima | Re：しましま
    CHARACTER_LEADERTHREE_KAWATA_HISASHI = 304,  # kawata hisashi | カワタヒサシ | 河田寿人
    CHARACTER_LEADERTHREE_RIKIDDO = 305,  # rikiddo | リキッド | 理奇德

    BACKGROUND_SINSYA = 401,  # 辰砂，中国古代风格
    BACKGROUND_HALATION = 402,  # 彩度優化器 Concept

    CLOTHES_NAKEDTOWEL = 501,  # 浴袍sexy 
    CLOTHES_VYSHIVANKA_PANTIES = 502,  # 一种性感nn
    CLOTHES_EASTEN_APRONS = 503,  # Sexy Attire | Aprons: Easten Aprons 东方风格围裙
    CLOTHES_BRIDAL_LINGERIE = 504,  # Bridal Lingerie 新娘内衣

    STYLE_BEAUTYLEGS = 601,  # ★★★★★ beautylegs 111195@119933
    STYLE_TORN_PANTYHOSE = 602,  # ★★★★★ 撕裂的

    FUNC_EHEGAO_CUTE_2D = 701,  # ehegao Concept 😌


class Embeddings(IntEnum):
    ULZZANG = 1,
    ZHUBAO = 2,
    SUIJING = 3,
    N3T0P = 4,
    BEAUTIFUL_MISTAKE = 5,
    PURE_EROS_FACE = 6,
    FCDETAILPORTRAIT = 7,
    FCHEATPORTRAIT = 8,
    MICROMINI = 9,
    UNDER_BOO = 10,


global_random_f = False


def get_single_lora_prompt(category, weight=None, diff_style=0):
    prompt = ""
    lora = LoraConfigManager()
    model = lora.query_data(f"{category}_1")
    if isinstance(model, ModelInfo):

        if model.trigger_words != "":
            prompt = "{},<lora:{}:{}>,".format(model.trigger_words, model.name_model,
                                               get_random_weight(model.min_widget, model.max_widget, model.default_widget, weight))

        else:
            prompt = "<lora:{}:{}>,".format(model.name_model,
                                            get_random_weight(model.min_widget, model.max_widget, model.default_widget, weight))
    """
    if category <= 0:
        return prompt
    if category == LoraCategory.FACE_FASHION:
        prompt = "fashi-g, makeup, mature female, <lora:fashigirl-v5.5-lora-naivae-64dim:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.POSE_BREASTS_ON_GLASS:
        prompt = "breasts_on_glass ，nipples,breast press, against glass, navel, completely nude, <lora:breasts_on_glass:{}>, ".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_ST_LOUIS:
        prompt = "stlouis, <lora:st louis epoch5:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.FACE_GIRL_FRIEND_MIX:
        prompt = "<lora:GirlfriendMix2:{}>, ".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.FACE_SHOJOVIBE:
        prompt = "<lora:shojovibe_v11:{}>, ".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.FACE_CHILLOUTMIXSS:
        prompt = "photorealistic, <lora:ChilloutMixss:{}>, ".format(get_random_weight(0.4, 0.8, 0.8, weight))
    elif category == LoraCategory.CHARACTER_YAE_MIKO:
        prompt = "<lora:YaeMiko_mix:{}>, ".format(get_random_weight(0.6, 0.8, 0.7, weight))
    elif category == LoraCategory.CLOTHES_CHINA_DRESS:
        
        prompt = "china dress, <lora:ChinaDress:{}>, ".format(get_random_weight(0.4, 0.6, 0.55, weight))
    elif category == LoraCategory.CLOTHES_NUDE_PANTYHOSE:
        prompt = "<lora:Nude_pantyhose:{}>, pantyhose, ".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.FACE_NWSJ:
        prompt = "<lora:PerfectNwsjMajic_4:{}>, PerfectNwsjMajic, ".format(get_random_weight(0.6, 0.8, 0.7, weight))
    elif category == LoraCategory.FACE_HIPOLY_3D:
        prompt = "<lora:hipoly_3dcg_v7-epoch-000012:{}>, 3d, intricate, ".format(
            get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.FACE_JANG_WON:
        prompt = "<lora:jwy___v1:{}>, jwy1, ".format(get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.FACE_KOREANDOLL:
        prompt = "<lora:koreanDollLikeness:{}>, ".format(get_random_weight(0.4, 0.7, 0.66, weight))
    elif category == LoraCategory.CLOTHES_LIQUID_CLOTHES:
        prompt = "<lora:LiquidClothesV1fixed:{}>, liquid clothes, blue_theme, ".format(
            get_random_weight(0.4, 1, 0.6, weight))
    elif category == LoraCategory.FACE_ONESAMA_SISTER:
        prompt = "<lora:Onesama:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.FACE_BAD_GIRL:
        prompt = "<lora:badgirl-v1.5-lora:{}>, bad-girl, mature female, ".format(
            get_random_weight(0.4, 0.6, 0.6, weight))
    elif category == LoraCategory.DRESS_PUFF:
        prompt = "wearing puff_dress, <lora:puff_dress-10:{}>, ".format(get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.DRESS_FLOUNCE:
        prompt = "(wearing flounce_dress:1.3), <lora:flounce_dress:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.DRESS_LEG_SPLIT:
        prompt = "(wearing leg_split_dress:1.2), <lora:leg_split_dress:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.5, weight))
    elif category == LoraCategory.DRESS_FLORAL_PROM:
        prompt = "(floral_prom_dress:1.3), <lora:floral_prom_dress:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.DRESS_ELEGANT_MERMAID:
        prompt = "(wearing mermaid dress:1.3), movie premier gala, <lora:elegant_mermaid_dress:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.DRESS_DEEP_V_NECK:
        prompt = "(wearing deep_v-neck_dress:1.3), <lora:deep_v-neck_dress:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_GGX_HEELS:
        prompt = "a pair of ggx heels, legs focus, sitting, <lora:ggx:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_GEM_STUDDED:
        prompt = "gems, <lora:Gem-Studded:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_GREEK:
        prompt = "greek clothes, peplos, <lora:GreekClothes:{}>, ".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.ACCESSORIES_CRYSTAL_FASHION:
        prompt = "crystal, crystal armor, <lora:Crystal-fC-V1:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.ACCESSORIES_SNOWFLAKE_FASHION:
        prompt = "snowflake, <lora:Snowflakes-V1:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.ACCESSORIES_BUBBLESUDS:
        prompt = "bubblesuds, bubble foam, <lora:bubblesuds:{}>, ".format(get_random_weight(0.4, 0.6, 0.6, weight))
    elif category == LoraCategory.BODY_MASUSU_BREASTANDNIPPLES:
        prompt = "large breast, nipples, <lora:masusu_breast:{}>, ".format(get_random_weight(0.4, 0.6, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_NAKED_BANDAGE:
        prompt = "naked bandage, claw pose, <lora:attire_nakedbandage:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.POSE_ALL_FOURS_AND_FROM_ABOVE:
        prompt = "all fours, <lora:AllFoursFromAboveV1:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.POSE_ASS_UP_WAIT_FEET:
        prompt = "(ass up wait feet, completely nude, pussy, big ass), <lora:ass_up_wait_feet.v2:{}>, ".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.POSE_POV_DOGGY_ANAL:
        prompt = "<lora:PovDoggyAnal-v3:{}>, close up photo of beautiful blonde white glossy skin woman supermodel doggystyle anal by pool, looking back, perfect lighting, masterpiece, perfect detailed face, from above,(ulzzang-6500:0.4), wet,  very long hair, ".format(
            get_random_weight(0.7, 0.85, 0.8, weight))
    elif category == LoraCategory.POSE_PANTIES_PULLED_ASIDE_FUCK:
        prompt = "panties pulled aside fuck, large breasts, long hair, navel, blue eyes, <lora:panties_pulled_aside_fuck.v1.0:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.ACCESSORIES_BODYCHAIN:
        prompt = "nipples, uncensored, photorealistic, <lora:bodychainV2:{}>, ".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_HAREM_DANCER:
        prompt = "harem outfit, dancer, dancing, see-through, <lora:HaremDancer_v1:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.SEXY_MIRROR_SELFIE:
        prompt = "p_m_s, <lora:SexyMirrorSelfie:{}>,".format(get_random_weight(0.55, 0.7, 0.6, weight))
    elif category == LoraCategory.POSE_PRESENT_ASS:
        prompt = "on all fours with butt exposed, looking back at viewer, presentass, <lora:presentass:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.POSE_SIDEWAY_ASS:
        prompt = "lying on her side with her legs to the side, looking back at viewer, sidewayass, <lora:sidewayass:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.POSE_POV_DOGGY_STYLE_MS:
        prompt = "1girl, 1boy, ass, hetero, penis, sex, solo focus,pussy, anus, sex from behind, pov, doggystyle, all fours, back, from behind, <lora:MS_Real_POVDoggyStyle_Lite:{}>, ".format(
            get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.POSE_PRONE_ASS_OUT:
        prompt = "prone, ass out, butt out, ass spread, lying down, on bed, anal gape, legs spread, hands on ass, from behind, from below, <lora:ProneV2:{}>,".format(
            get_random_weight(0.5, 0.65, 0.6, weight))
    elif category == LoraCategory.POSE_BUTTJOB_ANIMATED:
        prompt = "1boy, 1girl, pov hands gabbing another's ass, pov boy grabbing girl's ass, girl bending down, hetero, huge breasts, lace panties, completely nude, huge ass, pov, (pov boy's hands), buttjob, penis, girl on top, <lora:BUTTJOB_V2:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.FACE_KARINA_MAKINA:
        prompt = "<lora:makina69_karina:{}>, ".format(get_random_weight(0.6, 1, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_BUTTERFLY_ON_NIPPLES:
        prompt = "completely nude, butterflypasties, butterfly, navel, narrow waist, <lora:ButterflyPasties:{}>,".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.ACCESSORIES_FLORAL_BOW_CRYSTAL_POINTY_HEELS:
        prompt = "flower, bow, crystal, high heels, <lora:FloralBowCrystalPointyHeels:{}>, ".format(
            get_random_weight(0.5, 0.66, 0.6, weight))
    elif category == LoraCategory.BACKGROUND_NEBULA_STYLE:
        prompt = "<lora:Nebula_LOVE:{}>, ".format(get_random_weight(0.6, 0.7, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_CRYSTAL_TEXTURE:
        prompt = "<lora:crystal_3d:{}>, ".format(get_random_weight(0.7, 0.8, 0.7, weight))
    elif category == LoraCategory.CLOTHES_ST_LOUIS:
        prompt = "LuxuriousWheelsCostume,  silver dress, <lora:LWclothLora:{}>, ".format(
            get_random_weight(0.7, 0.8, 0.8, weight))
    elif category == LoraCategory.CLOTHES_SEXY_UNDERWEAR:
        prompt = "fishnets, lingerie, see-through, bodysuit, pantyhose, bare shoulders, halter neck, <lora:badbrounderwear:{}>, ".format(
            get_random_weight(0.4, 0.6, 0.5, weight))
    elif category == LoraCategory.POSE_FUCKED_SILLY_FROM_BEHIND_ANIMATE:
        prompt = "on bed, indoors, fucked silly, sex from behind, 1boy, completely nude, <lora:fucsil:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.POSE_POV_DOGGYSTYLE_1M:
        prompt = "1boy, penis, doggystyle, from behind, (facing away, completely nude, implied sex), pov hands, ass grab, spread ass, <lora:POVDoggy:{}>, ".format(
            get_random_weight(0.9, 1, 1, weight))
    elif category == LoraCategory.FACE_CUTE_GIRL_25D:
        prompt = "<lora:cutegirl25d:{}>, ".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.POSE_POV_WAIST_GRAB_ANIMATE:
        prompt = "missiongrab, missionary, 1girl, sex, pov, on bed, lying, penis, pussy, pussu juice, large breasts, completely nude, sweatdrop, narrow waist, jewelry, waist chain, chest jewelry, <lora:waistGrab:{}>,".format(
            get_random_weight(0.6, 1, 0.6, weight))
    elif category == LoraCategory.CHARACTER_GIRLS_FRONTLINE_LIGHTING:
        prompt = "redgown, look back,legs apart, squatting, omertosa, cowboy shot, <lora:Girls_Frontline-OTs:{}>, ".format(
            get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.CHARACTER_AILI_REAL:
        if diff_style == 2:
            prompt = "ali, huli erduo, ahri, <lora:ali_50:{}>,".format(get_random_weight(0.6, 1, 0.8, weight))
        else:
            prompt = "(ali, nine tails, Huli erduo, long wavy hair), red and gold bracelets, thighhighs, leg ribbon, <lora:girl_ali:{}>, ".format(get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.CLOTHES_BLACK_SEE_THROUGH_BODYSUIT:
        prompt = "(black see-through bodysuit, large breasts, nipples, highleg panties, high heels), <lora:Black_See-through_Bodysuit:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.FACE_YURISA_CHAN:
        prompt = "yurisa_chan, <lora:yurisa chan:{}>, ".format(get_random_weight(0.5, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_DUDOU:
        prompt = "(red/white/black/blue/green/yellow dudou, black/blue/green/yellow/red/white panties), bare shoulders, huge breasts, see-through, <lora:DuDou:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.65, weight))
    elif category == LoraCategory.ANGLE_STRADDLING_INCOMING_KISS:
        prompt = "(pov, girl on top, straddling, outstretched arms, 1boy), hetero, <lora:POV_KISS:{}>, ".format(
            get_random_weight(0.5, 0.8, 0.6, weight))
    elif category == LoraCategory.ANGLE_ARM_SUPPORT_AND_FROM_BELOW:
        prompt = "(pov, from below), <lora:PovFromBelowV1:{}>, ".format(get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.ACCESSORIES_WOMB_TATTOO_ANIMATE:
        prompt = "(womb tattoo, Pubic tattoo), <lora:womb_tattoo:{}>, ".format(get_random_weight(0.7, 1, 0.8, weight))
    elif category == LoraCategory.ACCESSORIES_WOMB_TATTOO_REAL:
        prompt = "(tattoo on crotch), <lora:womb_tattoo_v5.1.15:{}>, ".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_OUTFIT_OF_GLORIOUS:
        prompt = "(outfit-glorious, no panties), underboob , <lora:OutfitGlorious:{}>, ".format(
            get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.POSE_REVERSE_COWGIRL_WITH_SOLES_FEET:
        prompt = "1boy, penis, anal, pov, nude, soles, from behind, <lora:DDcowfeet:{}>, ".format(
            get_random_weight(0.5, 1, 0.8, weight))
    elif category == LoraCategory.POSE_EROPOSE_ALL_FOURS:
        prompt = "(nude, from behind, all fours, looking at viewer, ass, pussy, barefoot), <lora:eropose_allfours:{}>, ".format(
            get_random_weight(0.5, 1, 0.8, weight))
    elif category == LoraCategory.BACKGROUND_CHINESE_STYLE_FUTURE:
        prompt = "(hanfu, neon lights), <lora:DANWGFWL:{}>, ".format(get_random_weight(0.6, 0.85, 0.8, weight))
    elif category == LoraCategory.STYLE_THICK_RED_BOOK:
        prompt = "thick_red_book_face, <lora:thick_red_book_face_1600:{}>, ".format(
            get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.STYLE_DEVIL_ANGEL:
        prompt = "bj_Devil angel, <lora:bj_Devil_angel:{}>, ".format(get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.CLOTHES_DA_BEAUTY:
        prompt = "<lora:DA_Beauty:{}>, ".format(get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.STYLE_PERFECT_REALISTIC_SHINY_ANGEL:
        prompt = "princess, partially underwater shot, solo, angel, full body, huge wings, model pose, blue rose, blue wings, ice, crystal wings, glowing wings, ice jewelry, <lora:ShinyAngel:{}>, ".format(
            get_random_weight(0.5, 0.75, 0.6, weight))
    elif category == LoraCategory.STYLE_PERFECT_REALISTIC_SNOW_ANGEL:
        prompt = "Snow_Angel, princess, blue eyes, blue gown, blue rose, angel wings, blue jewel, satan, hellfire, full body, demon, flame, lucifer, (ice blue flame), (icicle), crystal wings, glowing wings, <lora:SnowAngel:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.65, weight))
    elif category == LoraCategory.CLOTHES_SHEER_SKIRT_BEACH_FASHION:
        prompt = "sheer skirt, sheer dress, <lora:SheerSkirtV2:{}>, ".format(get_random_weight(0.7, 0.8, 0.8, weight))
    elif category == LoraCategory.BACKGROUND_HUNDRED_FLOWERS_BREW:
        prompt = "baihuaniang, flower, <lora:Hundred_flowers_brew:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.BACKGROUND_GLOWING_STARS:
        prompt = "starlight, star, HDR.UHD.4K,8K,64K,Highly detailed,ultra-finepainting,extreme detail description,Professional, <lora:starlight:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_JIBRIL:
        prompt = "ngnl_jibril, long hair, pink hair, halo,large breasts, symbol-shaped pupils, tatoo, low wings, sideboob, midriff, asymmetrical legwear, mismatched legwear, <lora:ngnl_jibril:{}>, ".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_TUTU_GORGEOUS:
        prompt = "hll, pantyhose, blush, tassel, <lora:hll_v1:{}>, ".format(get_random_weight(0.4, 0.6, 0.4, weight))
    elif category == LoraCategory.CHARACTER_KDA:
        prompt = "kda, <lora:kda_v3:{}>, ".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_ELEMENT_ICE:
        prompt = "ice, <lora:Ice-Fashion-V1:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.BACKGROUND_BUTTERFLY_FLOWERS:
        prompt = "butterfly style, flowers, butterflies, garden, <lora:butterfly:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.CHARACTER_MAI_SHIRANUI:
        prompt = "<lora:ALLmai_shiranui:{}>, ".format(get_random_weight(0.4, 0.75, 0.6, weight))
    elif category == LoraCategory.POSE_PUSSY_ON_GLASS:
        # https://civitai.com/models/50161?modelVersionId=54694
        prompt = "crotch on glass, from below, facing away, (no panties, pussy,  big ass), <lora:pussy_on_glass:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.POSE_ASS_ON_GLASS_9K:
        prompt = "ass on glass, big ass, no panties, pussy, lower body focus, from below, close up, wet, <lora:Ass_On_Glass_9k:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.75, weight))
    elif category == LoraCategory.POSE_ASS_ON_GLASS_2K:
        prompt = "ass on glass, ass focus, from behind, completely nude, against glass, huge ass, pussy, anus, bathroom, wet, <lora:ass_on_glass_2k:{}>, ".format(
            get_random_weight(0.7, 1, 1, weight))
    elif category == LoraCategory.STYLE_SEE_THROUGH_ANIMATE:
        prompt = "see-through, prominent nipple, <lora:see_through:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_CM_UNDERWEARSTYLE:
        prompt = "UnderwearStyle02A, <lora:UnderwearStyle:{}>, ".format(get_random_weight(0.7, 1, 0.7, weight))
    elif category == LoraCategory.FACE_CM_MIX:
        prompt = "<lora:CM-mix:{}>, ".format(get_random_weight(0.4, 1, 0.6, weight))
    elif category == LoraCategory.CLOTHES_DUNHUANG_APSARAS_DUDOU:
        prompt = "(dress,underwear, see-through, chinese clothes, panties), <lora:Dunhuang_apsaras_dudou:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.FACE_CUTE_GIRL_MIX_TIKTOK:
        prompt = "mix4, <lora:cute_girl_mix4:{}>, ".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_JAPANESE_MAID_DRESS:
        prompt = "dress, white thighhighs, twin braids, <lora:Japanese_maid_dress:{}>, ".format(
            (get_random_weight(0.6, 0.8, 0.7, weight)))
    elif category == LoraCategory.CLOTHES_PETAL_CHEONGSAM:
        prompt = "china dress, chinese clothes, dress, <lora:Petal_cheongsam:{}>, ".format(
            (get_random_weight(0.6, 0.8, 0.7, weight)))
    elif category == LoraCategory.FACE_ASIAN_GIRLS_FACE:
        prompt = "FACE, <lora:asianGirlsFace:{}>, ".format(get_random_weight(0.3, 0.6, 0.6, weight))
    elif category == LoraCategory.CHARACTER_MOBILE_LEGENDS_ALICE:
        prompt = "(Mobile_Legends_Alice, blunt_bangs, thigh_highs, pink_eyes), <lora:Mobile_Legends_Alice:{}>, ".format(
            get_random_weight(0.6, 1, 0.95, weight))
    elif category == LoraCategory.STYLE_CHINESE_STYLE_HUAXIANGRONG:
        prompt = "Chinese style, <lora:Chinese_style:{}>,".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.CHARACTER_SHANHAIGUANWU_COS:
        prompt = "long hair, crown, forehead jewel, dress, arms behind back, looking at viewer, necklace, 1girl, jewelry, <lora:yishuihan_shanhai_cos:{}>, ".format(
            get_random_weight(0.6, 0.85, 0.8, weight))
    elif category == LoraCategory.FACE_SHANHAIGUANWU:
        prompt = "<lora:yishuihan_shanhai_face:{}>, ".format(get_random_weight(0.6, 0.85, 0.8, weight))
    elif category == LoraCategory.CHARACTER_SAEKI_SAYOKO:
        prompt = "SaekiSayoko, mature female, milf, full body shot, side view, sitting on chair, makeup, blue suit, blue pencil skirt, thighhighs, high heels, curvy, cleavage, ass, thighs, <lora:SaekiSayoko:{}>, ".format(
            get_random_weight(0.8, 0.95, 0.9, weight))
    elif category == LoraCategory.STYLE_ELEGANT_HANFU_RUQUN_STYLE:
        prompt = "ru_qun, hanfu, silk, tassel, ribbon, <lora:Elegant_hanfu_ruqun_style:{}>,".format(
            get_random_weight(0.7, 1, 0.8, weight))
    elif category == LoraCategory.FUNC_DETAIL_TWEAKER:
        prompt = "<lora:add_detail:{}>, ".format(get_random_weight(0.4, 2, 1, weight))
    elif category == LoraCategory.FUNC_DETAIL_ENHANCER:
        prompt = "<lora:more_details:{}>, ".format(get_random_weight(0.4, 1, 0.5, weight))
    elif category == LoraCategory.CLOTHES_CONCEPTSHORTSKIRT_ANIMTE:
        prompt = "skirt, miniskirt, microskirt, <lora:Micro-skirt:{}>, ".format(
            get_random_weight(0.5, 1.0, 0.8, weight))
    elif category == LoraCategory.CLOTHES_JK_MICRO_SKIRT_3D:
        # pleated_skirt, plaid_skirt, pencil_skirt
        prompt = "jkmicroskirt, microskirt, gigantic ass, ass focus, <lora:jkMicroSkirtV:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.CLOTHES_GLITTER_BEAD_DRESS:
        prompt = "huge breasts,pink dress, <lora:Glitter_bead_dress:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.75, weight))
    elif category == LoraCategory.STYLE_MULTIPLE_ASSES:
        prompt = "multiple girls, 2girls, all fours with butt expressions, pussy, smile, looking back, <lora:MultipleAsses:{}>, ".format(
            get_random_weight(0.9, 1, 1, weight))
    elif category == LoraCategory.BODY_HUGE_ASS_ANIMATE:
        prompt = "ass, ass focus, from behind, shiny skin, huge ass, <lora:HugeASS:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.POSE_AMAZON_POSITION_ANIMATE_297:
        prompt = "huge breasts, long hair, navel, nipples, nude, pov, pussy, pussy juice, smile, sweat, uncensored, narrow waist, <lora:amzn-000019:{}>, long hair, 1girl, thighhighs, jewelry, ".format(
            get_random_weight(0.9, 1, 1, weight))
    elif category == LoraCategory.STYLE_MILKYCHU_ANIMATE:
        prompt = "tongue out, tongue, <lora:milkychu_artstyle:{}>, ".format(get_random_weight(0.7, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_MEIKO:
        prompt = "meiko, skirt, cleavage, school uniform, choker, black thighhighs, huge breasts, <lora:meikoV3:{}>, ".format(
            get_random_weight(0.6, 0.7, 0.6, weight))
    elif category == LoraCategory.CLOTHES_PINK_NURSE_UNIFORM:
        prompt = "PW_nurse, (white thighhighs), <lora:PW_nurse_v1.1:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.65, weight))
    elif category == LoraCategory.POSE_POV_SQUATTING_COWGIRL_1M:
        prompt = "1boy,squatting cowgirl position, vaginal, pov, <lora:PSCowgirl:{}>, ".format(
            get_random_weight(0.9, 1.0, 1, weight))
    elif category == LoraCategory.POSE_COWGIRL_POSITION_ANIMATE:
        prompt = "cowgirlpose, 1boy, penis, cowgirl position, ass, ass focus, facing away, anal, pussy juice, cum on ass, <lora:EkuneCowgirl:{}>, ".format(
            get_random_weight(0.8, 1, 0.9, weight))
    elif category == LoraCategory.CHARACTER_lol_Ahri_Spirit_Blossom:
        prompt = "bell, bare shoulders, fox ears, hair beel, kimono, tail, fox tail, facial hair, (whisker marking:1.1), legwear, bowtie, <lora:LOL_Ahri_Spirit_Blossom:{}>, ".format(
            get_random_weight(0.7, 0.95, 0.8, weight))
    elif category == LoraCategory.POSE_POV_SPITROAST_ANIMATE:
        prompt = "pov, spitroast, top-down bottom-up, sex, 2boys, <lora:pov_spitroast:{}>, bedroom, ".format(
            get_random_weight(0.9, 1, 1, weight))
    elif category == LoraCategory.POSE_STANDING_SEX_ANIMATE:
        prompt = "sex from behind, <lora:DOGGY3rd-000007:{}>, ".format(get_random_weight(0.6, 0.9, 0.9, weight))
    elif category == LoraCategory.STYLE_DASH:
        prompt = "wave, crossed legs, looking at viewer, cloudy sky,long hair, starry sky, high heels, <lora:YingY-000016:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_Akiryo_Mai_3d:
        # https://civitai.com/models/16667/characterakiryos-mai
        prompt = "shiranui mai, akiryo-mai, high ponytail, lips, thighhighs, thighs, shiny skin, <lora:akiryomai-v2-naivae-final-6ep:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_TORN_PANTYHOSE:
        prompt = "torn pantyhose, <lora:torn_pantyhose:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_NIGHTDRESS_3D:
        prompt = "white skirt, white bra, underwear, <lora:nightdress v2_20230708132300:{}>,".format(
            get_random_weight(0.6, 0.75, 0.6, weight))
    elif category == LoraCategory.CHARACTER_Celestine_Lucullus:
        prompt = "celestine lucullus, blonde hair, head wreath, laurel crown, green eyes, o-ring, elf, pointy ears, <lora:celestine-lora-v1.5-naivae-4ep-32dim:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.FUNC_AHEGAO:
        prompt = "ahegao, blush, rolling eyes, tongue out,  saliva, <lora:Ahegaoo:{}>, ".format(
            get_random_weight(0.4, 1, 0.8, weight))
    elif category == LoraCategory.STYLE_TCTH_FAIRY:
        prompt = "fairy, butterfly_wings, gem,  blue_dress, <lora:TCTH_Fairy:{}>, ".format(
            get_random_weight(0.6, 0.7, 0.6, weight))
    elif category == LoraCategory.CLOTHES_SEXY_OFFICE_LADY:
        prompt = "white shirt, cleavage, black pantyhose, underwear, open clothes, glasses, no bra, <lora:Sexy_Office_Lady:{}>, indoors, ".format(
            get_random_weight(0.2, 0.7, 0.4, weight))
    elif category == LoraCategory.CLOTHES_NURSE_UNIFORM_3D:
        prompt = "nurse_uniform, nurse, white thighhighs, <lora:nurse_v11:{}>, ".format(
            get_random_weight(0.4, 0.7, 0.6, weight))
    elif category == LoraCategory.CLOTHES_UPSKIRT_NURSE_3D:
        prompt = "upskirt nurse, topless, <lora:upskirt_nurse:{}>, ".format(get_random_weight(0.6, 0.9, 0.75, weight))
    elif category == LoraCategory.CLOTHES_XUEGAO_2D:
        prompt = "(white pantyhose), thighs, <lora:white_legwear_2d:{}>, ".format(
            get_random_weight(0.8, 1, 0.9, weight))
    elif category == LoraCategory.CLOTHES_OIL_PANTYHOSE_2D:
        prompt = "oil skin, sweating, blush, pantyhose, wet, <lora:Oilgor_2d:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.POSE_THIGH_SEX:
        prompt = "1girl, 1boy, hetero, penis, thigh sex, grinding,thighs, pussy, thick thighs, grabbing from behind, ass, cum, <lora:ThighSexMS:{}>, nsfw, ".format(
            get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_UPSKIRT_OL_3D:
        prompt = "upskirt office lady, (white shirt),short dress, <lora:upskirt_office_lady:{}>, ".format(
            get_random_weight(0.75, 0.9, 0.8, weight))
    elif category == LoraCategory.POSE_XIAOMA_DACHE_2D:
        prompt = "onesyotahug, <lora:concept_xiaoma_dache:{}>, syota,1boy,large breasts,  hug,vaginal,sex, nude,nsfw,1girl,  grabbing breast, breast sucking,leg lock,mating press, on bed, ".format(
            get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.CLOTHES_PANTYHOSE_3D:
        prompt = "PANTYHOSE,ASS,CROTCHLESS, <lora:PANTYHOSE_3d_secret:{}>, ".format(
            get_random_weight(0.6, 0.7, 0.6, weight))
    elif category == LoraCategory.CLOTHES_CRYSTALFRUIT_2D:
        prompt = "(white pantyhose,white legwear), white shirt,  <lora:CrystalfruitV2-000012:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_ELEGANT_MATURE_CLOTHING4:
        prompt = "print dress, pink flower,pink theme, <lora:Elegant_mature_clothing4:{}>, ancient Chinese town,ancient Chinese building, chinese garden, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.FUNC_ADD_CUMBERSOME:
        prompt = "<lora:With_dropout_noise_version:{}>,".format(get_random_weight(0.6, 1, 1, weight))
    elif category == LoraCategory.POSE_SIT_CROSSLEG:
        if diff_style == 0:
            prompt = "sitcrossleg, sitting, crosslegged, <lora:sitcrossleg:{}>, ".format(
                get_random_weight(0.8, 1, 1, weight))
        elif diff_style == 1:
            prompt = "sitcrossleg, sitting, crosslegged, thighs, <lora:sitcrossleg:{}>, ".format(
                get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.BODY_PERFECT_FULL_ROUND_BREASTS_SLIM_WAIST:
        prompt = "breasts, <lora:PerfectFullBreasts:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CLOTHES_STLOUIS_CLOTHES_3D:
        prompt = "St.Louis_LuxuryHandle,high heels, full body, silver dress, blue hair, side ponytail, thighs, jewelry, bare shoulders, necklace, huge breasts, revealing clothes,  <lora:StLouis_clothes_3d:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_NURSE_NUDE_3D:
        prompt = "nurse, huge breasts, thick thighs, hospital, puffy nipples, shiny skin, pov, bed, stethoscope,nurse cap, <lora:Nurse-08:{}>, ".format(
            get_random_weight(0.6, 0.85, 0.8, weight))
    elif category == LoraCategory.POSE_RIDING_SEX_3D:
        if diff_style == 0:
            prompt = "ridingsexscene, closed eyes, nude, open mouth, arms up, on bed, <lora:ridingsexscene_lora_01-i4:{}>,".format(
                get_random_weight(0.6, 0.9, 0.65, weight))
        elif diff_style == 1:
            prompt = "ridingsexscene,closed eyes, nude, open mouth, arms up,sex, pov,penis, pussy juice, on bed, <lora:ridingsexscene_lora_01-i4:{}>,".format(
                get_random_weight(0.6, 0.9, 0.65, weight))
    elif category == LoraCategory.POSE_HUGGING_OWN_LEGS:
        prompt = "hugging own legs, thighs, <lora:hugging_own_legs:{}>, ".format(get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.POSE_GUIDED_BREAST_GRAB:
        if diff_style == 1:
            prompt = "1girl, 1boy, huge breast, fit and petite body, nude, grabbing, guided breast grab, guiding hand, in the bedroom,pov hands, <lora:POVBREASTGRAB_V2:{}>, ".format(
                get_random_weight(0.4, 0.9, 0.6, weight))
        else:
            prompt = "guided breast grab, guiding hand, pov hands, 1boy,1girl, hetero, navel, <lora:POVBREASTGRAB_V2:{}>, ".format(
                get_random_weight(0.4, 0.9, 0.6, weight))
    elif category == LoraCategory.CLOTHES_SEXY_CATHOLIC_SCHOOL_UNIFORM:
        prompt = "catholic school uniform, thighs, <lora:CatholicSchoolUniformDogu:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.CLOTHES_APHRODITE_ROR:
        prompt = "a woman, white dress, sleeveless, blonde hair, hair ornament,very long hair, underwear, arm bracelet, ring, hair flower, flower, sensual pose, perfect female body, (beautiful eyes:1), <lora:AphroditeROR:{}>, ".format(
            get_random_weight(0.8, 1, 0.9, weight))
    elif category == LoraCategory.POSE_HOLDING_WAIST_POV_COWGIRL:
        prompt = "1girl, 1boy, POVHipGrabCowgirl, hetero, vaginal, open mouth, blushing, on bed, bedroom, completely nude, <lora:CONCEPT_HipGrabCowgirl:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_Formidable_Swimsuit:
        prompt = "formidableswim,blue_bikini, <lora:FormidableSwimsuit:{}>, (white_single_thighhigh), pool, wet, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.CHARACTER_Taihou_All_Skins:
        if diff_style == 1:
            prompt = "taihouwedding, wedding dress, <lora:taihou-epoch5:{}>, ".format(
                get_random_weight(0.6, 1, 0.8, weight))
        elif diff_style == 2:
            prompt = "taihouphoenix, china dress, fishnets, <lora:taihou-epoch5:{}>, ".format(
                get_random_weight(0.6, 1, 0.8, weight))
        elif diff_style == 3:
            prompt = "taihousweet, school uniform, <lora:taihou-epoch5:{}>, ".format(
                get_random_weight(0.6, 1, 0.8, weight))
        elif diff_style == 4:
            prompt = "taihouforbid, red dress, thighhighs, red high heels, <lora:taihou-epoch5:{}>, ".format(
                get_random_weight(0.6, 1, 0.8, weight))
        elif diff_style == 5:
            prompt = "taihoudefault, mask, kimono, thighhighs, solo, <lora:taihou-epoch5:{}>, ".format(
                get_random_weight(0.6, 1, 0.8, weight))
        else:
            prompt = "taihou, <lora:taihou-epoch5:{}>, ".format(get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.CLOTHES_NAKED_APRON_3D:
        prompt = "2girls, apron,naked apron,heart print,ass,<lora:NakedApron:{}>, ".format(
            get_random_weight(0.35, 0.6, 0.4, weight))
    elif category == LoraCategory.CLOTHES_OIL_PANTYHOSE:
        prompt = "pantyhose, <lora:REALOilpantyhose:{}>, ".format(get_random_weight(0.6, 0.7, 0.7, weight))
    elif category == LoraCategory.CHARACTER_Howe_Pastry_Princess:
        prompt = "1girl red eyeshadow blue eyes makeup, hair ribbon maid headdress white apron detached collar bow frills detached sleeves black gloves black thighhighs lace-trimmed legwear garter straps red dress, <lora:howe_pastry_princess:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.CLOTHES_QINGHUA:
        prompt = "qinghua, cheongsam, blue floral background, <lora:qinghua50:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.STYLE_DREAMART:
        prompt = "<lora:DreamArt:{}>,".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.FUNC_ZOOM_SLIDER:
        prompt = "<lora:zoom_slider:{}>, ".format(get_random_weight(1, 1, 1, weight))
    elif category == LoraCategory.FACE_MengX_girl_mix:
        prompt = "<lora:MengX girl_Mix:{}>, ".format(get_random_weight(0.6, 1, 0.8, weight))
    elif category == LoraCategory.STYLE_outfit_torn:
        prompt = "torn clothes, torn, <lora:outfit_tornclothes:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LoraCategory.STYLE_anxiang_L:
        prompt = "<lora:anxiang_L:{}>,".format(get_random_weight(0.6, 0.8, 0.7, weight))
    elif category == LoraCategory.CLOTHES_cmmy_body_siut:
        prompt = "bodystocking, <lora:liantisiwa:{}>,".format(get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LoraCategory.CLOTHES_cmmy_black_lace_suspenders:
        prompt = "garter belt, <lora:diaodaiwav:{}>,".format(get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_cmmy_Lingerie_v2:
        prompt = "<lora:cmmy_Lingerie:{}>,".format(get_random_weight(0.6, 0.8, 0.6, weight))
    elif category == LoraCategory.ACCESSORIES_chest_chain:
        prompt = "Thoracic chain,<lora:Thoracic_chain:{}>,".format(get_random_weight(0.5, 0.8, 0.6, weight))
    elif category == LoraCategory.clothes_Sexy_school_uniform:
        prompt = "navel,white thighhighs,white shirt, <lora:Sexy school uniform:{}>,".format(get_random_weight(0.7, 1, 0.8, weight))
    elif category == LoraCategory.BACKGROUND_Bokeh_Glowing_Dust:
        prompt = "bokeh, glowingdust, <lora:glowingdust:{}>,".format(get_random_weight(0.6, 0.9, 0.6, weight))
    elif category == LoraCategory.STYLE_Twinkling_Twilight_Taproom:
        prompt = "bar, wine, nightclub, <lora:bar1:{}>,".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.CLOTHES_cmmy_purple_sexy:
        prompt = "<lora:purple_sexy:{}>,".format(get_random_weight(0.6, 0.8, 0.65, weight))
    elif category == LoraCategory.CLOTHES_yellow_sexy_dress:
        prompt = "<lora:coatdress:{}>,".format(get_random_weight(0.8, 1, 0.9, weight))
    elif category == LoraCategory.CLOTHES_cheongsam_with_high_slit:
        prompt = "chinese clothes, china dress, White dress,thighs, white underwear, <lora:Chinese_cheongsam_high_slit:{}>,".format(get_random_weight(0.7, 0.9, 0.8, weight))
    elif category == LoraCategory.CHARACTER_yae_miko_real:
        prompt = "yae miko, long hair, pink hair, bangs, hair between eyes, purple eyes, <lora:bachong_shenzi:{}>,".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LoraCategory.pose_cowgirl_with_hands_on_knees:
        prompt = "nsfw,pov,astride,thrusting,pussy juice, <lora:cowgirl_with_hands_on_knees_v1.0:{}>,".format(get_random_weight(0.8, 1, 0.8, weight))
    elif category == LoraCategory.pose_POV_Breast_Grab_Cowgirl:
        prompt = "breast grab, cowgirl position, girl on top, straddling, grabbing, sex, vaginal,nude,1boy,pov, pussy juice,blush,penis, <lora:BREAST_GRAB_V2:{}>,".format(get_random_weight(0.8, 1, 0.85, weight))
    elif category == LoraCategory.pose_Against_glass_sex:
        prompt = "1girl, 3boy, against glass, huge breasts, sex from behind, overflow, breasts on glass, hand up, doggystyle, grabbing from behind,school uniform, thigh sex,penis, cum,panties, train interior,kiss,<lora:pose_glass_sex:{}>,".format(get_random_weight(0.9, 1, 1, weight))
    elif category == LoraCategory.STYLE_ChihunHentai:
        prompt = "ChihunHentai, PIXIV, <lora:ChihunHentai:{}>,".format(get_random_weight(0.6, 1, 0.65, weight))
    """
    return prompt


def get_single_lycoris_prompt(category, weight=None, diff_style=0):
    prompt = ""
    model = LoraConfigManager().query_data(f"{category}_2")
    if isinstance(model, ModelInfo):

        if model.trigger_words != "":
            prompt = "{},<lyco:{}:{}>,".format(model.trigger_words, model.name_model,
                                               get_random_weight(model.min_widget, model.max_widget,
                                                                 model.default_widget, weight))

        else:
            prompt = "<lyco:{}:{}>,".format(model.name_model,
                                            get_random_weight(model.min_widget, model.max_widget, model.default_widget,
                                                              weight))
    """
    if category == LyCORIS.POSE_SAYA_POV_MISSIONARY_STRANGLING:
        prompt = "(vaginal,strangling, lying, pussy juice), <lyco:Saya-pov_missionary_strangling:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SAYA_POV_MISSIONARY_HOLDING_HANDS:
        prompt = "(vaginal,holding hands, interlocked fingers, lying, pussy juice), <lyco:Saya-pov_missionary_holdinghands:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SAYA_POV_MISSIONARY_BREAST_GRAB:
        prompt = "(vaginal, breast grab,arms up, lying, pussy juice), <lyco:Saya-pov_missionary_breastgrab:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SAYA_POV_MISSIONARY_THIGH_GRAB:
        prompt = "(vaginal,thigh grab, lying, pussy juice), <lyco:Saya-pov_missionary_thighgrab:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SAYA_POV_MISSIONARY_TORSO_GRAB:
        prompt = "(vaginal,torso grab, lying, pussy juice), <lyco:Saya-pov_missionary_torsograb:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SAYA_POV_MISSIONARY_HOLDING_WRIST:
        prompt = "(vaginal, lying, pussy juice), <lyco:Saya-pov_missionary_holdinganotherwrist:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.STYLE_AGM_STYLE_LOHA:
        prompt = "redgown,look back,legs apart,squatting, holding coffee cup,Omertosa,cowboy shot,  <lora:OTS14N:0.8>   <lyco:AGM5:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.CHARACTER_SLIME_TRANSFORMARTION:
        prompt = "SlimeC, slime girl, monster girl, colored skin, colored sclera, transparent, heart-shaped pupil, <lyco:SlimeC:{}>, ".format(
            get_random_weight(0.6, 1, 0.8, weight))
    elif category == LyCORIS.BACKGROUND_SINSYA:
        prompt = "sinsya, tassel, red flower, <lyco:Sinsya_Concept:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.STYLE_ABSTRACT_DREAMWAVE:
        prompt = "Dreamwave, <lyco:Dreamwave:{}>, ".format(get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.BACKGROUND_HALATION:
        prompt = "<lyco:Background halation:{}>, ".format(get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LyCORIS.CHARACTER_LEADERTHREE_SAYIKA:
        prompt = "sayika style, (cowgirl position:1.3), girl on top, straddling, upright straddle, happy sex, cum in pussy, pussy piercing, excessive pussy juice, pussy juice, pussy juice stain, pussy juice trail, pussy juice puddle, torn, see-through, female ejaculation, demon wings, demon horns, demon tail, tail wagging, tail ornament,  bridal veil,  evil, seductive, bridal legwear, wedding, marriage, lace trim, thighhighs,   (pink pubic tattoo:1.2), (heart tattoo), <lyco:lt_sayika3:{}>,".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_HEADBOARD_ANGLE_UPSIDE_DOWN:
        prompt = "detailed body,detailed arms,detailed face, (headboardangle, missionary, on back, legs up, 1girl, 1boy, nude,), <lyco:headboardangle:{}>, ".format(
            get_random_weight(0.65, 0.75, 0.75, weight))
    elif category == LyCORIS.CHARACTER_LEADERTHREE_SHIMASHIMA:
        prompt = "reflection, refraction, reshimashima, perfect female body, full body, beautiful detailed glow, (beautiful detailed eyes), solo, (succubus:1.3, silver hair:1.2, looking at viewer), <lyco:lt_Reshimashima:{}>,".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.CHARACTER_LEADERTHREE_KAWATA_HISASHI:
        prompt = "kawata hisashi style, mefmera \(character\), (mefmera hair:1.2), (mefmera ears:1.2), (mefmera eyes:1.3), hair ribbon, butterfly hair ornament, looking at viewer, evil, seductive, seductive smile, (cowgirl position:1.3), girl on top, (straddling), motion lines, (large areolae:1.3), huge nipples, puffy nipples, cum on breasts, bukkake, uterus, pink pubic tattoo, pink womb tattoo, pussy juice, ass visible through thighs, (happy sex), cum in pussy, topless, lace trim, cross-laced footwear, lace-trimmed legwear, lace-trimmed bra, <lyco:lt_kawata_hisashi:{}>, ".format(
            get_random_weight(0.7, 0.85, 0.8, weight))
    elif category == LyCORIS.CHARACTER_LEADERTHREE_RIKIDDO:
        prompt = "rikiddo, perfect female body, full body, beautiful detailed glow, solo, mature, huge breasts, (girl on top, cowgirl position), straddling, blush, (evil, evil girl, seductive, aggressive girl), lactation, (silver hair), (looking at viewer), (symbol-shaped pupils), semen, cum, cum in pussy, motion lines, (succubus), demon horn, cum on body, <lyco:lt_rikiddo:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_SEX_FROM_BEHIND_SMOOTH_ASS:
        prompt = "pov, makelove from behind, straddling, ass focus, sex, 1boy, penis, ass, shiny skin, from behind, <lyco:ASSv12:{}>, ".format(
            get_random_weight(0.45, 0.6, 0.45, weight))
    elif category == LyCORIS.POSE_FRONT_VIEW_DOGGYSTYLE_ARMGRAB:
        prompt = "front view doggystyle, facing viewer, arm grab, standing doggystyle, men behind girl's back, 1boy, hetero, <lyco:front_view_doggystyle_armgrab:{}>, ".format(
            get_random_weight(0.85, 1, 1, weight))
    elif category == LyCORIS.CLOTHES_NAKEDTOWEL:
        prompt = "nakedtowel, towel, ass focus, ass, huge ass, <lyco:NakedTowel:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.65, weight))
    elif category == LyCORIS.CLOTHES_VYSHIVANKA_PANTIES:
        prompt = "edgVyshivanka,edgPanties, <lyco:edgVyshivankaPanties:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LyCORIS.STYLE_BEAUTYLEGS:
        prompt = "beautylegs, high heels, skirt, transparent blouse, standing, full body, <lyco:beautylegs_v01:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LyCORIS.CHARACTER_BELIAL_SEVEN_MORTAL_SINS:
        # https://civitai.com/models/74577/belial-seven-mortal-sins
        prompt = "belialglory, ponytail, heterochromia, <lyco:BelialV2:{}>, ".format(
            get_random_weight(0.6, 0.8, 0.8, weight))
    elif category == LyCORIS.CLOTHES_EASTEN_APRONS:
        prompt = "dudou, LnF, edgApron, embroidery, ([edgApron|dudou|LnF]::0.5), <lyco:edgApron:{}>, ".format(
            get_random_weight(0.8, 1, 1, weight))
    elif category == LyCORIS.POSE_PUBLIC_TRAIN_SEX:
        prompt = "TranT, train, standing, bent over, skirt, shirt, pantyhose, netorare, chikan, molestation, public indecency, horny, ahegao, open mouth, blush, hetero, pussy juice, fingering, multiple boys, faceless male, <lyco:Train:{}>, ".format(
            get_random_weight(0.6, 1, 1, weight))
    elif category == LyCORIS.CHARACTER_HYPNOTIZED_HAREM:
        # https://civitai.com/models/80314/change-a-character-hypnotized-harem-your-waifu-has-been-forced-to-join-a-harem
        prompt = "HypHarem, (highleg panties, see-through, miniskirt), waist chain,narrow waist, navel,chest jewel, symbol-shaped pupils, heart-shaped pupils, expressionless, :o, mind control, <lyco:HypnoHarem:{}>, ".format(
            get_random_weight(0.5, 0.7, 0.7, weight))
    elif category == LyCORIS.STYLE_TORN_PANTYHOSE:
        prompt = "PANTYHOSE,TORN PANTYHOSE, cowboy shot, <lyco:TORN_PANTYHOSE:{}>, ".format(
            get_random_weight(0.4, 0.8, 0.6, weight))
    elif category == LyCORIS.POSE_POV_GROUP_SEX:
        # https://civitai.com/models/114843/pov-group-sex-or-sex-with-multiple-girls

        if diff_style == 0:
            prompt = "<lyco:PovGroupSex_v10:{}>, (3girls,multiple girls:1), sex ,1boy,pov,cowgirl position,smile,blush,large breasts, looking at viewer, nipples,pussy,pussy juice,penis, thighhighs,garter belt,mature female, ".format(
                get_random_weight(0.8, 0.9, 0.8, weight))
        elif diff_style == 1:
            prompt = "<lyco:PovGroupSex_v10:{}>, (3girls,multiple girls:1), sex ,1boy,pov, missionary, smile,blush,large breasts, looking at viewer, nipples,pussy,pussy juice,penis, thighhighs,garter belt,mature female, ".format(
                get_random_weight(0.8, 0.9, 0.8, weight))
        elif diff_style == 2:
            prompt = "<lyco:PovGroupSex_v10:{}>, (3girls,multiple girls:1), sex ,1boy,pov, reverse cowgirl position, ass, sex from behind, girl on top  smile,blush,large breasts, looking at viewer, nipples,pussy,pussy juice,penis, thighhighs,garter belt,mature female, ".format(
                get_random_weight(0.8, 0.9, 0.8, weight))
    elif category == LyCORIS.FUNC_EHEGAO_CUTE_2D:
        prompt = "ehegao, blush, <lyco:ehegao_v2:{}>, ".format(get_random_weight(0.8, 0.9, 0.9, weight))
    elif category == LyCORIS.CLOTHES_BRIDAL_LINGERIE:
        prompt = "bridal lingerie, bridal veil, <lyco:bridalLingerieClothes:{}>,".format(
            get_random_weight(0.7, 0.8, 0.8, weight))
    """
    return prompt


def get_random_weight(from_v, to_v=1.0, default_v=0.6, weight=None):
    if weight is not None and isinstance(weight, str):
        return weight
    final_v = 0
    if global_random_f is not True:
        final_v = default_v
    else:
        final_v = random.uniform(from_v, to_v)
    return "{:.2f}".format(final_v)


def gen_lora_prompt_list(lora_list, random_f=False):
    global global_random_f
    global_random_f = random_f
    prompt_list = []
    for lora in lora_list:
        lora_name, weight, prompt_type = convert_widget_string(lora)
        prompt_list.append(get_single_lora_prompt(lora_name, weight, diff_style=prompt_type))
    prompt = "".join(prompt_list)
    return prompt


def gen_lycoris_prompt_list(lycoris_list, random_f=False):
    global global_random_f
    global_random_f = random_f
    prompt_list = []
    for lyco in lycoris_list:
        lyco_name, weight, prompt_type = convert_widget_string(lyco)
        prompt_list.append(get_single_lycoris_prompt(lyco_name, weight, diff_style=prompt_type))
    prompt = "".join(prompt_list)
    return prompt


def get_embed_prompt(embedding_list):
    prompt = ""
    if len(embedding_list) <= 0:
        return prompt
    else:
        for embedding_str in embedding_list:
            embedding, weight, prompt_type = convert_widget_string(embedding_str)

            if embedding == Embeddings.ULZZANG:
                prompt = prompt + "(ulzzang-6500:{0}), ".format(0.6 if weight is None else weight)
            elif embedding == Embeddings.ZHUBAO:
                prompt = prompt + "(zhubao:{}), ".format(1.0 if weight is None else weight)
            elif embedding == Embeddings.SUIJING:
                prompt = prompt + "(suijing:{}), (ice crystal dress), princess of the crystal, ".format(
                    1.0 if weight is None else weight)
            elif embedding == Embeddings.N3T0P:
                prompt = prompt + "(n3t0p:0.5), "
            elif embedding == Embeddings.BEAUTIFUL_MISTAKE:
                prompt = prompt + "(beautiful_mistake-8500:{}), ".format(0.8 if weight is None else weight)
            elif embedding == Embeddings.PURE_EROS_FACE:
                prompt = prompt + "(pureerosface_v1:{}), ".format(0.8 if weight is None else weight)
            elif embedding == Embeddings.FCHEATPORTRAIT:
                prompt = prompt + "(fcHeatPortrait:0.6), "
            elif embedding == Embeddings.FCDETAILPORTRAIT:
                prompt = prompt + "(fcDetailPortrait:0.6), "
            elif embedding == Embeddings.MICROMINI:
                prompt = prompt + "(micromini:0.7), "
            elif embedding == Embeddings.UNDER_BOO:
                prompt = prompt + "(under-boo:0.6), "
    return prompt


def convert_widget_string(model_str):
    # check if model_str is int or float
    if isinstance(model_str, int) or isinstance(model_str, float):
        return model_str, None, 0
    elif isinstance(model_str, str):

        if ':' in model_str:
            splitted = model_str.split(':')
            before_colon = int(splitted[0])
            after_colon = splitted[1]
            prompt_type = '0'
            if len(splitted) > 2:
                prompt_type = splitted[2]
            if prompt_type is not None and prompt_type.isdigit():
                prompt_type = int(prompt_type)
            return before_colon, after_colon, prompt_type
        else:
            result = None
            if model_str.isdigit():
                result = int(model_str)
            return result, None, 0
    else:
        raise ValueError("model_str is not int or float or str")


def should_re_gen_prompt(lora_list):
    if len(lora_list) <= 0:
        return False
    return True

def is_special_single(lora_list):
    white_list = [LoraCategory.POSE_POV_DOGGY_ANAL, LoraCategory.POSE_PANTIES_PULLED_ASIDE_FUCK,
                  LoraCategory.POSE_POV_WAIST_GRAB_ANIMATE, LoraCategory.POSE_XIAOMA_DACHE_2D,
                  LoraCategory.CHARACTER_SHANHAIGUANWU_COS, LoraCategory.POSE_AMAZON_POSITION_ANIMATE_297,
                  LoraCategory.pose_Against_glass_sex]
    lyco_white_list = []
    for lora in lora_list:
        lora_name, weight, prompt_type = convert_widget_string(lora)
        if lora_name in white_list:
            return True

    for lyco in lora_list:
        lyco_name, weight, prompt_type = convert_widget_string(lyco)
        if lyco_name in lyco_white_list:
            return True
    return False
