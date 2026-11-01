with base as (
    select
        b.sexe_code,
        b.homa_ir,
        m.tour_taille_cm,
        b.imc,
        b.hdl,
        b.cholesterol_total,
        b.ldl,
        b.triglycerides,
        b.hba1c,
        b.hemoglobine,
        b.ferritine
    from `nutrition-homa-nn.nhanes_marts.mart_participants_bilans` as b
    inner join `nutrition-homa-nn.nhanes_marts.mart_participants` as m
        on b.participant_id = m.participant_id
    where b.motif_exclusion is null
      and b.homa_ir is not null
),

long as (
    select sexe_code, homa_ir, x.mesure, x.valeur
    from base,
    unnest([
        struct('IMC' as mesure, imc as valeur),
        struct('Tour de taille' as mesure, tour_taille_cm as valeur),
        struct('HDL' as mesure, hdl as valeur),
        struct('Cholestérol total' as mesure, cholesterol_total as valeur),
        struct('LDL' as mesure, ldl as valeur),
        struct('Triglycérides' as mesure, triglycerides as valeur),
        struct('Hémoglobine glyquée' as mesure, hba1c as valeur),
        struct('Hémoglobine' as mesure, hemoglobine as valeur),
        struct('Ferritine' as mesure, ferritine as valeur)
    ]) as x
    where x.valeur is not null
),

rangs as (
    select
        sexe_code,
        mesure,
        rank() over (partition by sexe_code, mesure order by homa_ir) as rang_homa,
        rank() over (partition by sexe_code, mesure order by valeur) as rang_valeur
    from long
)

select
    mesure,
    case sexe_code when 1 then 'Homme' when 2 then 'Femme' end as groupe_sexe,
    count(*) as n,
    round(corr(rang_homa, rang_valeur), 2) as correlation_spearman
from rangs
group by mesure, sexe_code
order by mesure, groupe_sexe