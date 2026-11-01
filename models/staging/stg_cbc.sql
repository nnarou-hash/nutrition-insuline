select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbxhgb') }} as float64) as hemoglobine
from {{ source('nhanes_raw', 'cbc_l') }}
