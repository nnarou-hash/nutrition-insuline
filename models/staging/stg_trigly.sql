select
    cast(seqn as int64) as participant_id,
    cast({{ clean_zero('lbxtlg') }} as float64) as triglycerides,
    cast({{ clean_zero('lbdldl') }} as float64) as ldl
from {{ source('nhanes_raw', 'trigly_l') }}
