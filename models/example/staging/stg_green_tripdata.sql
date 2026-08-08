select
    -- identifiers
    cast(vendorid as int) as vendor_id,
    cast(ratecodeid as int) as rate_code_id,
    cast(pulocationid as int) pickup_location_id,
    cast(dolocationid as int) as dropoff_location_id,

    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    cast(passenger_count as int),
    cast(trip_distance as float),
    cast(trip_type as int),

    --payment info
    cast(fare_amount as numeric),
    cast(extra as numeric),
    cast(mta_tax as numeric),
    cast(tip_amount as numeric),
    cast(tolls_amount as numeric),
    cast(improvement_surcharge as numeric),
    cast(total_amount as numeric),
    cast(payment_type as int)

from {{ source('raw_data', 'green_tripdata_materialized') }}