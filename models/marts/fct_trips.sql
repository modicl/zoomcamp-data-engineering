/*
TO DO :
- ONE ROW PER TRIP (DOESNT MATTER IF YELLOW OR GREEN)
- ADD A PRIMARY KEY (trip_id). IT HAS TO BE UNIQUE .
- FIND ALL THE DUPLICATES, UNDERSTAND WHY THEY HAPPEN, AND FIX THEM.
- FIND A WAY TO ENRICH THE COLUMN payment_type.

*/

with payment_types as (
    select * from {{ ref('payment_type_lookup')}}

),
trips_unioned as (
    select * from {{ ref("int_trips_union")}}
)


select 
    vendor_id,
    rate_coid_id,
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
    payment_types.description as payment_type,

from trips_unioned as fct_trips
join fct_trips on payment_types where fct_trips.payment_type = payment_types.payment_type

select * from fct_trips