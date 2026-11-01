select participant_id
from {{ ref('mart_participants') }}
where motif_exclusion is null
  and (homa_ir is null or homa_ir <= 0)
