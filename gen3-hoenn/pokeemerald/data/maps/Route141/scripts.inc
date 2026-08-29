Route141_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route141_EventScript_Leona::
	trainerbattle_single TRAINER_LEONA, Route141_Text_LeonaIntro, Route141_Text_LeonaDefeat
	msgbox Route141_Text_LeonaPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_LeonaIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route141_Text_LeonaDefeat:
	.string "I underestimated you.$"

Route141_Text_LeonaPostBattle:
	.string "I'll be training when you come\nback.$"

Route141_EventScript_Fenwick::
	trainerbattle_single TRAINER_FENWICK, Route141_Text_FenwickIntro, Route141_Text_FenwickDefeat
	msgbox Route141_Text_FenwickPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FenwickIntro:
	.string "Cast off! Let's battle.$"

Route141_Text_FenwickDefeat:
	.string "Hah! Hooked myself.$"

Route141_Text_FenwickPostBattle:
	.string "Tight lines, TRAINER.$"

Route141_EventScript_Ferris::
	trainerbattle_single TRAINER_FERRIS, Route141_Text_FerrisIntro, Route141_Text_FerrisDefeat
	msgbox Route141_Text_FerrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FerrisIntro:
	.string "Quiet! ...Ah, you've scared them\noff.\pYou owe me a battle.$"

Route141_Text_FerrisDefeat:
	.string "Reeled in and thrown back.$"

Route141_Text_FerrisPostBattle:
	.string "Best water's round the bend. Try\nit.$"

Route141_EventScript_Finlay::
	trainerbattle_single TRAINER_FINLAY, Route141_Text_FinlayIntro, Route141_Text_FinlayDefeat
	msgbox Route141_Text_FinlayPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FinlayIntro:
	.string "Been here since dawn. Nothing\nbiting.\pYou'll do.$"

Route141_Text_FinlayDefeat:
	.string "You're the one that got away.$"

Route141_Text_FinlayPostBattle:
	.string "Bring a ROD next time and I'll show\nyou a spot.$"

