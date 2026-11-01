select
  'imc' as variable,
  count(*) as n_total,
  countif(imc is null) as n_manquants,
  round(100 * countif(imc is null) / count(*), 1) as pct_manquants
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where motif_exclusion is null

union all

select
  'tour_taille_cm',
  count(*),
  countif(tour_taille_cm is null),
  round(100 * countif(tour_taille_cm is null) / count(*), 1)
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where motif_exclusion is null

union all

select
  'sedentaire_minutes',
  count(*),
  countif(sedentaire_minutes is null),
  round(100 * countif(sedentaire_minutes is null) / count(*), 1)
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where motif_exclusion is null

union all

select
  'niveau_education_code',
  count(*),
  countif(niveau_education_code is null),
  round(100 * countif(niveau_education_code is null) / count(*), 1)
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where motif_exclusion is null
