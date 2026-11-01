with base as (
    select
        d.participant_id,
        d.sexe_code,
        d.age_annees,
        d.grossesse_code,
        d.niveau_education_code,
        d.ratio_revenu_seuil_pauvrete,
        b.poids_kg,
        b.taille_cm,
        b.imc,
        b.tour_taille_cm,
        i.poids_sondage_jeun,
        i.insuline_uu_ml,
        i.insuline_code_limite_detection,
        g.glycemie_mg_dl,
        f.jeune_heures + coalesce(f.jeune_minutes, 0) / 60 as jeune_heures_total,
        p.moderee_frequence,
        p.moderee_unite,
        p.moderee_minutes,
        p.intense_frequence,
        p.intense_unite,
        p.intense_minutes,
        p.sedentaire_minutes
    from {{ ref('stg_demo') }} as d
    left join {{ ref('stg_bmx') }} as b on d.participant_id = b.participant_id
    left join {{ ref('stg_ins') }} as i on d.participant_id = i.participant_id
    left join {{ ref('stg_glu') }} as g on d.participant_id = g.participant_id
    left join {{ ref('stg_fastqx') }} as f on d.participant_id = f.participant_id
    left join {{ ref('stg_paq') }} as p on d.participant_id = p.participant_id
    where d.a_ete_examine
),

avec_homa as (
    select
        *,
        case
            when insuline_uu_ml is not null and glycemie_mg_dl is not null
            then glycemie_mg_dl * insuline_uu_ml / 405
        end as homa_ir
    from base
)

select
    *,
    case
        when age_annees < 18 then 'moins de 18 ans'
        when insuline_uu_ml is null or glycemie_mg_dl is null then 'insuline ou glycemie manquante'
        when grossesse_code in (1, 3) then 'grossesse ou statut indetermine'
        when jeune_heures_total is null then 'duree de jeune inconnue'
        when jeune_heures_total < 8 or jeune_heures_total >= 24 then 'jeune hors 8h a moins de 24h'
    end as motif_exclusion
from avec_homa
