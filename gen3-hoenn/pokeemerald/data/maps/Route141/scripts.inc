Route141_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route141_EventScript_Gustav::
	trainerbattle_single TRAINER_GUSTAV, Route141_Text_GustavIntro, Route141_Text_GustavDefeat
	msgbox Route141_Text_GustavPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_GustavIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route141_Text_GustavDefeat:
	.string "I underestimated you.$"

Route141_Text_GustavPostBattle:
	.string "I'll be training when you come\nback.$"

Route141_EventScript_Hadley::
	trainerbattle_single TRAINER_HADLEY, Route141_Text_HadleyIntro, Route141_Text_HadleyDefeat
	msgbox Route141_Text_HadleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_HadleyIntro:
	.string "Battle me and I'll let you pass.$"

Route141_Text_HadleyDefeat:
	.string "That settles it.$"

Route141_Text_HadleyPostBattle:
	.string "Safe travels.$"

Route141_EventScript_Harriet::
	trainerbattle_single TRAINER_HARRIET, Route141_Text_HarrietIntro, Route141_Text_HarrietDefeat
	msgbox Route141_Text_HarrietPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_HarrietIntro:
	.string "Not many come this far. Battle me.$"

Route141_Text_HarrietDefeat:
	.string "You've come a long way indeed.$"

Route141_Text_HarrietPostBattle:
	.string "Keep heading on. It opens out.$"

Route141_EventScript_Hamish::
	trainerbattle_single TRAINER_HAMISH, Route141_Text_HamishIntro, Route141_Text_HamishDefeat
	msgbox Route141_Text_HamishPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_HamishIntro:
	.string "A challenger! At last.$"

Route141_Text_HamishDefeat:
	.string "The ROUTE is yours.$"

Route141_Text_HamishPostBattle:
	.string "There's more of us further along.$"

