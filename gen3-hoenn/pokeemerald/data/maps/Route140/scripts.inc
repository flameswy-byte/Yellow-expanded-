Route140_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route140_EventScript_Iris::
	trainerbattle_single TRAINER_IRIS, Route140_Text_IrisIntro, Route140_Text_IrisDefeat
	msgbox Route140_Text_IrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_IrisIntro:
	.string "The weather held. Let's use it.$"

Route140_Text_IrisDefeat:
	.string "How nice. And how losing.$"

Route140_Text_IrisPostBattle:
	.string "Good luck out there.$"

Route140_EventScript_Fenwick::
	trainerbattle_single TRAINER_FENWICK, Route140_Text_FenwickIntro, Route140_Text_FenwickDefeat
	msgbox Route140_Text_FenwickPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_FenwickIntro:
	.string "You look tough. I'm tougher.$"

Route140_Text_FenwickDefeat:
	.string "I'll train more.$"

Route140_Text_FenwickPostBattle:
	.string "I'll remember you!$"

Route140_EventScript_Ferris::
	trainerbattle_single TRAINER_FERRIS, Route140_Text_FerrisIntro, Route140_Text_FerrisDefeat
	msgbox Route140_Text_FerrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_FerrisIntro:
	.string "One battle! Just one!$"

Route140_Text_FerrisDefeat:
	.string "Next time! Next time!$"

Route140_Text_FerrisPostBattle:
	.string "Come back when I'm stronger!$"

Route140_EventScript_Isolde::
	trainerbattle_single TRAINER_ISOLDE, Route140_Text_IsoldeIntro, Route140_Text_IsoldeDefeat
	msgbox Route140_Text_IsoldePostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_IsoldeIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route140_Text_IsoldeDefeat:
	.string "Out of my depth.$"

Route140_Text_IsoldePostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route140_EventScript_Jemma::
	trainerbattle_single TRAINER_JEMMA, Route140_Text_JemmaIntro, Route140_Text_JemmaDefeat
	msgbox Route140_Text_JemmaPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JemmaIntro:
	.string "Don't hold back. I won't.$"

Route140_Text_JemmaDefeat:
	.string "You didn't waste my time.$"

Route140_Text_JemmaPostBattle:
	.string "There's more of us further along.$"

Route140_EventScript_Josie::
	trainerbattle_single TRAINER_JOSIE, Route140_Text_JosieIntro, Route140_Text_JosieDefeat
	msgbox Route140_Text_JosiePostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JosieIntro:
	.string "I came out here for a real match.$"

Route140_Text_JosieDefeat:
	.string "Strong. Genuinely strong.$"

Route140_Text_JosiePostBattle:
	.string "Rest before the next stretch.$"

Route140_EventScript_Juno::
	trainerbattle_single TRAINER_JUNO, Route140_Text_JunoIntro, Route140_Text_JunoDefeat
	msgbox Route140_Text_JunoPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_JunoIntro:
	.string "Let's not waste each other's time.$"

Route140_Text_JunoDefeat:
	.string "I'll take that loss.$"

Route140_Text_JunoPostBattle:
	.string "Good luck out there.$"

