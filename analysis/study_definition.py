from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from codelists import *
from study_definition_delivery_common import common_variables, index_date

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1976-01-01", "latest": "2006-01-01"},
        "rate": "uniform",
        "incidence": 0.98,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),
    
    age=patients.age_as_of(
        "2020-02-29",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    
    dob=patients.date_of_birth(
    "YYYY-MM",
    return_expectations={
        "date": {"earliest": "1975-01-01", "latest": "2007-01-01"},
        "rate": "uniform",},
    ),
       
 ###############################################################################
    # COVID VACCINATION
    ###############################################################################
    # any COVID vaccination (first dose)
    covid_vacc_date=patients.with_tpp_vaccination_record(
        target_disease_matches="SARS-2 CORONAVIRUS",
        on_or_after="2020-12-01",  # check all december to date
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "2020-12-08",  # first vaccine administered on the 8/12
                "latest": index_date,
            },
                "incidence":0.9
        },
    ),
    # SECOND DOSE COVID VACCINATION
    covid_vacc_second_dose_date=patients.with_tpp_vaccination_record(
        target_disease_matches="SARS-2 CORONAVIRUS",
        on_or_after="covid_vacc_date + 19 days",
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "2020-12-29",  # first reported second dose administered on the 29/12
                "latest": index_date,
            },
                "incidence": 0.8
        },
    ),
    
    # BOOSTER (3rd) DOSE COVID VACCINATION- From https://github.com/opensafely/nhs-covid-vaccination-coverage/blob/main/analysis/study_definition_delivery.py
    ## Booster dose scehdule is 6 months from 2nd dose. However, for now, we will use an 8 week interval, 
    ## to ensure that anyone having a third dose within the primary course (immunosuppressed, from 1st Sept) 
    ## are not shown as due/missing a booster dose.
    ## however those with third doses will also eventually become eligible for booster so this may need to be revisited
    covid_vacc_third_dose_date=patients.with_tpp_vaccination_record(
        target_disease_matches="SARS-2 CORONAVIRUS",
        on_or_after="covid_vacc_second_dose_date + 56 days", 
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "2021-09-24",  # first booster dose recorded
                "latest": index_date,
            },
                "incidence": 0.1
        },
    ),
    
    # COVID VACCINATION - Pfizer BioNTech
    covid_vacc_pfizer_date=patients.with_tpp_vaccination_record(
        product_name_matches="COVID-19 mRNA Vaccine Comirnaty 30micrograms/0.3ml dose conc for susp for inj MDV (Pfizer)",
        on_or_after="2020-12-01",  # check all december to date
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "2020-12-08",  # first vaccine administered on the 8/12
                "latest": index_date,},
            "incidence": 0.7
        },
    ),
    # COVID VACCINATION - Oxford AZ
    covid_vacc_oxford_date=patients.with_tpp_vaccination_record(
        product_name_matches="COVID-19 Vac AstraZeneca (ChAdOx1 S recomb) 5x10000000000 viral particles/0.5ml dose sol for inj MDV",
        on_or_after="2020-12-01",  # check all december to date
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "2020-01-04",  # first vaccine administered on the 4/1
                "latest": index_date,
            },
            "incidence": 0.7
        },
    ),
    sex=patients.sex(
            return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0, "F": 1}},
        }
    ),
    rural_urban=patients.address_as_of(
        "2020-02-01", returning="rural_urban_classification",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"rural": 0.1, "urban": 0.9}},
        },
    ),
    bmi=patients.most_recent_bmi(
        on_or_after="2010-02-01",
        minimum_age_at_measurement=16,
        include_measurement_date=False,
        include_month=False,
        return_expectations={
            "date": {},
            "float": {"distribution": "normal", "mean": 35, "stddev": 10},
            "incidence": 0.95,
        },
    ),

)