select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbxtc') }} as float64) as cholesterol_total
from {{ source('nhanes_raw', 'tchol_l') }}
