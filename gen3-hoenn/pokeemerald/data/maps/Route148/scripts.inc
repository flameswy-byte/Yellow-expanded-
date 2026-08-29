Route148_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route148_EventScript_Renata::
	trainerbattle_single TRAINER_RENATA, Route148_Text_RenataIntro, Route148_Text_RenataDefeat
	msgbox Route148_Text_RenataPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RenataIntro:
	.string "Lovely spot for lunch.\pAnd a battle.$"

Route148_Text_RenataDefeat:
	.string "Well, that's the afternoon gone.$"

Route148_Text_RenataPostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Otto::
	trainerbattle_single TRAINER_OTTO, Route148_Text_OttoIntro, Route148_Text_OttoDefeat
	msgbox Route148_Text_OttoPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_OttoIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route148_Text_OttoDefeat:
	.string "Yesterday me would have lost worse.$"

Route148_Text_OttoPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route148_EventScript_Percy::
	trainerbattle_single TRAINER_PERCY, Route148_Text_PercyIntro, Route148_Text_PercyDefeat
	msgbox Route148_Text_PercyPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_PercyIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route148_Text_PercyDefeat:
	.string "Aww.$"

Route148_Text_PercyPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route148_EventScript_Porter::
	trainerbattle_single TRAINER_PORTER, Route148_Text_PorterIntro, Route148_Text_PorterDefeat
	msgbox Route148_Text_PorterPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_PorterIntro:
	.string "I walked all this way for a battle.$"

Route148_Text_PorterDefeat:
	.string "You're really strong!$"

Route148_Text_PorterPostBattle:
	.string "Do you know the way out? ...Me\nneither.$"

Route148_EventScript_Rosalind::
	trainerbattle_single TRAINER_ROSALIND, Route148_Text_RosalindIntro, Route148_Text_RosalindDefeat
	msgbox Route148_Text_RosalindPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RosalindIntro:
	.string "Show me the team that got you this\nfar.$"

Route148_Text_RosalindDefeat:
	.string "Good. Very good.$"

Route148_Text_RosalindPostBattle:
	.string "I'll be training when you come\nback.$"

Route148_EventScript_Ruby::
	trainerbattle_single TRAINER_RUBY, Route148_Text_RubyIntro, Route148_Text_RubyDefeat
	msgbox Route148_Text_RubyPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RubyIntro:
	.string "Ready when you are.$"

Route148_Text_RubyDefeat:
	.string "You've earned the ROUTE.$"

Route148_Text_RubyPostBattle:
	.string "Safe travels.$"

Route148_EventScript_Sable::
	trainerbattle_single TRAINER_SABLE, Route148_Text_SableIntro, Route148_Text_SableDefeat
	msgbox Route148_Text_SablePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SableIntro:
	.string "You have the walk of someone worth\nbattling.$"

Route148_Text_SableDefeat:
	.string "That was a real match.$"

Route148_Text_SablePostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Quinn::
	trainerbattle_single TRAINER_QUINN, Route148_Text_QuinnIntro, Route148_Text_QuinnDefeat
	msgbox Route148_Text_QuinnPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_QuinnIntro:
	.string "A challenger! At last.$"

Route148_Text_QuinnDefeat:
	.string "The ROUTE is yours.$"

Route148_Text_QuinnPostBattle:
	.string "There's more of us further along.$"

Route148_EventScript_Rafe::
	trainerbattle_single TRAINER_RAFE, Route148_Text_RafeIntro, Route148_Text_RafeDefeat
	msgbox Route148_Text_RafePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RafeIntro:
	.string "I've been waiting for someone like\nyou.$"

Route148_Text_RafeDefeat:
	.string "Beaten.$"

Route148_Text_RafePostBattle:
	.string "Rest before the next stretch.$"

Route148_EventScript_Reeves::
	trainerbattle_single TRAINER_REEVES, Route148_Text_ReevesIntro, Route148_Text_ReevesDefeat
	msgbox Route148_Text_ReevesPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_ReevesIntro:
	.string "I sleep where the ROUTE ends.$"

Route148_Text_ReevesDefeat:
	.string "Well fought.$"

Route148_Text_ReevesPostBattle:
	.string "Good luck out there.$"

Route148_EventScript_Reggie::
	trainerbattle_single TRAINER_REGGIE, Route148_Text_ReggieIntro, Route148_Text_ReggieDefeat
	msgbox Route148_Text_ReggiePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_ReggieIntro:
	.string "You travel light. So do I.$"

Route148_Text_ReggieDefeat:
	.string "I'll break camp early.$"

Route148_Text_ReggiePostBattle:
	.string "I'll be training when you come\nback.$"

Route148_EventScript_Rhys::
	trainerbattle_single TRAINER_RHYS, Route148_Text_RhysIntro, Route148_Text_RhysDefeat
	msgbox Route148_Text_RhysPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RhysIntro:
	.string "One battle, then I'm moving on.$"

Route148_Text_RhysDefeat:
	.string "That's me humbled.$"

Route148_Text_RhysPostBattle:
	.string "Safe travels.$"

Route148_EventScript_Roscoe::
	trainerbattle_single TRAINER_ROSCOE, Route148_Text_RoscoeIntro, Route148_Text_RoscoeDefeat
	msgbox Route148_Text_RoscoePostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RoscoeIntro:
	.string "Not many come this far. Battle me.$"

Route148_Text_RoscoeDefeat:
	.string "You've come a long way indeed.$"

Route148_Text_RoscoePostBattle:
	.string "Keep heading on. It opens out.$"

Route148_EventScript_Rowan::
	trainerbattle_single TRAINER_ROWAN, Route148_Text_RowanIntro, Route148_Text_RowanDefeat
	msgbox Route148_Text_RowanPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RowanIntro:
	.string "A challenger! At last.$"

Route148_Text_RowanDefeat:
	.string "The ROUTE is yours.$"

Route148_Text_RowanPostBattle:
	.string "There's more of us further along.$"

Route148_EventScript_Rufus::
	trainerbattle_single TRAINER_RUFUS, Route148_Text_RufusIntro, Route148_Text_RufusDefeat
	msgbox Route148_Text_RufusPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_RufusIntro:
	.string "I've been waiting for someone like\nyou.$"

Route148_Text_RufusDefeat:
	.string "Beaten.$"

Route148_Text_RufusPostBattle:
	.string "Rest before the next stretch.$"

Route148_EventScript_Seamus::
	trainerbattle_single TRAINER_SEAMUS, Route148_Text_SeamusIntro, Route148_Text_SeamusDefeat
	msgbox Route148_Text_SeamusPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SeamusIntro:
	.string "Let's not waste each other's time.$"

Route148_Text_SeamusDefeat:
	.string "I'll take that loss.$"

Route148_Text_SeamusPostBattle:
	.string "Good luck out there.$"

Route148_EventScript_Seth::
	trainerbattle_single TRAINER_SETH, Route148_Text_SethIntro, Route148_Text_SethDefeat
	msgbox Route148_Text_SethPostBattle, MSGBOX_AUTOCLOSE
	end

Route148_Text_SethIntro:
	.string "Show me the team that got you this\nfar.$"

Route148_Text_SethDefeat:
	.string "Good. Very good.$"

Route148_Text_SethPostBattle:
	.string "I'll be training when you come\nback.$"

