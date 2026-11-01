select
  coalesce(motif_exclusion, 'Retenus pour le HOMA-IR') as motif,
  count(*) as n
from `nutrition-homa-nn.nhanes_marts.mart_participants`
group by 1
order by n desc
