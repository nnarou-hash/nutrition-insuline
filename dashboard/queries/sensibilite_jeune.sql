with adultes as (
    select homa_ir, imc, jeune_heures_total
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where age_annees >= 18
      and homa_ir is not null
      and imc is not null
      and (grossesse_code is null or grossesse_code = 2)
      and jeune_heures_total is not null
      and jeune_heures_total < 24
),

seuils as (
    select seuil from unnest([0, 8, 9, 12]) as seuil
),

groupes as (
    select
        s.seuil as jeune_minimum_heures,
        a.homa_ir,
        case
            when a.imc < 25 then '1 - IMC < 25'
            when a.imc < 30 then '2 - IMC 25 à < 30'
            else '3 - IMC ≥ 30'
        end as groupe_imc
    from adultes as a
    cross join seuils as s
    where a.jeune_heures_total >= s.seuil
)

select distinct
    jeune_minimum_heures,
    groupe_imc,
    count(*) over (partition by jeune_minimum_heures, groupe_imc) as n,
    round(percentile_cont(homa_ir, 0.5) over (partition by jeune_minimum_heures, groupe_imc), 2) as homa_mediane
from groupes
order by jeune_minimum_heures, groupe_imc