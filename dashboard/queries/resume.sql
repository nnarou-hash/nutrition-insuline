select
  count(*) as adultes_retenus,
  countif(moderee_frequence is null or intense_frequence is null) as activite_inconnue
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where motif_exclusion is null
