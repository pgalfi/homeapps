
BASE_CURRENCY = "DKK"

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