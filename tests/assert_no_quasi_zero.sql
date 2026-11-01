select 'stg_fastqx' as modele, participant_id
from {{ ref('stg_fastqx') }}
where (jeune_minutes != 0 and abs(jeune_minutes) < 1e-9)
   or (jeune_heures != 0 and abs(jeune_heures) < 1e-9)
union all
select 'stg_ins', participant_id
from {{ ref('stg_ins') }}
where insuline_code_limite_detection is not null
  and insuline_code_limite_detection not in (0, 1)
