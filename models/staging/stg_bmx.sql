select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('bmxwt') }} as float64) as poids_kg,
    cast({{ clean_zero('bmxht') }} as float64) as taille_cm,
    cast({{ clean_zero('bmxbmi') }} as float64) as imc,
    cast({{ clean_zero('bmxwaist') }} as float64) as tour_taille_cm
from {{ source('nhanes_raw', 'bmx_l') }}
