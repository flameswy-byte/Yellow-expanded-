Route145_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route145_EventScript_Lucia::
	trainerbattle_single TRAINER_LUCIA, Route145_Text_LuciaIntro, Route145_Text_LuciaDefeat
	msgbox Route145_Text_LuciaPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LuciaIntro:
	.string "Battle me and I'll let you pass.$"

Route145_Text_LuciaDefeat:
	.string "That settles it.$"

Route145_Text_LuciaPostBattle:
	.string "Safe travels.$"

Route145_EventScript_Ludo::
	trainerbattle_single TRAINER_LUDO, Route145_Text_LudoIntro, Route145_Text_LudoDefeat
	msgbox Route145_Text_LudoPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LudoIntro:
	.string "Not many come this far. Battle me.$"

Route145_Text_LudoDefeat:
	.string "You've come a long way indeed.$"

Route145_Text_LudoPostBattle:
	.string "Keep heading on. It opens out.$"

Route145_EventScript_Mabel::
	trainerbattle_single TRAINER_MABEL, Route145_Text_MabelIntro, Route145_Text_MabelDefeat
	msgbox Route145_Text_MabelPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_MabelIntro:
	.string "A challenger! At last.$"

Route145_Text_MabelDefeat:
	.string "The ROUTE is yours.$"

Route145_Text_MabelPostBattle:
	.string "There's more of us further along.$"

