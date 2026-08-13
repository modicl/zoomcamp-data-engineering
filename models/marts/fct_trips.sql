/*
TO DO :
- ONE ROW PER TRIP (DOESNT MATTER IF YELLOW OR GREEN) OK
- ADD A PRIMARY KEY (trip_id). IT HAS TO BE UNIQUE . OK
- FIND ALL THE DUPLICATES, UNDERSTAND WHY THEY HAPPEN, AND FIX THEM.
- FIND A WAY TO ENRICH THE COLUMN payment_type. OK

*/
with
    payment_types as (select * from {{ ref("payment_type_lookup") }}),
    trips_unioned as (select * from {{ ref("int_trips_union") }})

select
    {{
        dbt_utils.generate_surrogate_key(
            [
                "vendor_id",
                "pickup_datetime",
                "dropoff_datetime",
                "pickup_location_id",
                "dropoff_location_id",
                "passenger_count",
                "trip_distance",
                "total_amount",
                "pt.description"
            ]
        )
    }} as trip_id,
    vendor_id,
    rate_code_id,
    pickup_location_id,
    dropoff_location_id,
    pickup_datetime,
    dropoff_datetime,
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    trip_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    pt.description as payment_type,
    {{ get_is_chargeback('total_amount') }} as is_chargeback
    
from trips_unioned as fct_trips
left join payment_types as pt on fct_trips.payment_type = pt.payment_type
