select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbdhdd') }} as float64) as hdl
from {{ source('nhanes_raw', 'hdl_l') }}
