select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('wtsaf2yr') }} as float64) as poids_sondage_jeun,
    cast({{ clean_zero('lbxin') }} as float64) as insuline_uu_ml,
    cast({{ clean_zero('lbdinsi') }} as float64) as insuline_pmol_l,
    cast({{ clean_zero('lbdinlc') }} as int64) as insuline_code_limite_detection
from {{ source('nhanes_raw', 'ins_l') }}
