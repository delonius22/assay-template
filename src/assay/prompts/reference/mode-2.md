# Mode 2: change or fix to an existing system

A current-state map of the code has been made and corrected by developers.
Grill the gap between how the system works now and how it should work.

Defects: can it be reproduced; what is the CONFIRMED cause versus the
suspected cause (never record a suspicion as a decision); since when; what
is the customer or financial impact; do past records need remediation; is a
workaround in place.

Enhancements: who depends on current behaviour, including reports and
downstream systems; is it backward compatible; does data need migrating;
can it ship behind a flag and roll back.

Both: blast radius, regression tests, and whether an existing control,
approval step, audit log, or reconciliation changes (and who owns it).
