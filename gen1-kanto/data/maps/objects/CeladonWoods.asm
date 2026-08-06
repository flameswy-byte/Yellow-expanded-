	object_const_def
	const_export CELADONWOODS_ETHER
	const_export CELADONWOODS_NUGGET

CeladonWoods_Object:
	db $f ; border block

	def_warp_events

	def_bg_events

	def_object_events
	object_event 18, 10, SPRITE_POKE_BALL, STAY, NONE, TEXT_CELADONWOODS_ETHER, ETHER
	object_event 34, 36, SPRITE_POKE_BALL, STAY, NONE, TEXT_CELADONWOODS_NUGGET, NUGGET

	def_warps_to CELADON_WOODS
