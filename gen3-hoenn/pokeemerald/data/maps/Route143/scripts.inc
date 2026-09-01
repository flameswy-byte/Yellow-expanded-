Route143_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route143_EventScript_Isolde::
	trainerbattle_single TRAINER_ISOLDE, Route143_Text_IsoldeIntro, Route143_Text_IsoldeDefeat
	msgbox Route143_Text_IsoldePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_IsoldeIntro:
	.string "Sandwich? No? Battle, then.$"

Route143_Text_IsoldeDefeat:
	.string "I'll pack up, then.$"

Route143_Text_IsoldePostBattle:
	.string "Safe travels.$"

Route143_EventScript_Jemma::
	trainerbattle_single TRAINER_JEMMA, Route143_Text_JemmaIntro, Route143_Text_JemmaDefeat
	msgbox Route143_Text_JemmaPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JemmaIntro:
	.string "Lovely spot for lunch.\pAnd a battle.$"

Route143_Text_JemmaDefeat:
	.string "Well, that's the afternoon gone.$"

Route143_Text_JemmaPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Hamish::
	trainerbattle_single TRAINER_HAMISH, Route143_Text_HamishIntro, Route143_Text_HamishDefeat
	msgbox Route143_Text_HamishPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HamishIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route143_Text_HamishDefeat:
	.string "Yesterday me would have lost worse.$"

Route143_Text_HamishPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route143_EventScript_Harlow::
	trainerbattle_single TRAINER_HARLOW, Route143_Text_HarlowIntro, Route143_Text_HarlowDefeat
	msgbox Route143_Text_HarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HarlowIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route143_Text_HarlowDefeat:
	.string "Aww.$"

Route143_Text_HarlowPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route143_EventScript_Hollis::
	trainerbattle_single TRAINER_HOLLIS, Route143_Text_HollisIntro, Route143_Text_HollisDefeat
	msgbox Route143_Text_HollisPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HollisIntro:
	.string "I walked all this way for a battle.$"

Route143_Text_HollisDefeat:
	.string "You're really strong!$"

Route143_Text_HollisPostBattle:
	.string "Do you know the way out? ...Me\nneither.$"

Route143_EventScript_Josie::
	trainerbattle_single TRAINER_JOSIE, Route143_Text_JosieIntro, Route143_Text_JosieDefeat
	msgbox Route143_Text_JosiePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JosieIntro:
	.string "Show me the team that got you this\nfar.$"

Route143_Text_JosieDefeat:
	.string "Good. Very good.$"

Route143_Text_JosiePostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Juno::
	trainerbattle_single TRAINER_JUNO, Route143_Text_JunoIntro, Route143_Text_JunoDefeat
	msgbox Route143_Text_JunoPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JunoIntro:
	.string "Ready when you are.$"

Route143_Text_JunoDefeat:
	.string "You've earned the ROUTE.$"

Route143_Text_JunoPostBattle:
	.string "Safe travels.$"

Route143_EventScript_Kendra::
	trainerbattle_single TRAINER_KENDRA, Route143_Text_KendraIntro, Route143_Text_KendraDefeat
	msgbox Route143_Text_KendraPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_KendraIntro:
	.string "You have the walk of someone worth\nbattling.$"

Route143_Text_KendraDefeat:
	.string "That was a real match.$"

Route143_Text_KendraPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Horace::
	trainerbattle_single TRAINER_HORACE, Route143_Text_HoraceIntro, Route143_Text_HoraceDefeat
	msgbox Route143_Text_HoracePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HoraceIntro:
	.string "Nobody out here but us.\pLet's make it count.$"

Route143_Text_HoraceDefeat:
	.string "You've a longer stride than me.$"

Route143_Text_HoracePostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Hugo::
	trainerbattle_single TRAINER_HUGO, Route143_Text_HugoIntro, Route143_Text_HugoDefeat
	msgbox Route143_Text_HugoPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HugoIntro:
	.string "The fire's out. Warm me up with a\nbattle.$"

Route143_Text_HugoDefeat:
	.string "Beaten at my own camp.$"

Route143_Text_HugoPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Idris::
	trainerbattle_single TRAINER_IDRIS, Route143_Text_IdrisIntro, Route143_Text_IdrisDefeat
	msgbox Route143_Text_IdrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_IdrisIntro:
	.string "I sleep where the ROUTE ends.$"

Route143_Text_IdrisDefeat:
	.string "Well fought.$"

Route143_Text_IdrisPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Ivor::
	trainerbattle_single TRAINER_IVOR, Route143_Text_IvorIntro, Route143_Text_IvorDefeat
	msgbox Route143_Text_IvorPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_IvorIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route143_Text_IvorDefeat:
	.string "I underestimated you.$"

Route143_Text_IvorPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Jamie::
	trainerbattle_single TRAINER_JAMIE, Route143_Text_JamieIntro, Route143_Text_JamieDefeat
	msgbox Route143_Text_JamiePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JamieIntro:
	.string "Battle me and I'll let you pass.$"

Route143_Text_JamieDefeat:
	.string "That settles it.$"

Route143_Text_JamiePostBattle:
	.string "Safe travels.$"

Route143_EventScript_Jasper::
	trainerbattle_single TRAINER_JASPER, Route143_Text_JasperIntro, Route143_Text_JasperDefeat
	msgbox Route143_Text_JasperPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JasperIntro:
	.string "Not many come this far. Battle me.$"

Route143_Text_JasperDefeat:
	.string "You've come a long way indeed.$"

Route143_Text_JasperPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Jethro::
	trainerbattle_single TRAINER_JETHRO, Route143_Text_JethroIntro, Route143_Text_JethroDefeat
	msgbox Route143_Text_JethroPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JethroIntro:
	.string "Don't hold back. I won't.$"

Route143_Text_JethroDefeat:
	.string "You didn't waste my time.$"

Route143_Text_JethroPostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Julian::
	trainerbattle_single TRAINER_JULIAN, Route143_Text_JulianIntro, Route143_Text_JulianDefeat
	msgbox Route143_Text_JulianPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JulianIntro:
	.string "I came out here for a real match.$"

Route143_Text_JulianDefeat:
	.string "Strong. Genuinely strong.$"

Route143_Text_JulianPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Jude::
	trainerbattle_single TRAINER_JUDE, Route143_Text_JudeIntro, Route143_Text_JudeDefeat
	msgbox Route143_Text_JudePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JudeIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route143_Text_JudeDefeat:
	.string "Well fought.$"

Route143_Text_JudePostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Keaton::
	trainerbattle_single TRAINER_KEATON, Route143_Text_KeatonIntro, Route143_Text_KeatonDefeat
	msgbox Route143_Text_KeatonPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_KeatonIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route143_Text_KeatonDefeat:
	.string "I underestimated you.$"

Route143_Text_KeatonPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Kestrel::
	trainerbattle_single TRAINER_KESTREL, Route143_Text_KestrelIntro, Route143_Text_KestrelDefeat
	msgbox Route143_Text_KestrelPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_KestrelIntro:
	.string "I carry everything on my back.\pIncluding a win or two.$"

Route143_Text_KestrelDefeat:
	.string "Fair enough! Fair enough.$"

Route143_Text_KestrelPostBattle:
	.string "Walk well, TRAINER.$"

