select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbxgh') }} as float64) as hba1c
from {{ source('nhanes_raw', 'ghb_l') }}
