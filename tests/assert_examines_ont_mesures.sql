select d.participant_id
from {{ ref('stg_demo') }} as d
left join {{ ref('stg_bmx') }} as b on d.participant_id = b.participant_id
where d.a_ete_examine and b.participant_id is null
