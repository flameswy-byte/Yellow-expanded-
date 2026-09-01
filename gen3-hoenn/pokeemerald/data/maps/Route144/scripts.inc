Route144_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route144_EventScript_RouteSignFallarborTown::
	msgbox Route144_Text_RouteSignFallarborTown, MSGBOX_SIGN
	end

Route144_Text_RouteSignFallarborTown:
	.string "ROUTE 144\n"
	.string "{UP_ARROW} FALLARBOR TOWN$"

// Open Hoenn - tools/trainers.py

Route144_EventScript_Lacey::
	trainerbattle_single TRAINER_LACEY, Route144_Text_LaceyIntro, Route144_Text_LaceyDefeat
	msgbox Route144_Text_LaceyPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LaceyIntro:
	.string "Not many come this far. Battle me.$"

Route144_Text_LaceyDefeat:
	.string "You've come a long way indeed.$"

Route144_Text_LaceyPostBattle:
	.string "Keep heading on. It opens out.$"

Route144_EventScript_Leona::
	trainerbattle_single TRAINER_LEONA, Route144_Text_LeonaIntro, Route144_Text_LeonaDefeat
	msgbox Route144_Text_LeonaPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LeonaIntro:
	.string "A challenger! At last.$"

Route144_Text_LeonaDefeat:
	.string "The ROUTE is yours.$"

Route144_Text_LeonaPostBattle:
	.string "There's more of us further along.$"

Route144_EventScript_Kieran::
	trainerbattle_single TRAINER_KIERAN, Route144_Text_KieranIntro, Route144_Text_KieranDefeat
	msgbox Route144_Text_KieranPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KieranIntro:
	.string "My NET is faster than your feet.$"

Route144_Text_KieranDefeat:
	.string "Squashed.$"

Route144_Text_KieranPostBattle:
	.string "Rest before the next stretch.$"

Route144_EventScript_Kirby::
	trainerbattle_single TRAINER_KIRBY, Route144_Text_KirbyIntro, Route144_Text_KirbyDefeat
	msgbox Route144_Text_KirbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KirbyIntro:
	.string "Bugs first, battles second. Or the\nother way.$"

Route144_Text_KirbyDefeat:
	.string "I'll catch a better one.$"

Route144_Text_KirbyPostBattle:
	.string "Good luck out there.$"

Route144_EventScript_Lilah::
	trainerbattle_single TRAINER_LILAH, Route144_Text_LilahIntro, Route144_Text_LilahDefeat
	msgbox Route144_Text_LilahPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LilahIntro:
	.string "My POKéMON smell of the field.$"

Route144_Text_LilahDefeat:
	.string "I'll tend the beds instead.$"

Route144_Text_LilahPostBattle:
	.string "I'll be training when you come\nback.$"

Route144_EventScript_Lamont::
	trainerbattle_single TRAINER_LAMONT, Route144_Text_LamontIntro, Route144_Text_LamontDefeat
	msgbox Route144_Text_LamontPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LamontIntro:
	.string "Battle me and I'll let you pass.$"

Route144_Text_LamontDefeat:
	.string "That settles it.$"

Route144_Text_LamontPostBattle:
	.string "Safe travels.$"

Route144_EventScript_Landon::
	trainerbattle_single TRAINER_LANDON, Route144_Text_LandonIntro, Route144_Text_LandonDefeat
	msgbox Route144_Text_LandonPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LandonIntro:
	.string "Not many come this far. Battle me.$"

Route144_Text_LandonDefeat:
	.string "You've come a long way indeed.$"

Route144_Text_LandonPostBattle:
	.string "Keep heading on. It opens out.$"

Route144_EventScript_Leslie::
	trainerbattle_single TRAINER_LESLIE, Route144_Text_LeslieIntro, Route144_Text_LeslieDefeat
	msgbox Route144_Text_LesliePostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LeslieIntro:
	.string "A challenger! At last.$"

Route144_Text_LeslieDefeat:
	.string "The ROUTE is yours.$"

Route144_Text_LesliePostBattle:
	.string "There's more of us further along.$"

Route144_EventScript_Lucia::
	trainerbattle_single TRAINER_LUCIA, Route144_Text_LuciaIntro, Route144_Text_LuciaDefeat
	msgbox Route144_Text_LuciaPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LuciaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route144_Text_LuciaDefeat:
	.string "Beaten.$"

Route144_Text_LuciaPostBattle:
	.string "Rest before the next stretch.$"

Route144_EventScript_Lewis::
	trainerbattle_single TRAINER_LEWIS, Route144_Text_LewisIntro, Route144_Text_LewisDefeat
	msgbox Route144_Text_LewisPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LewisIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route144_Text_LewisDefeat:
	.string "Well fought.$"

Route144_Text_LewisPostBattle:
	.string "Good luck out there.$"

Route144_EventScript_Logan::
	trainerbattle_single TRAINER_LOGAN, Route144_Text_LoganIntro, Route144_Text_LoganDefeat
	msgbox Route144_Text_LoganPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LoganIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route144_Text_LoganDefeat:
	.string "I underestimated you.$"

Route144_Text_LoganPostBattle:
	.string "I'll be training when you come\nback.$"

