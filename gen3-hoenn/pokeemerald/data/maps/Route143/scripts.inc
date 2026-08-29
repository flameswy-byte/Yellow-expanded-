Route143_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route143_EventScript_Gabe::
	trainerbattle_single TRAINER_GABE, Route143_Text_GabeIntro, Route143_Text_GabeDefeat
	msgbox Route143_Text_GabePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GabeIntro:
	.string "Cast off! Let's battle.$"

Route143_Text_GabeDefeat:
	.string "Hah! Hooked myself.$"

Route143_Text_GabePostBattle:
	.string "Tight lines, TRAINER.$"

Route143_EventScript_Garland::
	trainerbattle_single TRAINER_GARLAND, Route143_Text_GarlandIntro, Route143_Text_GarlandDefeat
	msgbox Route143_Text_GarlandPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GarlandIntro:
	.string "Quiet! ...Ah, you've scared them\noff.\pYou owe me a battle.$"

Route143_Text_GarlandDefeat:
	.string "Reeled in and thrown back.$"

Route143_Text_GarlandPostBattle:
	.string "Best water's round the bend. Try\nit.$"

Route143_EventScript_Gavin::
	trainerbattle_single TRAINER_GAVIN, Route143_Text_GavinIntro, Route143_Text_GavinDefeat
	msgbox Route143_Text_GavinPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GavinIntro:
	.string "Been here since dawn. Nothing\nbiting.\pYou'll do.$"

Route143_Text_GavinDefeat:
	.string "You're the one that got away.$"

Route143_Text_GavinPostBattle:
	.string "Bring a ROD next time and I'll show\nyou a spot.$"

Route143_EventScript_Glenn::
	trainerbattle_single TRAINER_GLENN, Route143_Text_GlennIntro, Route143_Text_GlennDefeat
	msgbox Route143_Text_GlennPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GlennIntro:
	.string "My birds saw you before I did.$"

Route143_Text_GlennDefeat:
	.string "Down we come.$"

Route143_Text_GlennPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Griffin::
	trainerbattle_single TRAINER_GRIFFIN, Route143_Text_GriffinIntro, Route143_Text_GriffinDefeat
	msgbox Route143_Text_GriffinPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GriffinIntro:
	.string "The sky's clear. Perfect for it.$"

Route143_Text_GriffinDefeat:
	.string "The sky's yours today.$"

Route143_Text_GriffinPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Gustav::
	trainerbattle_single TRAINER_GUSTAV, Route143_Text_GustavIntro, Route143_Text_GustavDefeat
	msgbox Route143_Text_GustavPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_GustavIntro:
	.string "Wings beat legs. Prove me wrong.$"

Route143_Text_GustavDefeat:
	.string "Well flown.$"

Route143_Text_GustavPostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Hadley::
	trainerbattle_single TRAINER_HADLEY, Route143_Text_HadleyIntro, Route143_Text_HadleyDefeat
	msgbox Route143_Text_HadleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HadleyIntro:
	.string "Fly at me, then.$"

Route143_Text_HadleyDefeat:
	.string "Back to the nest.$"

Route143_Text_HadleyPostBattle:
	.string "Safe travels.$"

Route143_EventScript_Lilah::
	trainerbattle_single TRAINER_LILAH, Route143_Text_LilahIntro, Route143_Text_LilahDefeat
	msgbox Route143_Text_LilahPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_LilahIntro:
	.string "Lovely spot for lunch.\pAnd a battle.$"

Route143_Text_LilahDefeat:
	.string "Well, that's the afternoon gone.$"

Route143_Text_LilahPostBattle:
	.string "Keep heading on. It opens out.$"

Route143_EventScript_Lucia::
	trainerbattle_single TRAINER_LUCIA, Route143_Text_LuciaIntro, Route143_Text_LuciaDefeat
	msgbox Route143_Text_LuciaPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_LuciaIntro:
	.string "I packed for two. Battle first?$"

Route143_Text_LuciaDefeat:
	.string "You've earned lunch.$"

Route143_Text_LuciaPostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Mabel::
	trainerbattle_single TRAINER_MABEL, Route143_Text_MabelIntro, Route143_Text_MabelDefeat
	msgbox Route143_Text_MabelPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_MabelIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route143_Text_MabelDefeat:
	.string "Beaten before dessert.$"

Route143_Text_MabelPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Mallory::
	trainerbattle_single TRAINER_MALLORY, Route143_Text_MalloryIntro, Route143_Text_MalloryDefeat
	msgbox Route143_Text_MalloryPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_MalloryIntro:
	.string "The weather held. Let's use it.$"

Route143_Text_MalloryDefeat:
	.string "How nice. And how losing.$"

Route143_Text_MalloryPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Hamish::
	trainerbattle_single TRAINER_HAMISH, Route143_Text_HamishIntro, Route143_Text_HamishDefeat
	msgbox Route143_Text_HamishPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HamishIntro:
	.string "You look tough. I'm tougher.$"

Route143_Text_HamishDefeat:
	.string "I'll train more.$"

Route143_Text_HamishPostBattle:
	.string "I'll remember you!$"

Route143_EventScript_Harlow::
	trainerbattle_single TRAINER_HARLOW, Route143_Text_HarlowIntro, Route143_Text_HarlowDefeat
	msgbox Route143_Text_HarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HarlowIntro:
	.string "One battle! Just one!$"

Route143_Text_HarlowDefeat:
	.string "Next time! Next time!$"

Route143_Text_HarlowPostBattle:
	.string "Come back when I'm stronger!$"

Route143_EventScript_Hollis::
	trainerbattle_single TRAINER_HOLLIS, Route143_Text_HollisIntro, Route143_Text_HollisDefeat
	msgbox Route143_Text_HollisPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HollisIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route143_Text_HollisDefeat:
	.string "I'm still not lost.$"

Route143_Text_HollisPostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route143_EventScript_Maude::
	trainerbattle_single TRAINER_MAUDE, Route143_Text_MaudeIntro, Route143_Text_MaudeDefeat
	msgbox Route143_Text_MaudePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_MaudeIntro:
	.string "Don't hold back. I won't.$"

Route143_Text_MaudeDefeat:
	.string "You didn't waste my time.$"

Route143_Text_MaudePostBattle:
	.string "There's more of us further along.$"

Route143_EventScript_Mira::
	trainerbattle_single TRAINER_MIRA, Route143_Text_MiraIntro, Route143_Text_MiraDefeat
	msgbox Route143_Text_MiraPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_MiraIntro:
	.string "I came out here for a real match.$"

Route143_Text_MiraDefeat:
	.string "Strong. Genuinely strong.$"

Route143_Text_MiraPostBattle:
	.string "Rest before the next stretch.$"

Route143_EventScript_Nadia::
	trainerbattle_single TRAINER_NADIA, Route143_Text_NadiaIntro, Route143_Text_NadiaDefeat
	msgbox Route143_Text_NadiaPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_NadiaIntro:
	.string "Let's not waste each other's time.$"

Route143_Text_NadiaDefeat:
	.string "I'll take that loss.$"

Route143_Text_NadiaPostBattle:
	.string "Good luck out there.$"

Route143_EventScript_Horace::
	trainerbattle_single TRAINER_HORACE, Route143_Text_HoraceIntro, Route143_Text_HoraceDefeat
	msgbox Route143_Text_HoracePostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HoraceIntro:
	.string "You travel light. So do I.$"

Route143_Text_HoraceDefeat:
	.string "I'll break camp early.$"

Route143_Text_HoracePostBattle:
	.string "I'll be training when you come\nback.$"

Route143_EventScript_Hugo::
	trainerbattle_single TRAINER_HUGO, Route143_Text_HugoIntro, Route143_Text_HugoDefeat
	msgbox Route143_Text_HugoPostBattle, MSGBOX_AUTOCLOSE
	end

Route143_Text_HugoIntro:
	.string "One battle, then I'm moving on.$"

Route143_Text_HugoDefeat:
	.string "That's me humbled.$"

Route143_Text_HugoPostBattle:
	.string "Safe travels.$"

