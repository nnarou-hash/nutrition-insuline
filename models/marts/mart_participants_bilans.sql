select
    m.participant_id,
    m.sexe_code,
    m.age_annees,
    m.motif_exclusion,
    m.homa_ir,
    m.imc,
    h.hdl,
    c.cholesterol_total,
    t.triglycerides,
    t.ldl,
    g.hba1c,
    b.hemoglobine,
    f.ferritine
from {{ ref('mart_participants') }} as m
left join {{ ref('stg_hdl') }} as h on m.participant_id = h.participant_id
left join {{ ref('stg_tchol') }} as c on m.participant_id = c.participant_id
left join {{ ref('stg_trigly') }} as t on m.participant_id = t.participant_id
left join {{ ref('stg_ghb') }} as g on m.participant_id = g.participant_id
left join {{ ref('stg_cbc') }} as b on m.participant_id = b.participant_id
left join {{ ref('stg_ferritine') }} as f on m.participant_id = f.participant_id
