with green_tripdata as (
    select * from {{ ref('stg_green_tripdata') }}
),

yellow_tripdata as (
    select * from {{ ref('stg_yellow_tripdata')}}
),

trip_union as (
    select * from green_tripdata
    union all
    select * from yellow_tripdata
)

select distinct pickup_location_id from trip_union