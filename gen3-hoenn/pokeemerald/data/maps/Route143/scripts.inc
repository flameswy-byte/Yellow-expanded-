Route143_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route143_EventScript_Garland::
	trainerbattle_single TRAINER_GARLAND, Route143_Text_GarlandIntro, Route143_Text_GarlandDefeat
	msgbox Route143_Text_GarlandPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GarlandIntro:
	.string "One battle! Just one!$"

Route143_Text_GarlandDefeat:
	.string "Next time! Next time!$"

Route143_Text_GarlandPostBattle:
	.string "Come back when I'm stronger!$"

Route143_EventScript_Gavin::
	trainerbattle_single TRAINER_GAVIN, Route143_Text_GavinIntro, Route143_Text_GavinDefeat
	msgbox Route143_Text_GavinPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GavinIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route143_Text_GavinDefeat:
	.string "I'm still not lost.$"

Route143_Text_GavinPostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route143_EventScript_Leona::
	trainerbattle_single TRAINER_LEONA, Route143_Text_LeonaIntro, Route143_Text_LeonaDefeat
	msgbox Route143_Text_LeonaPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_LeonaIntro:
	.string "Don't hold back. I won't.$"

Route143_Text_LeonaDefeat:
	.string "You didn't waste my time.$"

Route143_Text_LeonaPostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Lilah::
	trainerbattle_single TRAINER_LILAH, Route143_Text_LilahIntro, Route143_Text_LilahDefeat
	msgbox Route143_Text_LilahPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_LilahIntro:
	.string "I came out here for a real match.$"

Route143_Text_LilahDefeat:
	.string "Strong. Genuinely strong.$"

Route143_Text_LilahPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Lucia::
	trainerbattle_single TRAINER_LUCIA, Route143_Text_LuciaIntro, Route143_Text_LuciaDefeat
	msgbox Route143_Text_LuciaPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_LuciaIntro:
	.string "Let's not waste each other's time.$"

Route143_Text_LuciaDefeat:
	.string "I'll take that loss.$"

Route143_Text_LuciaPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Glenn::
	trainerbattle_single TRAINER_GLENN, Route143_Text_GlennIntro, Route143_Text_GlennDefeat
	msgbox Route143_Text_GlennPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GlennIntro:
	.string "You travel light. So do I.$"

Route143_Text_GlennDefeat:
	.string "I'll break camp early.$"

Route143_Text_GlennPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Griffin::
	trainerbattle_single TRAINER_GRIFFIN, Route143_Text_GriffinIntro, Route143_Text_GriffinDefeat
	msgbox Route143_Text_GriffinPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GriffinIntro:
	.string "One battle, then I'm moving on.$"

Route143_Text_GriffinDefeat:
	.string "That's me humbled.$"

Route143_Text_GriffinPostBattle:
	.string "Safe travels.$"

Route143_EventScript_Gustav::
	trainerbattle_single TRAINER_GUSTAV, Route143_Text_GustavIntro, Route143_Text_GustavDefeat
	msgbox Route143_Text_GustavPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GustavIntro:
	.string "Made camp here last night.\pBattle before I strike it?$"

Route143_Text_GustavDefeat:
	.string "Time to pack.$"

Route143_Text_GustavPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Hadley::
	trainerbattle_single TRAINER_HADLEY, Route143_Text_HadleyIntro, Route143_Text_HadleyDefeat
	msgbox Route143_Text_HadleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HadleyIntro:
	.string "A challenger! At last.$"

Route143_Text_HadleyDefeat:
	.string "The ROUTE is yours.$"

Route143_Text_HadleyPostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Hamish::
	trainerbattle_single TRAINER_HAMISH, Route143_Text_HamishIntro, Route143_Text_HamishDefeat
	msgbox Route143_Text_HamishPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HamishIntro:
	.string "I've been waiting for someone like\nyou.$"

Route143_Text_HamishDefeat:
	.string "Beaten.$"

Route143_Text_HamishPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Harlow::
	trainerbattle_single TRAINER_HARLOW, Route143_Text_HarlowIntro, Route143_Text_HarlowDefeat
	msgbox Route143_Text_HarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HarlowIntro:
	.string "Let's not waste each other's time.$"

Route143_Text_HarlowDefeat:
	.string "I'll take that loss.$"

Route143_Text_HarlowPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Hollis::
	trainerbattle_single TRAINER_HOLLIS, Route143_Text_HollisIntro, Route143_Text_HollisDefeat
	msgbox Route143_Text_HollisPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HollisIntro:
	.string "Show me the team that got you this\nfar.$"

Route143_Text_HollisDefeat:
	.string "Good. Very good.$"

Route143_Text_HollisPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Horace::
	trainerbattle_single TRAINER_HORACE, Route143_Text_HoraceIntro, Route143_Text_HoraceDefeat
	msgbox Route143_Text_HoracePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HoraceIntro:
	.string "Ready when you are.$"

Route143_Text_HoraceDefeat:
	.string "You've earned the ROUTE.$"

Route143_Text_HoracePostBattle:
	.string "Safe travels.$"

Route143_EventScript_Hugo::
	trainerbattle_single TRAINER_HUGO, Route143_Text_HugoIntro, Route143_Text_HugoDefeat
	msgbox Route143_Text_HugoPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HugoIntro:
	.string "Not many come this far. Battle me.$"

Route143_Text_HugoDefeat:
	.string "You've come a long way indeed.$"

Route143_Text_HugoPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Idris::
	trainerbattle_single TRAINER_IDRIS, Route143_Text_IdrisIntro, Route143_Text_IdrisDefeat
	msgbox Route143_Text_IdrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_IdrisIntro:
	.string "A challenger! At last.$"

Route143_Text_IdrisDefeat:
	.string "The ROUTE is yours.$"

Route143_Text_IdrisPostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Ivor::
	trainerbattle_single TRAINER_IVOR, Route143_Text_IvorIntro, Route143_Text_IvorDefeat
	msgbox Route143_Text_IvorPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_IvorIntro:
	.string "You look like you've been climbing\ntoo.\pProve it.$"

Route143_Text_IvorDefeat:
	.string "Well climbed.$"

Route143_Text_IvorPostBattle:
	.string "There's water further on. Fill up.$"

Route143_EventScript_Jamie::
	trainerbattle_single TRAINER_JAMIE, Route143_Text_JamieIntro, Route143_Text_JamieDefeat
	msgbox Route143_Text_JamiePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JamieIntro:
	.string "Rest a minute! Then battle me.$"

Route143_Text_JamieDefeat:
	.string "That's the top of me, then.$"

Route143_Text_JamiePostBattle:
	.string "Watch the loose stone past the\nridge.$"

Route143_EventScript_Jasper::
	trainerbattle_single TRAINER_JASPER, Route143_Text_JasperIntro, Route143_Text_JasperDefeat
	msgbox Route143_Text_JasperPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JasperIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route143_Text_JasperDefeat:
	.string "I underestimated you.$"

Route143_Text_JasperPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Jethro::
	trainerbattle_single TRAINER_JETHRO, Route143_Text_JethroIntro, Route143_Text_JethroDefeat
	msgbox Route143_Text_JethroPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_JethroIntro:
	.string "Battle me and I'll let you pass.$"

Route143_Text_JethroDefeat:
	.string "That settles it.$"

Route143_Text_JethroPostBattle:
	.string "Safe travels.$"

