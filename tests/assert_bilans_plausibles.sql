select participant_id, 'hdl hors bornes' as regle
from {{ ref('mart_participants_bilans') }}
where hdl is not null and (hdl < 5 or hdl > 300)
union all
select participant_id, 'cholesterol total hors bornes'
from {{ ref('mart_participants_bilans') }}
where cholesterol_total is not null and (cholesterol_total < 40 or cholesterol_total > 700)
union all
select participant_id, 'triglycerides hors bornes'
from {{ ref('mart_participants_bilans') }}
where triglycerides is not null and (triglycerides < 10 or triglycerides > 5000)
union all
select participant_id, 'hba1c hors bornes'
from {{ ref('mart_participants_bilans') }}
where hba1c is not null and (hba1c < 2 or hba1c > 20)
union all
select participant_id, 'hemoglobine hors bornes'
from {{ ref('mart_participants_bilans') }}
where hemoglobine is not null and (hemoglobine < 3 or hemoglobine > 25)
