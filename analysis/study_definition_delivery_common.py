from cohortextractor import patients, combine_codelists
from codelists import *
from datetime import date


index_date = date.today().isoformat()


common_variables = dict(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "1970-01-01", "latest": index_date},
        "rate": "uniform",
        "incidence": 0.2,
    },

    # This line defines the study population
    population=patients.satisfying(
        """
        registered = 1
        AND
        NOT has_died
        AND 
        age <= 120
        AND 
        age>=16
        """,
        registered=patients.registered_as_of(
            index_date, 
        ),
        has_died=patients.died_from_any_cause(
            on_or_before=index_date,
            returning="binary_flag",
        ),
    ),

    has_follow_up=patients.registered_with_one_practice_between(
        start_date="index_date - 12 months",
        end_date=index_date,
        return_expectations={"incidence": 0.90},
    ),
   
    # Demographic information
    age=patients.age_as_of(
        "2021-08-31",  # PHE defined date for vaccine coverage
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    ageband=patients.categorised_as(
        {
            "0": "DEFAULT",
            "16-29": """ age >= 16 AND age < 30""",
            "30-39": """ age >= 30 AND age < 40""",
            "40-49": """ age >= 40 AND age < 50""",
            "50-59": """ age >= 50 AND age < 60""",
            "60-69": """ age >= 60 AND age < 70""",
            "70-79": """ age >= 70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",  
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "16-29": 0.25,
                    "30-39": 0.5,
                    "40-49": 0.25,
                    "50-59": 0,
                    "60-69": 0,
                    "70-79": 0,
                    "80+": 0,
                }
            },
        },
    ),
    
    
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0, "F": 1}},
        }
    ),
    
    # NHS administrative region
    region=patients.registered_practice_as_of(
        index_date,
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.2,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.1,
                    "South East": 0.2,
                },
            },
        },
    ),

    # IMD - quintile
    imd=patients.categorised_as(
        {
            "0": "DEFAULT", 
            "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            index_date,
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.05,
                    "1": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5": 0.19,
                }
            },
        },
    ),

            
            
    # BMI
    bmi=patients.categorised_as(
        {
            "Not obese": "DEFAULT",
            "Obese I (30-34.9)": """ bmi_value >= 30 AND bmi_value < 35""",
            "Obese II (35-39.9)": """ bmi_value >= 35 AND bmi_value < 40""",
            "Obese III (40+)": """ bmi_value >= 40 AND bmi_value < 100""", 
            # set maximum to avoid any impossibly extreme values being classified as obese
        },
        bmi_value=patients.most_recent_bmi(
            on_or_after="index_date - 60 months",
            minimum_age_at_measurement=16
            ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Not obese": 0.7,
                    "Obese I (30-34.9)": 0.1,
                    "Obese II (35-39.9)": 0.1,
                    "Obese III (40+)": 0.1,
                }
            },
        },
    ),
)