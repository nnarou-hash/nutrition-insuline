with groupes as (
    select
        homa_ir,
        case
            when sedentaire_minutes is null then null
            when sedentaire_minutes < 240 then '1 - Moins de 4 h assis par jour'
            when sedentaire_minutes < 480 then '2 - 4 h à moins de 8 h'
            else '3 - 8 h et plus'
        end as groupe_sedentarite
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null
      and homa_ir is not null
)

select distinct
    groupe_sedentarite,
    count(*) over (partition by groupe_sedentarite) as n,
    round(percentile_cont(homa_ir, 0.25) over (partition by groupe_sedentarite), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by groupe_sedentarite), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by groupe_sedentarite), 2) as homa_q3
from groupes
where groupe_sedentarite is not null
order by groupe_sedentarite