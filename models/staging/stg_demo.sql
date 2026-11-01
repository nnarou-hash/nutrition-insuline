select
    cast(seqn as int64)                                  as participant_id,
    cast(riagendr as int64)                              as sexe_code,
    cast({{ clean_zero('ridageyr') }} as int64)          as age_annees,
    cast(ridstatr as int64) = 2                          as a_ete_examine,
    cast(ridexprg as int64)                              as grossesse_code,
    case
        when cast(dmdeduc2 as int64) in (7, 9) then null
        else cast(dmdeduc2 as int64)
    end                                                  as niveau_education_code,
    coalesce(cast(dmdeduc2 as int64) in (7, 9), false)   as education_refus_ou_nsp,
    cast({{ clean_zero('indfmpir') }} as float64)        as ratio_revenu_seuil_pauvrete,
    cast({{ clean_zero('wtmec2yr') }} as float64)        as poids_sondage_examen
from {{ source('nhanes_raw', 'demo_l') }}
