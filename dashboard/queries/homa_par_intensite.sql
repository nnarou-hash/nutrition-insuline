with groupes as (
    select
        homa_ir,
        case
            when moderee_frequence is null or intense_frequence is null then null
            when moderee_frequence = 0 and intense_frequence = 0 then '1 - Aucune activité de loisir'
            when moderee_frequence > 0 and intense_frequence = 0 then '2 - Modérée seulement'
            when moderee_frequence = 0 and intense_frequence > 0 then '3 - Intense seulement'
            else '4 - Modérée et intense'
        end as groupe_intensite
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null
      and homa_ir is not null
)

select distinct
    groupe_intensite,
    count(*) over (partition by groupe_intensite) as n,
    round(percentile_cont(homa_ir, 0.25) over (partition by groupe_intensite), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by groupe_intensite), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by groupe_intensite), 2) as homa_q3
from groupes
where groupe_intensite is not null
order by groupe_intensite