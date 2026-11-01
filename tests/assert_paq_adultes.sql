select p.participant_id
from {{ ref('stg_paq') }} as p
inner join {{ ref('stg_demo') }} as d on p.participant_id = d.participant_id
where d.age_annees < 18
