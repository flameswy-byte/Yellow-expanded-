Route146_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route146_EventScript_Nora::
	trainerbattle_single TRAINER_NORA, Route146_Text_NoraIntro, Route146_Text_NoraDefeat
	msgbox Route146_Text_NoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NoraIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route146_Text_NoraDefeat:
	.string "Beaten before dessert.$"

Route146_Text_NoraPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Olive::
	trainerbattle_single TRAINER_OLIVE, Route146_Text_OliveIntro, Route146_Text_OliveDefeat
	msgbox Route146_Text_OlivePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_OliveIntro:
	.string "The weather held. Let's use it.$"

Route146_Text_OliveDefeat:
	.string "How nice. And how losing.$"

Route146_Text_OlivePostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Paige::
	trainerbattle_single TRAINER_PAIGE, Route146_Text_PaigeIntro, Route146_Text_PaigeDefeat
	msgbox Route146_Text_PaigePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_PaigeIntro:
	.string "My POKéMON eat better than I do.$"

Route146_Text_PaigeDefeat:
	.string "A picnic and a defeat.$"

Route146_Text_PaigePostBattle:
	.string "I'll be training when you come\nback.$"

Route146_EventScript_Petronella::
	trainerbattle_single TRAINER_PETRONELLA, Route146_Text_PetronellaIntro, Route146_Text_PetronellaDefeat
	msgbox Route146_Text_PetronellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_PetronellaIntro:
	.string "Sandwich? No? Battle, then.$"

Route146_Text_PetronellaDefeat:
	.string "I'll pack up, then.$"

Route146_Text_PetronellaPostBattle:
	.string "Safe travels.$"

Route146_EventScript_Leslie::
	trainerbattle_single TRAINER_LESLIE, Route146_Text_LeslieIntro, Route146_Text_LeslieDefeat
	msgbox Route146_Text_LesliePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_LeslieIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route146_Text_LeslieDefeat:
	.string "I'm still not lost.$"

Route146_Text_LesliePostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route146_EventScript_Lewis::
	trainerbattle_single TRAINER_LEWIS, Route146_Text_LewisIntro, Route146_Text_LewisDefeat
	msgbox Route146_Text_LewisPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_LewisIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route146_Text_LewisDefeat:
	.string "Yesterday me would have lost worse.$"

Route146_Text_LewisPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route146_EventScript_Logan::
	trainerbattle_single TRAINER_LOGAN, Route146_Text_LoganIntro, Route146_Text_LoganDefeat
	msgbox Route146_Text_LoganPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_LoganIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route146_Text_LoganDefeat:
	.string "Aww.$"

Route146_Text_LoganPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route146_EventScript_Piper::
	trainerbattle_single TRAINER_PIPER, Route146_Text_PiperIntro, Route146_Text_PiperDefeat
	msgbox Route146_Text_PiperPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_PiperIntro:
	.string "Let's not waste each other's time.$"

Route146_Text_PiperDefeat:
	.string "I'll take that loss.$"

Route146_Text_PiperPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Ramona::
	trainerbattle_single TRAINER_RAMONA, Route146_Text_RamonaIntro, Route146_Text_RamonaDefeat
	msgbox Route146_Text_RamonaPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_RamonaIntro:
	.string "Show me the team that got you this\nfar.$"

Route146_Text_RamonaDefeat:
	.string "Good. Very good.$"

Route146_Text_RamonaPostBattle:
	.string "I'll be training when you come\nback.$"

Route146_EventScript_Renata::
	trainerbattle_single TRAINER_RENATA, Route146_Text_RenataIntro, Route146_Text_RenataDefeat
	msgbox Route146_Text_RenataPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_RenataIntro:
	.string "Ready when you are.$"

Route146_Text_RenataDefeat:
	.string "You've earned the ROUTE.$"

Route146_Text_RenataPostBattle:
	.string "Safe travels.$"

Route146_EventScript_Lorcan::
	trainerbattle_single TRAINER_LORCAN, Route146_Text_LorcanIntro, Route146_Text_LorcanDefeat
	msgbox Route146_Text_LorcanPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_LorcanIntro:
	.string "Made camp here last night.\pBattle before I strike it?$"

Route146_Text_LorcanDefeat:
	.string "Time to pack.$"

Route146_Text_LorcanPostBattle:
	.string "Keep heading on. It opens out.$"

Route146_EventScript_Ludo::
	trainerbattle_single TRAINER_LUDO, Route146_Text_LudoIntro, Route146_Text_LudoDefeat
	msgbox Route146_Text_LudoPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_LudoIntro:
	.string "Nobody out here but us.\pLet's make it count.$"

Route146_Text_LudoDefeat:
	.string "You've a longer stride than me.$"

Route146_Text_LudoPostBattle:
	.string "There's more of us further along.$"

Route146_EventScript_Magnus::
	trainerbattle_single TRAINER_MAGNUS, Route146_Text_MagnusIntro, Route146_Text_MagnusDefeat
	msgbox Route146_Text_MagnusPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MagnusIntro:
	.string "I've been waiting for someone like\nyou.$"

Route146_Text_MagnusDefeat:
	.string "Beaten.$"

Route146_Text_MagnusPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Marlow::
	trainerbattle_single TRAINER_MARLOW, Route146_Text_MarlowIntro, Route146_Text_MarlowDefeat
	msgbox Route146_Text_MarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MarlowIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route146_Text_MarlowDefeat:
	.string "Well fought.$"

Route146_Text_MarlowPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Merle::
	trainerbattle_single TRAINER_MERLE, Route146_Text_MerleIntro, Route146_Text_MerleDefeat
	msgbox Route146_Text_MerlePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MerleIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route146_Text_MerleDefeat:
	.string "I underestimated you.$"

Route146_Text_MerlePostBattle:
	.string "I'll be training when you come\nback.$"

