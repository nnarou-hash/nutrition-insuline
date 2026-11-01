select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('phafsthr') }} as float64) as jeune_heures,
    cast({{ clean_zero('phafstmn') }} as float64) as jeune_minutes
from {{ source('nhanes_raw', 'fastqx_l') }}
