with adultes as (
    select
        homa_ir,
        imc,
        case
            when moderee_frequence is null then null
            when moderee_frequence = 0 then 0
            when moderee_minutes is null then null
            else moderee_frequence * moderee_minutes * case moderee_unite
                when 'D' then 7
                when 'W' then 1
                when 'M' then 12 / 52
                when 'Y' then 1 / 52
            end
        end as moderee_min_semaine,
        case
            when intense_frequence is null then null
            when intense_frequence = 0 then 0
            when intense_minutes is null then null
            else intense_frequence * intense_minutes * case intense_unite
                when 'D' then 7
                when 'W' then 1
                when 'M' then 12 / 52
                when 'Y' then 1 / 52
            end
        end as intense_min_semaine
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null
),

total as (
    select
        homa_ir,
        imc,
        case
            when moderee_min_semaine is null or intense_min_semaine is null then null
            else moderee_min_semaine + intense_min_semaine
        end as activite_min_semaine
    from adultes
),

seuil as (
    select distinct
        percentile_cont(activite_min_semaine, 0.5) over () as mediane_actifs
    from total
    where activite_min_semaine > 0
),

groupes as (
    select
        t.homa_ir,
        case
            when t.imc < 25 then '1 - IMC < 25'
            when t.imc < 30 then '2 - IMC 25 à < 30'
            else '3 - IMC ≥ 30'
        end as groupe_imc,
        case
            when t.activite_min_semaine = 0 then '1 - Aucune activité de loisir déclarée'
            when t.activite_min_semaine <= s.mediane_actifs then '2 - En dessous de la médiane des actifs'
            else '3 - Au-dessus de la médiane des actifs'
        end as groupe_activite
    from total as t
    cross join seuil as s
    where t.imc is not null
      and t.homa_ir is not null
      and t.activite_min_semaine is not null
)

select distinct
    groupe_imc,
    groupe_activite,
    count(*) over (partition by groupe_imc, groupe_activite) as n,
    round(percentile_cont(homa_ir, 0.25) over (partition by groupe_imc, groupe_activite), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by groupe_imc, groupe_activite), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by groupe_imc, groupe_activite), 2) as homa_q3
from groupes
order by groupe_imc, groupe_activite