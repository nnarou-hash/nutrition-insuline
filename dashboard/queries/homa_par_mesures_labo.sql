with base as (
    select
        sexe_code,
        homa_ir,
        m.mesure,
        m.valeur
    from `nutrition-homa-nn.nhanes_marts.mart_participants_bilans`,
    unnest([
        struct('HDL' as mesure, hdl as valeur),
        struct('Cholestérol total' as mesure, cholesterol_total as valeur),
        struct('LDL' as mesure, ldl as valeur),
        struct('Triglycérides' as mesure, triglycerides as valeur),
        struct('Hémoglobine glyquée' as mesure, hba1c as valeur),
        struct('Hémoglobine' as mesure, hemoglobine as valeur),
        struct('Ferritine' as mesure, ferritine as valeur)
    ]) as m
    where motif_exclusion is null
      and homa_ir is not null
      and m.valeur is not null
),

quartiles as (
    select
        *,
        ntile(4) over (partition by mesure, sexe_code order by valeur) as quartile
    from base
)

select distinct
    mesure,
    case sexe_code when 1 then 'Homme' when 2 then 'Femme' end as groupe_sexe,
    quartile,
    count(*) over (partition by mesure, sexe_code, quartile) as n,
    round(min(valeur) over (partition by mesure, sexe_code, quartile), 1) as valeur_min,
    round(max(valeur) over (partition by mesure, sexe_code, quartile), 1) as valeur_max,
    round(percentile_cont(homa_ir, 0.5) over (partition by mesure, sexe_code, quartile), 2) as homa_mediane
from quartiles
order by mesure, groupe_sexe, quartile