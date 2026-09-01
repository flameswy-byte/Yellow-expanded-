Route148_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route148_EventScript_Otto::
	trainerbattle_single TRAINER_OTTO, Route148_Text_OttoIntro, Route148_Text_OttoDefeat
	msgbox Route148_Text_OttoPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_OttoIntro:
	.string "Not many come this far. Battle me.$"

Route148_Text_OttoDefeat:
	.string "You've come a long way indeed.$"

Route148_Text_OttoPostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Renata::
	trainerbattle_single TRAINER_RENATA, Route148_Text_RenataIntro, Route148_Text_RenataDefeat
	msgbox Route148_Text_RenataPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RenataIntro:
	.string "A challenger! At last.$"

Route148_Text_RenataDefeat:
	.string "The ROUTE is yours.$"

Route148_Text_RenataPostBattle:
	.string "There's more of us further along.$"

Route148_EventScript_Percy::
	trainerbattle_single TRAINER_PERCY, Route148_Text_PercyIntro, Route148_Text_PercyDefeat
	msgbox Route148_Text_PercyPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_PercyIntro:
	.string "I've been waiting for someone like\nyou.$"

Route148_Text_PercyDefeat:
	.string "Beaten.$"

Route148_Text_PercyPostBattle:
	.string "Rest before the next stretch.$"

Route148_EventScript_Porter::
	trainerbattle_single TRAINER_PORTER, Route148_Text_PorterIntro, Route148_Text_PorterDefeat
	msgbox Route148_Text_PorterPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_PorterIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route148_Text_PorterDefeat:
	.string "Well fought.$"

Route148_Text_PorterPostBattle:
	.string "Good luck out there.$"

Route148_EventScript_Rosalind::
	trainerbattle_single TRAINER_ROSALIND, Route148_Text_RosalindIntro, Route148_Text_RosalindDefeat
	msgbox Route148_Text_RosalindPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RosalindIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route148_Text_RosalindDefeat:
	.string "I underestimated you.$"

Route148_Text_RosalindPostBattle:
	.string "I'll be training when you come\nback.$"

Route148_EventScript_Ruby::
	trainerbattle_single TRAINER_RUBY, Route148_Text_RubyIntro, Route148_Text_RubyDefeat
	msgbox Route148_Text_RubyPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RubyIntro:
	.string "Battle me and I'll let you pass.$"

Route148_Text_RubyDefeat:
	.string "That settles it.$"

Route148_Text_RubyPostBattle:
	.string "Safe travels.$"

Route148_EventScript_Quinn::
	trainerbattle_single TRAINER_QUINN, Route148_Text_QuinnIntro, Route148_Text_QuinnDefeat
	msgbox Route148_Text_QuinnPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_QuinnIntro:
	.string "Not many come this far. Battle me.$"

Route148_Text_QuinnDefeat:
	.string "You've come a long way indeed.$"

Route148_Text_QuinnPostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Rafe::
	trainerbattle_single TRAINER_RAFE, Route148_Text_RafeIntro, Route148_Text_RafeDefeat
	msgbox Route148_Text_RafePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RafeIntro:
	.string "$"

Route148_Text_RafeDefeat:
	.string "K$"

Route148_Text_RafePostBattle:
	.string "$"

Route148_EventScript_Sable::
	trainerbattle_single TRAINER_SABLE, Route148_Text_SableIntro, Route148_Text_SableDefeat
	msgbox Route148_Text_SablePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SableIntro:
	.string "I've been waiting for someone like\nyou.$"

Route148_Text_SableDefeat:
	.string "Beaten.$"

Route148_Text_SablePostBattle:
	.string "Rest before the next stretch.$"

Route148_EventScript_Sorrel::
	trainerbattle_single TRAINER_SORREL, Route148_Text_SorrelIntro, Route148_Text_SorrelDefeat
	msgbox Route148_Text_SorrelPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SorrelIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route148_Text_SorrelDefeat:
	.string "Well fought.$"

Route148_Text_SorrelPostBattle:
	.string "Good luck out there.$"

Route148_EventScript_Reeves::
	trainerbattle_single TRAINER_REEVES, Route148_Text_ReevesIntro, Route148_Text_ReevesDefeat
	msgbox Route148_Text_ReevesPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_ReevesIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route148_Text_ReevesDefeat:
	.string "I underestimated you.$"

Route148_Text_ReevesPostBattle:
	.string "I'll be training when you come\nback.$"

Route148_EventScript_Selma::
	trainerbattle_single TRAINER_SELMA, Route148_Text_SelmaIntro, Route148_Text_SelmaDefeat
	msgbox Route148_Text_SelmaPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SelmaIntro:
	.string "Battle me and I'll let you pass.$"

Route148_Text_SelmaDefeat:
	.string "That settles it.$"

Route148_Text_SelmaPostBattle:
	.string "Safe travels.$"

Route148_EventScript_Sigrid::
	trainerbattle_single TRAINER_SIGRID, Route148_Text_SigridIntro, Route148_Text_SigridDefeat
	msgbox Route148_Text_SigridPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SigridIntro:
	.string "Not many come this far. Battle me.$"

Route148_Text_SigridDefeat:
	.string "You've come a long way indeed.$"

Route148_Text_SigridPostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Reggie::
	trainerbattle_single TRAINER_REGGIE, Route148_Text_ReggieIntro, Route148_Text_ReggieDefeat
	msgbox Route148_Text_ReggiePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_ReggieIntro:
	.string "A challenger! At last.$"

Route148_Text_ReggieDefeat:
	.string "The ROUTE is yours.$"

Route148_Text_ReggiePostBattle:
	.string "There's more of us further along.$"

Route148_EventScript_Rhys::
	trainerbattle_single TRAINER_RHYS, Route148_Text_RhysIntro, Route148_Text_RhysDefeat
	msgbox Route148_Text_RhysPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RhysIntro:
	.string "I've been waiting for someone like\nyou.$"

Route148_Text_RhysDefeat:
	.string "Beaten.$"

Route148_Text_RhysPostBattle:
	.string "Rest before the next stretch.$"

Route148_EventScript_Simone::
	trainerbattle_single TRAINER_SIMONE, Route148_Text_SimoneIntro, Route148_Text_SimoneDefeat
	msgbox Route148_Text_SimonePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SimoneIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route148_Text_SimoneDefeat:
	.string "Well fought.$"

Route148_Text_SimonePostBattle:
	.string "Good luck out there.$"

Route148_EventScript_Roscoe::
	trainerbattle_single TRAINER_ROSCOE, Route148_Text_RoscoeIntro, Route148_Text_RoscoeDefeat
	msgbox Route148_Text_RoscoePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RoscoeIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route148_Text_RoscoeDefeat:
	.string "I underestimated you.$"

Route148_Text_RoscoePostBattle:
	.string "I'll be training when you come\nback.$"

