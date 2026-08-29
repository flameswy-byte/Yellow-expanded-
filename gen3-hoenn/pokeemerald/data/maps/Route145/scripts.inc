Route145_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route145_EventScript_Kirby::
	trainerbattle_single TRAINER_KIRBY, Route145_Text_KirbyIntro, Route145_Text_KirbyDefeat
	msgbox Route145_Text_KirbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_KirbyIntro:
	.string "Fly at me, then.$"

Route145_Text_KirbyDefeat:
	.string "Back to the nest.$"

Route145_Text_KirbyPostBattle:
	.string "Safe travels.$"

Route145_EventScript_Lamont::
	trainerbattle_single TRAINER_LAMONT, Route145_Text_LamontIntro, Route145_Text_LamontDefeat
	msgbox Route145_Text_LamontPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LamontIntro:
	.string "Look up. That's mine.\pNow look here - battle me.$"

Route145_Text_LamontDefeat:
	.string "Grounded.$"

Route145_Text_LamontPostBattle:
	.string "Keep heading on. It opens out.$"

Route145_EventScript_Landon::
	trainerbattle_single TRAINER_LANDON, Route145_Text_LandonIntro, Route145_Text_LandonDefeat
	msgbox Route145_Text_LandonPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LandonIntro:
	.string "They circle when a battle's coming.$"

Route145_Text_LandonDefeat:
	.string "You clipped us.$"

Route145_Text_LandonPostBattle:
	.string "There's more of us further along.$"

