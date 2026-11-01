select
    case sexe_code when 1 then 'Homme' when 2 then 'Femme' end as groupe_sexe,
    case
        when age_annees < 30 then '1 - 18 à 29 ans'
        when age_annees < 40 then '2 - 30 à 39 ans'
        when age_annees < 50 then '3 - 40 à 49 ans'
        when age_annees < 60 then '4 - 50 à 59 ans'
        when age_annees < 70 then '5 - 60 à 69 ans'
        else '6 - 70 ans et plus'
    end as groupe_age,
    count(*) as n_adultes_examines,
    countif(motif_exclusion is null) as n_retenus,
    round(100 * countif(motif_exclusion is null) / count(*), 1) as pct_retenus
from `nutrition-homa-nn.nhanes_marts.mart_participants`
where age_annees >= 18
group by 1, 2
order by 1, 2