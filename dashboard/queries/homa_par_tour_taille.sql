with base as (
    select
        homa_ir,
        sexe_code,
        tour_taille_cm,
        ntile(4) over (partition by sexe_code order by tour_taille_cm) as quartile_tour_taille
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null
      and homa_ir is not null
      and tour_taille_cm is not null
)

select distinct
    case sexe_code when 1 then 'Homme' when 2 then 'Femme' end as groupe_sexe,
    quartile_tour_taille,
    count(*) over (partition by sexe_code, quartile_tour_taille) as n,
    round(min(tour_taille_cm) over (partition by sexe_code, quartile_tour_taille), 1) as tour_taille_min_cm,
    round(max(tour_taille_cm) over (partition by sexe_code, quartile_tour_taille), 1) as tour_taille_max_cm,
    round(percentile_cont(homa_ir, 0.25) over (partition by sexe_code, quartile_tour_taille), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by sexe_code, quartile_tour_taille), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by sexe_code, quartile_tour_taille), 2) as homa_q3
from base
order by groupe_sexe, quartile_tour_taille