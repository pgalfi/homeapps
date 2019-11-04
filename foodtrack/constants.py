
BASE_CURRENCY = "DKK"

DEFAULT_UNIT_ID = 99999  # kg

MEASURE_VOLUME = 10
MEASURE_WEIGHT = 20
MEASURE_OTHER = 30

MEASURE_KINDS = {
    (MEASURE_VOLUME, "Volume"),
    (MEASURE_WEIGHT, "Weight"),
    (MEASURE_OTHER, "Other")
}

FOOD_PURCHASE_SUMM_ITEM_STORE = 10
FOOD_PURCHASE_SUMM_STORE_ITEM = 20
FOOD_PURCHASE_SUMM_ITEM = 30
FOOD_PURCHASE_SUMM_STORE = 40

FOOD_PURCHASE_SUMMARY_TYPES = (
    (FOOD_PURCHASE_SUMM_ITEM_STORE, "Summary By Item, Store"),
    (FOOD_PURCHASE_SUMM_STORE_ITEM, "Summary By Store, Item"),
    (FOOD_PURCHASE_SUMM_ITEM, "Summary By Item"),
    (FOOD_PURCHASE_SUMM_STORE, "Summary By Store"),
)

DAILY_TARGETS = 1
DYNAMIC_TAPERED = 10
DYNAMIC_DRBERGKETO = 10

PROFILE_TYPES = (
    (DAILY_TARGETS, "Daily Targets"),
    (DYNAMIC_TAPERED, "Future Implementation"),
)

LOG_BREAKFAST = 10
LOG_LUNCH = 20
LOG_DINNER = 30

DEFAULT_LOG_CATEGORIES = (
    (LOG_BREAKFAST, "Breakfast"),
    (LOG_LUNCH, "Lunch"),
    (LOG_DINNER, "Dinner")
)

PURCHASE_FOOD_DB = 10
PURCHASE_OTHER = 20

PURCHASE_ITEM_KINDS = {
    (PURCHASE_FOOD_DB, "Food from DB"),
    (PURCHASE_OTHER, "Other"),

}

FOOD_DATA_TYPES = {
    ('agricultural_acquisition', 'agricultural_acquisition'),
    ('branded_food', 'branded_food'),
    ('foundation_food', 'foundation_food'),
    ('market_acquisition', 'market_acquisition'),
    ('sample_food', 'sample_food'),
    ('sr_legacy_food', 'sr_legacy_food'),
    ('sub_sample_food', 'sub_sample_food'),
    ('survey_fndds_food', 'survey_fndds_food'),
}


NUTRIENT_TARGET_GRAMS = 10
NUTRIENT_TARGET_PERCENT = 20

NUTRIENT_TARGET_TYPES = {
    (NUTRIENT_TARGET_GRAMS, 'Daily Grams'),
    (NUTRIENT_TARGET_PERCENT, 'Daily Percentage')
}


OBJECT_FOOD = 10
OBJECT_NUTRIENT = 20
OBJECT_RECIPE = 30

OBJECT_TYPES = {
    (OBJECT_FOOD, "Food"),
    (OBJECT_NUTRIENT, "Nutrient"),
    (OBJECT_RECIPE, "Recipe")
}

DEFAULT_PREFERENCES = {

}

def get_default_prefs():
    return DEFAULT_PREFERENCES