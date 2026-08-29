Route146_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route146_EventScript_Mallory::
	trainerbattle_single TRAINER_MALLORY, Route146_Text_MalloryIntro, Route146_Text_MalloryDefeat
	msgbox Route146_Text_MalloryPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MalloryIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route146_Text_MalloryDefeat:
	.string "Beaten before dessert.$"

Route146_Text_MalloryPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Maude::
	trainerbattle_single TRAINER_MAUDE, Route146_Text_MaudeIntro, Route146_Text_MaudeDefeat
	msgbox Route146_Text_MaudePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MaudeIntro:
	.string "The weather held. Let's use it.$"

Route146_Text_MaudeDefeat:
	.string "How nice. And how losing.$"

Route146_Text_MaudePostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Mira::
	trainerbattle_single TRAINER_MIRA, Route146_Text_MiraIntro, Route146_Text_MiraDefeat
	msgbox Route146_Text_MiraPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MiraIntro:
	.string "My POKéMON eat better than I do.$"

Route146_Text_MiraDefeat:
	.string "A picnic and a defeat.$"

Route146_Text_MiraPostBattle:
	.string "I'll be training when you come\nback.$"

Route146_EventScript_Nadia::
	trainerbattle_single TRAINER_NADIA, Route146_Text_NadiaIntro, Route146_Text_NadiaDefeat
	msgbox Route146_Text_NadiaPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NadiaIntro:
	.string "Sandwich? No? Battle, then.$"

Route146_Text_NadiaDefeat:
	.string "I'll pack up, then.$"

Route146_Text_NadiaPostBattle:
	.string "Safe travels.$"

Route146_EventScript_Magnus::
	trainerbattle_single TRAINER_MAGNUS, Route146_Text_MagnusIntro, Route146_Text_MagnusDefeat
	msgbox Route146_Text_MagnusPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MagnusIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route146_Text_MagnusDefeat:
	.string "I'm still not lost.$"

Route146_Text_MagnusPostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route146_EventScript_Marlow::
	trainerbattle_single TRAINER_MARLOW, Route146_Text_MarlowIntro, Route146_Text_MarlowDefeat
	msgbox Route146_Text_MarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MarlowIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route146_Text_MarlowDefeat:
	.string "Yesterday me would have lost worse.$"

Route146_Text_MarlowPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route146_EventScript_Merle::
	trainerbattle_single TRAINER_MERLE, Route146_Text_MerleIntro, Route146_Text_MerleDefeat
	msgbox Route146_Text_MerlePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MerleIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route146_Text_MerleDefeat:
	.string "Aww.$"

Route146_Text_MerlePostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route146_EventScript_Niamh::
	trainerbattle_single TRAINER_NIAMH, Route146_Text_NiamhIntro, Route146_Text_NiamhDefeat
	msgbox Route146_Text_NiamhPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NiamhIntro:
	.string "Let's not waste each other's time.$"

Route146_Text_NiamhDefeat:
	.string "I'll take that loss.$"

Route146_Text_NiamhPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Nora::
	trainerbattle_single TRAINER_NORA, Route146_Text_NoraIntro, Route146_Text_NoraDefeat
	msgbox Route146_Text_NoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NoraIntro:
	.string "Show me the team that got you this\nfar.$"

Route146_Text_NoraDefeat:
	.string "Good. Very good.$"

Route146_Text_NoraPostBattle:
	.string "I'll be training when you come\nback.$"

Route146_EventScript_Olive::
	trainerbattle_single TRAINER_OLIVE, Route146_Text_OliveIntro, Route146_Text_OliveDefeat
	msgbox Route146_Text_OlivePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_OliveIntro:
	.string "Ready when you are.$"

Route146_Text_OliveDefeat:
	.string "You've earned the ROUTE.$"

Route146_Text_OlivePostBattle:
	.string "Safe travels.$"

Route146_EventScript_Milo::
	trainerbattle_single TRAINER_MILO, Route146_Text_MiloIntro, Route146_Text_MiloDefeat
	msgbox Route146_Text_MiloPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MiloIntro:
	.string "Made camp here last night.\pBattle before I strike it?$"

Route146_Text_MiloDefeat:
	.string "Time to pack.$"

Route146_Text_MiloPostBattle:
	.string "Keep heading on. It opens out.$"

Route146_EventScript_Morgan::
	trainerbattle_single TRAINER_MORGAN, Route146_Text_MorganIntro, Route146_Text_MorganDefeat
	msgbox Route146_Text_MorganPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MorganIntro:
	.string "Nobody out here but us.\pLet's make it count.$"

Route146_Text_MorganDefeat:
	.string "You've a longer stride than me.$"

Route146_Text_MorganPostBattle:
	.string "There's more of us further along.$"

Route146_EventScript_Murphy::
	trainerbattle_single TRAINER_MURPHY, Route146_Text_MurphyIntro, Route146_Text_MurphyDefeat
	msgbox Route146_Text_MurphyPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MurphyIntro:
	.string "I've been waiting for someone like\nyou.$"

Route146_Text_MurphyDefeat:
	.string "Beaten.$"

Route146_Text_MurphyPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Neely::
	trainerbattle_single TRAINER_NEELY, Route146_Text_NeelyIntro, Route146_Text_NeelyDefeat
	msgbox Route146_Text_NeelyPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NeelyIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route146_Text_NeelyDefeat:
	.string "Well fought.$"

Route146_Text_NeelyPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Nevin::
	trainerbattle_single TRAINER_NEVIN, Route146_Text_NevinIntro, Route146_Text_NevinDefeat
	msgbox Route146_Text_NevinPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NevinIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route146_Text_NevinDefeat:
	.string "I underestimated you.$"

Route146_Text_NevinPostBattle:
	.string "I'll be training when you come\nback.$"

