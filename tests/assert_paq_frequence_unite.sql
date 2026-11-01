select participant_id, 'moderee' as activite
from {{ ref('stg_paq') }}
where (moderee_frequence > 0 and moderee_unite is null)
   or (moderee_frequence = 0 and moderee_unite is not null)
union all
select participant_id, 'intense'
from {{ ref('stg_paq') }}
where (intense_frequence > 0 and intense_unite is null)
   or (intense_frequence = 0 and intense_unite is not null)
