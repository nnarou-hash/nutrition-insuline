with groupes as (
    select
        homa_ir,
        case
            when imc < 18.5 then '1 - IMC < 18,5'
            when imc < 25 then '2 - IMC 18,5 à < 25'
            when imc < 30 then '3 - IMC 25 à < 30'
            else '4 - IMC ≥ 30'
        end as groupe_imc
    from `nutrition-homa-nn.nhanes_marts.mart_participants`
    where motif_exclusion is null
      and imc is not null
      and homa_ir is not null
)

select distinct
    groupe_imc,
    count(*) over (partition by groupe_imc) as n,
    round(percentile_cont(homa_ir, 0.25) over (partition by groupe_imc), 2) as homa_q1,
    round(percentile_cont(homa_ir, 0.5) over (partition by groupe_imc), 2) as homa_mediane,
    round(percentile_cont(homa_ir, 0.75) over (partition by groupe_imc), 2) as homa_q3
from groupes
order by groupe_imc