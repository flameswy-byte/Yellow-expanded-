Route147_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route147_EventScript_Rosalind::
	trainerbattle_single TRAINER_ROSALIND, Route147_Text_RosalindIntro, Route147_Text_RosalindDefeat
	msgbox Route147_Text_RosalindPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_RosalindIntro:
	.string "Sandwich? No? Battle, then.$"

Route147_Text_RosalindDefeat:
	.string "I'll pack up, then.$"

Route147_Text_RosalindPostBattle:
	.string "Safe travels.$"

Route147_EventScript_Milo::
	trainerbattle_single TRAINER_MILO, Route147_Text_MiloIntro, Route147_Text_MiloDefeat
	msgbox Route147_Text_MiloPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_MiloIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route147_Text_MiloDefeat:
	.string "Out of my depth.$"

Route147_Text_MiloPostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route147_EventScript_Morgan::
	trainerbattle_single TRAINER_MORGAN, Route147_Text_MorganIntro, Route147_Text_MorganDefeat
	msgbox Route147_Text_MorganPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_MorganIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route147_Text_MorganDefeat:
	.string "Yesterday me would have lost worse.$"

Route147_Text_MorganPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route147_EventScript_Murphy::
	trainerbattle_single TRAINER_MURPHY, Route147_Text_MurphyIntro, Route147_Text_MurphyDefeat
	msgbox Route147_Text_MurphyPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_MurphyIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route147_Text_MurphyDefeat:
	.string "Aww.$"

Route147_Text_MurphyPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route147_EventScript_Ruby::
	trainerbattle_single TRAINER_RUBY, Route147_Text_RubyIntro, Route147_Text_RubyDefeat
	msgbox Route147_Text_RubyPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_RubyIntro:
	.string "Let's not waste each other's time.$"

Route147_Text_RubyDefeat:
	.string "I'll take that loss.$"

Route147_Text_RubyPostBattle:
	.string "Good luck out there.$"

Route147_EventScript_Sable::
	trainerbattle_single TRAINER_SABLE, Route147_Text_SableIntro, Route147_Text_SableDefeat
	msgbox Route147_Text_SablePostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_SableIntro:
	.string "Show me the team that got you this\nfar.$"

Route147_Text_SableDefeat:
	.string "Good. Very good.$"

Route147_Text_SablePostBattle:
	.string "I'll be training when you come\nback.$"

Route147_EventScript_Sorrel::
	trainerbattle_single TRAINER_SORREL, Route147_Text_SorrelIntro, Route147_Text_SorrelDefeat
	msgbox Route147_Text_SorrelPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_SorrelIntro:
	.string "Ready when you are.$"

Route147_Text_SorrelDefeat:
	.string "You've earned the ROUTE.$"

Route147_Text_SorrelPostBattle:
	.string "Safe travels.$"

