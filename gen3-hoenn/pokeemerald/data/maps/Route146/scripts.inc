Route146_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route146_EventScript_RouteSignFortreeCity::
	msgbox Route146_Text_RouteSignFortreeCity, MSGBOX_SIGN
	end

Route146_Text_RouteSignFortreeCity:
	.string "ROUTE 146\n"
	.string "{UP_ARROW} FORTREE CITY$"

// Open Hoenn - tools/trainers.py

Route146_EventScript_Marlow::
	trainerbattle_single TRAINER_MARLOW, Route146_Text_MarlowIntro, Route146_Text_MarlowDefeat
	msgbox Route146_Text_MarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MarlowIntro:
	.string "My birds saw you before I did.$"

Route146_Text_MarlowDefeat:
	.string "Down we come.$"

Route146_Text_MarlowPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Merle::
	trainerbattle_single TRAINER_MERLE, Route146_Text_MerleIntro, Route146_Text_MerleDefeat
	msgbox Route146_Text_MerlePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MerleIntro:
	.string "The sky's clear. Perfect for it.$"

Route146_Text_MerleDefeat:
	.string "The sky's yours today.$"

Route146_Text_MerlePostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Milo::
	trainerbattle_single TRAINER_MILO, Route146_Text_MiloIntro, Route146_Text_MiloDefeat
	msgbox Route146_Text_MiloPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MiloIntro:
	.string "Wings beat legs. Prove me wrong.$"

Route146_Text_MiloDefeat:
	.string "Well flown.$"

Route146_Text_MiloPostBattle:
	.string "I'll be training when you come\nback.$"

Route146_EventScript_Morgan::
	trainerbattle_single TRAINER_MORGAN, Route146_Text_MorganIntro, Route146_Text_MorganDefeat
	msgbox Route146_Text_MorganPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MorganIntro:
	.string "Fly at me, then.$"

Route146_Text_MorganDefeat:
	.string "Back to the nest.$"

Route146_Text_MorganPostBattle:
	.string "Safe travels.$"

Route146_EventScript_Mabel::
	trainerbattle_single TRAINER_MABEL, Route146_Text_MabelIntro, Route146_Text_MabelDefeat
	msgbox Route146_Text_MabelPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MabelIntro:
	.string "Lovely spot for lunch.\pAnd a battle.$"

Route146_Text_MabelDefeat:
	.string "Well, that's the afternoon gone.$"

Route146_Text_MabelPostBattle:
	.string "Keep heading on. It opens out.$"

Route146_EventScript_Mallory::
	trainerbattle_single TRAINER_MALLORY, Route146_Text_MalloryIntro, Route146_Text_MalloryDefeat
	msgbox Route146_Text_MalloryPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MalloryIntro:
	.string "I packed for two. Battle first?$"

Route146_Text_MalloryDefeat:
	.string "You've earned lunch.$"

Route146_Text_MalloryPostBattle:
	.string "There's more of us further along.$"

Route146_EventScript_Maude::
	trainerbattle_single TRAINER_MAUDE, Route146_Text_MaudeIntro, Route146_Text_MaudeDefeat
	msgbox Route146_Text_MaudePostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MaudeIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route146_Text_MaudeDefeat:
	.string "Beaten before dessert.$"

Route146_Text_MaudePostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Mira::
	trainerbattle_single TRAINER_MIRA, Route146_Text_MiraIntro, Route146_Text_MiraDefeat
	msgbox Route146_Text_MiraPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MiraIntro:
	.string "The weather held. Let's use it.$"

Route146_Text_MiraDefeat:
	.string "How nice. And how losing.$"

Route146_Text_MiraPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Murphy::
	trainerbattle_single TRAINER_MURPHY, Route146_Text_MurphyIntro, Route146_Text_MurphyDefeat
	msgbox Route146_Text_MurphyPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_MurphyIntro:
	.string "You look tough. I'm tougher.$"

Route146_Text_MurphyDefeat:
	.string "I'll train more.$"

Route146_Text_MurphyPostBattle:
	.string "I'll remember you!$"

Route146_EventScript_Neely::
	trainerbattle_single TRAINER_NEELY, Route146_Text_NeelyIntro, Route146_Text_NeelyDefeat
	msgbox Route146_Text_NeelyPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NeelyIntro:
	.string "One battle! Just one!$"

Route146_Text_NeelyDefeat:
	.string "Next time! Next time!$"

Route146_Text_NeelyPostBattle:
	.string "Come back when I'm stronger!$"

Route146_EventScript_Nevin::
	trainerbattle_single TRAINER_NEVIN, Route146_Text_NevinIntro, Route146_Text_NevinDefeat
	msgbox Route146_Text_NevinPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NevinIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route146_Text_NevinDefeat:
	.string "I'm still not lost.$"

Route146_Text_NevinPostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route146_EventScript_Nadia::
	trainerbattle_single TRAINER_NADIA, Route146_Text_NadiaIntro, Route146_Text_NadiaDefeat
	msgbox Route146_Text_NadiaPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NadiaIntro:
	.string "Don't hold back. I won't.$"

Route146_Text_NadiaDefeat:
	.string "You didn't waste my time.$"

Route146_Text_NadiaPostBattle:
	.string "There's more of us further along.$"

Route146_EventScript_Niamh::
	trainerbattle_single TRAINER_NIAMH, Route146_Text_NiamhIntro, Route146_Text_NiamhDefeat
	msgbox Route146_Text_NiamhPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NiamhIntro:
	.string "I came out here for a real match.$"

Route146_Text_NiamhDefeat:
	.string "Strong. Genuinely strong.$"

Route146_Text_NiamhPostBattle:
	.string "Rest before the next stretch.$"

Route146_EventScript_Nora::
	trainerbattle_single TRAINER_NORA, Route146_Text_NoraIntro, Route146_Text_NoraDefeat
	msgbox Route146_Text_NoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_NoraIntro:
	.string "Let's not waste each other's time.$"

Route146_Text_NoraDefeat:
	.string "I'll take that loss.$"

Route146_Text_NoraPostBattle:
	.string "Good luck out there.$"

Route146_EventScript_Oakley::
	trainerbattle_single TRAINER_OAKLEY, Route146_Text_OakleyIntro, Route146_Text_OakleyDefeat
	msgbox Route146_Text_OakleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route146_Text_OakleyIntro:
	.string "You travel light. So do I.$"

Route146_Text_OakleyDefeat:
	.string "I'll break camp early.$"

Route146_Text_OakleyPostBattle:
	.string "I'll be training when you come\nback.$"

