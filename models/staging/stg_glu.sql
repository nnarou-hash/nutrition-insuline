select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('wtsaf2yr') }} as float64) as poids_sondage_jeun,
    cast({{ clean_zero('lbxglu') }} as float64) as glycemie_mg_dl,
    cast({{ clean_zero('lbdglusi') }} as float64) as glycemie_mmol_l
from {{ source('nhanes_raw', 'glu_l') }}
