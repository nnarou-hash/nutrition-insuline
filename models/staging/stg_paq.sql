select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero(na_codes('pad790q')) }} as float64) as moderee_frequence,
    nullif(trim(pad790u), '') as moderee_unite,
    cast({{ clean_zero(na_codes('pad800')) }} as float64) as moderee_minutes,
    cast({{ clean_zero(na_codes('pad810q')) }} as float64) as intense_frequence,
    nullif(trim(pad810u), '') as intense_unite,
    cast({{ clean_zero(na_codes('pad820')) }} as float64) as intense_minutes,
    cast({{ clean_zero(na_codes('pad680')) }} as float64) as sedentaire_minutes,
    coalesce(
        abs(pad790q - 7777) < 1e-6 or abs(pad790q - 9999) < 1e-6
        or abs(pad800 - 7777) < 1e-6 or abs(pad800 - 9999) < 1e-6
        or abs(pad810q - 7777) < 1e-6 or abs(pad810q - 9999) < 1e-6
        or abs(pad820 - 7777) < 1e-6 or abs(pad820 - 9999) < 1e-6
        or abs(pad680 - 7777) < 1e-6 or abs(pad680 - 9999) < 1e-6,
        false
    ) as paq_refus_ou_nsp
from {{ source('nhanes_raw', 'paq_l') }}
