select participant_id, 'imc hors bornes' as regle
from {{ ref('stg_bmx') }}
where imc is not null and (imc < 8 or imc > 100)
union all
select participant_id, 'poids hors bornes'
from {{ ref('stg_bmx') }}
where poids_kg is not null and (poids_kg < 1 or poids_kg > 400)
union all
select participant_id, 'taille hors bornes'
from {{ ref('stg_bmx') }}
where taille_cm is not null and (taille_cm < 40 or taille_cm > 250)
union all
select participant_id, 'tour de taille hors bornes'
from {{ ref('stg_bmx') }}
where tour_taille_cm is not null and (tour_taille_cm < 20 or tour_taille_cm > 250)
union all
select participant_id, 'imc incoherent avec poids et taille'
from {{ ref('stg_bmx') }}
where imc is not null and poids_kg is not null and taille_cm is not null
  and abs(imc - poids_kg / pow(taille_cm / 100, 2)) > 0.5
