select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbxfer') }} as float64) as ferritine
from {{ source('nhanes_raw', 'fertin_l') }}
