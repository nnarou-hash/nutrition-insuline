with groupes as (
    select
        homa_ir,
        case
            when age_annees < 30 then '1 - 18 à 29 ans'
            when age_annees < 40 then '2 - 30 à 39 ans'
            when age_annees < 50 then '3 - 40 à 49 ans'
            when age_annees < 60 then '4 - 50 à 59 ans'
            when age_annees < 70 then '5 - 60 à 69 ans'
            else '6 - 70 ans et plus'
        end as groupe_age,
        case sexe_code when 1 then 'Homme' when 2 then 'Femme' end as groupe_sexe
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null and homa_ir is not null
)
select distinct
    groupe_age,
    groupe_sexe,
    count(*) over (partition by groupe_age, groupe_sexe) as n,
    round(percentile_cont(homa_ir, 0.25) over (partition by groupe_age, groupe_sexe), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by groupe_age, groupe_sexe), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by groupe_age, groupe_sexe), 2) as homa_q3
from groupes
order by groupe_age, groupe_sexe