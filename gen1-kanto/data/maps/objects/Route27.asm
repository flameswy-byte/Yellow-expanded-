	object_const_def
	const_export ROUTE27_POTION

Route27_Object:
	db $f ; border block

	def_warp_events

	def_bg_events

	def_object_events
	object_event 6, 4, SPRITE_POKE_BALL, STAY, NONE, TEXT_ROUTE27_POTION, POTION

	def_warps_to ROUTE_27
