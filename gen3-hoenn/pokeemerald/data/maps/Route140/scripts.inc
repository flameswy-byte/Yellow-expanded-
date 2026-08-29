Route140_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route140_EventScript_Jemma::
	trainerbattle_single TRAINER_JEMMA, Route140_Text_JemmaIntro, Route140_Text_JemmaDefeat
	msgbox Route140_Text_JemmaPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JemmaIntro:
	.string "The weather held. Let's use it.$"

Route140_Text_JemmaDefeat:
	.string "How nice. And how losing.$"

Route140_Text_JemmaPostBattle:
	.string "Good luck out there.$"

Route140_EventScript_Enzo::
	trainerbattle_single TRAINER_ENZO, Route140_Text_EnzoIntro, Route140_Text_EnzoDefeat
	msgbox Route140_Text_EnzoPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_EnzoIntro:
	.string "You look tough. I'm tougher.$"

Route140_Text_EnzoDefeat:
	.string "I'll train more.$"

Route140_Text_EnzoPostBattle:
	.string "I'll remember you!$"

Route140_EventScript_Evans::
	trainerbattle_single TRAINER_EVANS, Route140_Text_EvansIntro, Route140_Text_EvansDefeat
	msgbox Route140_Text_EvansPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_EvansIntro:
	.string "One battle! Just one!$"

Route140_Text_EvansDefeat:
	.string "Next time! Next time!$"

Route140_Text_EvansPostBattle:
	.string "Come back when I'm stronger!$"

Route140_EventScript_Josie::
	trainerbattle_single TRAINER_JOSIE, Route140_Text_JosieIntro, Route140_Text_JosieDefeat
	msgbox Route140_Text_JosiePostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JosieIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route140_Text_JosieDefeat:
	.string "Out of my depth.$"

Route140_Text_JosiePostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route140_EventScript_Juno::
	trainerbattle_single TRAINER_JUNO, Route140_Text_JunoIntro, Route140_Text_JunoDefeat
	msgbox Route140_Text_JunoPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JunoIntro:
	.string "Don't hold back. I won't.$"

Route140_Text_JunoDefeat:
	.string "You didn't waste my time.$"

Route140_Text_JunoPostBattle:
	.string "There's more of us further along.$"

Route140_EventScript_Kendra::
	trainerbattle_single TRAINER_KENDRA, Route140_Text_KendraIntro, Route140_Text_KendraDefeat
	msgbox Route140_Text_KendraPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_KendraIntro:
	.string "I came out here for a real match.$"

Route140_Text_KendraDefeat:
	.string "Strong. Genuinely strong.$"

Route140_Text_KendraPostBattle:
	.string "Rest before the next stretch.$"

Route140_EventScript_Lacey::
	trainerbattle_single TRAINER_LACEY, Route140_Text_LaceyIntro, Route140_Text_LaceyDefeat
	msgbox Route140_Text_LaceyPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_LaceyIntro:
	.string "Let's not waste each other's time.$"

Route140_Text_LaceyDefeat:
	.string "I'll take that loss.$"

Route140_Text_LaceyPostBattle:
	.string "Good luck out there.$"

