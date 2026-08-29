Route136_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route136_EventScript_Bonnie::
	trainerbattle_single TRAINER_BONNIE, Route136_Text_BonnieIntro, Route136_Text_BonnieDefeat
	msgbox Route136_Text_BonniePostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BonnieIntro:
	.string "Cold? You get used to it.$"

Route136_Text_BonnieDefeat:
	.string "I'll float here a while.$"

Route136_Text_BonniePostBattle:
	.string "I'll race you next time.$"

Route136_EventScript_Briar::
	trainerbattle_single TRAINER_BRIAR, Route136_Text_BriarIntro, Route136_Text_BriarDefeat
	msgbox Route136_Text_BriarPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BriarIntro:
	.string "Battle me and I'll let you pass.$"

Route136_Text_BriarDefeat:
	.string "That settles it.$"

Route136_Text_BriarPostBattle:
	.string "Safe travels.$"

Route136_EventScript_Arlo::
	trainerbattle_single TRAINER_ARLO, Route136_Text_ArloIntro, Route136_Text_ArloDefeat
	msgbox Route136_Text_ArloPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_ArloIntro:
	.string "Not many come this far. Battle me.$"

Route136_Text_ArloDefeat:
	.string "You've come a long way indeed.$"

Route136_Text_ArloPostBattle:
	.string "Keep heading on. It opens out.$"

Route136_EventScript_Asher::
	trainerbattle_single TRAINER_ASHER, Route136_Text_AsherIntro, Route136_Text_AsherDefeat
	msgbox Route136_Text_AsherPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_AsherIntro:
	.string "A challenger! At last.$"

Route136_Text_AsherDefeat:
	.string "The ROUTE is yours.$"

Route136_Text_AsherPostBattle:
	.string "There's more of us further along.$"

Route136_EventScript_Branwen::
	trainerbattle_single TRAINER_BRANWEN, Route136_Text_BranwenIntro, Route136_Text_BranwenDefeat
	msgbox Route136_Text_BranwenPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BranwenIntro:
	.string "I've been waiting for someone like\nyou.$"

Route136_Text_BranwenDefeat:
	.string "Beaten.$"

Route136_Text_BranwenPostBattle:
	.string "Rest before the next stretch.$"

