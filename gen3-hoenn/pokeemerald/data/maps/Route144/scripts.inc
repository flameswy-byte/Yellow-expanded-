Route144_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route144_EventScript_Julian::
	trainerbattle_single TRAINER_JULIAN, Route144_Text_JulianIntro, Route144_Text_JulianDefeat
	msgbox Route144_Text_JulianPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_JulianIntro:
	.string "Not many come this far. Battle me.$"

Route144_Text_JulianDefeat:
	.string "You've come a long way indeed.$"

Route144_Text_JulianPostBattle:
	.string "Keep heading on. It opens out.$"

Route144_EventScript_Mabel::
	trainerbattle_single TRAINER_MABEL, Route144_Text_MabelIntro, Route144_Text_MabelDefeat
	msgbox Route144_Text_MabelPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_MabelIntro:
	.string "A challenger! At last.$"

Route144_Text_MabelDefeat:
	.string "The ROUTE is yours.$"

Route144_Text_MabelPostBattle:
	.string "There's more of us further along.$"

Route144_EventScript_Jude::
	trainerbattle_single TRAINER_JUDE, Route144_Text_JudeIntro, Route144_Text_JudeDefeat
	msgbox Route144_Text_JudePostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_JudeIntro:
	.string "The fish can wait. You can't.$"

Route144_Text_JudeDefeat:
	.string "Should've stuck to the water.$"

Route144_Text_JudePostBattle:
	.string "They bite better at dusk out here.$"

Route144_EventScript_Keaton::
	trainerbattle_single TRAINER_KEATON, Route144_Text_KeatonIntro, Route144_Text_KeatonDefeat
	msgbox Route144_Text_KeatonPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KeatonIntro:
	.string "You've a look about you. A biting\nlook.$"

Route144_Text_KeatonDefeat:
	.string "A fine catch you are.$"

Route144_Text_KeatonPostBattle:
	.string "Still waters. Deep POKéMON.$"

Route144_EventScript_Kestrel::
	trainerbattle_single TRAINER_KESTREL, Route144_Text_KestrelIntro, Route144_Text_KestrelDefeat
	msgbox Route144_Text_KestrelPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KestrelIntro:
	.string "I hook things that fight back.\pLike you.$"

Route144_Text_KestrelDefeat:
	.string "Slipped right through.$"

Route144_Text_KestrelPostBattle:
	.string "I'll be here till the light goes.$"

Route144_EventScript_Kieran::
	trainerbattle_single TRAINER_KIERAN, Route144_Text_KieranIntro, Route144_Text_KieranDefeat
	msgbox Route144_Text_KieranPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KieranIntro:
	.string "Cast off! Let's battle.$"

Route144_Text_KieranDefeat:
	.string "Hah! Hooked myself.$"

Route144_Text_KieranPostBattle:
	.string "Tight lines, TRAINER.$"

Route144_EventScript_Kirby::
	trainerbattle_single TRAINER_KIRBY, Route144_Text_KirbyIntro, Route144_Text_KirbyDefeat
	msgbox Route144_Text_KirbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_KirbyIntro:
	.string "Quiet! ...Ah, you've scared them\noff.\pYou owe me a battle.$"

Route144_Text_KirbyDefeat:
	.string "Reeled in and thrown back.$"

Route144_Text_KirbyPostBattle:
	.string "Best water's round the bend. Try\nit.$"

Route144_EventScript_Lamont::
	trainerbattle_single TRAINER_LAMONT, Route144_Text_LamontIntro, Route144_Text_LamontDefeat
	msgbox Route144_Text_LamontPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LamontIntro:
	.string "Been here since dawn. Nothing\nbiting.\pYou'll do.$"

Route144_Text_LamontDefeat:
	.string "You're the one that got away.$"

Route144_Text_LamontPostBattle:
	.string "Bring a ROD next time and I'll show\nyou a spot.$"

Route144_EventScript_Landon::
	trainerbattle_single TRAINER_LANDON, Route144_Text_LandonIntro, Route144_Text_LandonDefeat
	msgbox Route144_Text_LandonPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LandonIntro:
	.string "My birds saw you before I did.$"

Route144_Text_LandonDefeat:
	.string "Down we come.$"

Route144_Text_LandonPostBattle:
	.string "Rest before the next stretch.$"

Route144_EventScript_Leslie::
	trainerbattle_single TRAINER_LESLIE, Route144_Text_LeslieIntro, Route144_Text_LeslieDefeat
	msgbox Route144_Text_LesliePostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LeslieIntro:
	.string "The sky's clear. Perfect for it.$"

Route144_Text_LeslieDefeat:
	.string "The sky's yours today.$"

Route144_Text_LesliePostBattle:
	.string "Good luck out there.$"

Route144_EventScript_Lewis::
	trainerbattle_single TRAINER_LEWIS, Route144_Text_LewisIntro, Route144_Text_LewisDefeat
	msgbox Route144_Text_LewisPostBattle, MSGBOX_AUTOCLOSE
	end

Route144_Text_LewisIntro:
	.string "Wings beat legs. Prove me wrong.$"

Route144_Text_LewisDefeat:
	.string "Well flown.$"

Route144_Text_LewisPostBattle:
	.string "I'll be training when you come\nback.$"

