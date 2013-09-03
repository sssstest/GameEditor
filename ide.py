#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import sys
import os
import CliClass

resourcePath="GameEditor/ideicons/"

class RoomViewInstance(QWidget):
	def __init__(self, image, res, parent, qTreeWidgetItem):
		QWidget.__init__(self, parent)
		self.image=image
		self.rotation=0
		if image:
			self.scaledWidth=self.image.width()
			self.scaledHeight=self.image.height()
			self.resize(self.scaledWidth+8,self.scaledHeight+8)
			self.containerWidth=self.scaledHeight+8
			self.containerHeight=self.image.height()+8
		else:
			self.resize(64,64)
			self.containerWidth=64
			self.containerHeight=64
			self.scaledWidth=64
			self.scaledHeight=64
		self.res=res
		self.selected=False
		self.qTreeWidgetItem=qTreeWidgetItem

		self.updateFromRes()

	def updateFromRes(self):
		x=self.res.getMember("x")
		y=self.res.getMember("y")
		scaleX=self.res.getMember("scaleX")
		scaleY=self.res.getMember("scaleY")
		self.rotation=self.res.getMember("rotation")
		self.move(x-4,y-4)

		transform=QTransform()
		transform.rotate(self.rotation)
		rect=self.contentsRect()
		mapRect=transform.mapRect(rect)
		self.resize(mapRect.width(),mapRect.height())

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		matrix=QMatrix()
		matrix.translate(self.width()/2, self.height()/2)
		matrix.rotate(self.rotation)
		matrix.translate(-self.scaledWidth/2, -self.scaledHeight/2)
		transform=QTransform(matrix)
		rect=self.contentsRect()
		mapRect=transform.mapRect(rect)
		painter.setTransform(transform)
		if self.image:
			painter.drawImage(QRect(0,0,self.scaledWidth,self.scaledHeight),self.image)
			self.containerWidth=self.scaledWidth+8
			self.containerHeight=self.scaledHeight+8
		else:
			painter.drawText(6,6,64,64,0,"no\nsprite")
			self.containerWidth=64
			self.containerHeight=64
		if self.selected:
			transform=QTransform()
			painter.setTransform(transform)
			painter.setPen(QColor(0))
			painter.setBrush(QColor(255,0,0))
			painter.drawRect(0,0,7,7)
			painter.drawRect(self.containerWidth-8,0,7,7)
			painter.drawRect(0,self.containerHeight-8,7,7)
			painter.drawRect(self.containerWidth-8,self.containerHeight-8,7,7)
			painter.setBrush(QColor(0,255,0))
			painter.drawEllipse(self.containerWidth-8,(self.containerHeight-8)/2,7,7)

	def setRotation(self, angle):
		self.rotation=angle

	def moveRes(self, qPoint):
		self.move(qPoint)
		self.res.setMember("x", qPoint.x()+4)
		self.res.setMember("y", qPoint.y()+4)

	def setScaleImageSize(self, width, height):
		self.scaledWidth=width
		self.scaledHeight=height
		self.resize(self.scaledWidth+8,self.scaledHeight+8)

	def getScaledWidth(self):
		return self.scaledWidth

	def getScaledHeight(self):
		return self.scaledHeight

class RoomView(QWidget):
	def __init__(self, parent, res, roomWindow):
		QWidget.__init__(self, parent)
		self.res=res
		self.roomWindow=roomWindow
		self.rubberBand=None
		self.resize(self.res.getMember("width"), self.res.getMember("height"))
		self.gridX=160
		self.gridY=160
		self.updateBrush()
		self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
		for c in xrange(self.roomWindow.tree.topLevelItemCount()):
			item=self.roomWindow.tree.topLevelItem(c)
			for c in xrange(item.childCount()):
				x=item.child(c)
				if x.res and type(x.res)==CliClass.GameRoomInstance:
					i=x.res
					imageLabel=None
					if i.getMember("object"):
						if i.getMember("object").getMember("sprite"):
							if len(i.getMember("object").getMember("sprite").subimages)>0:
								q=i.getMember("object").getMember("sprite").subimages[0].getQImage()
								imageLabel=RoomViewInstance(q,i,self,x)
					if not imageLabel:
						imageLabel=RoomViewInstance(None,i,self,x)
					imageLabel.updateFromRes()

	def updateBrush(self):
		x=0
		y=0
		height=self.gridY
		width=self.gridX
		i=QtGui.QImage(width,height,QtGui.QImage.Format_ARGB32)
		painter=QtGui.QPainter(i)
		painter.setBrush(QColor(0x1ea0e6))
		painter.drawRect(-1,-1,width,height)
		painter.setPen(QColor(0x13648f))
		painter.drawLine(width-1,0,width-1,height-1)
		painter.drawLine(0,height-1,width-1,height-1)
		painter.setPen(QColor(0x73c4ef))
		painter.drawLine(0,0,width,0)
		painter.drawLine(0,0,0,height)
		painter.end()
		self.brush=QBrush(i)
		x=0
		y=0
		height=self.gridY
		width=self.gridX
		i=QtGui.QImage(width,height,QtGui.QImage.Format_ARGB32)
		painter=QtGui.QPainter(i)
		cx0 = x + (width >> 1)
		cy0 = y + (height >> 1)
		cx1 = x + (width + 1 >> 1)
		cy1 = y + (height + 1 >> 1)
		painter.setBrush(QColor(0x1ea0e6))
		painter.drawRect(-1,-1,width+1,height+1)
		painter.setPen(QColor(0,0,50))
		painter.drawLine(x + 1,cy1,cx0,y + height - 1)
		painter.drawLine(cx1,y + height - 1,x + width - 1,cy1)
		painter.drawLine(x + width,cy0 - 1,cx1 + 1,y)
		painter.drawLine(cx0 - 1,y,x,cy0 - 1)
		painter.setPen(QColor(200,200,250))
		painter.drawLine(x + width - 1,cy0,cx1,y + 1)
		painter.drawLine(cx0,y + 1,x + 1,cy0)
		painter.drawLine(x,cy1 + 1,cx0 - 1,y + height)
		painter.drawLine(cx1 + 1,y + height,x + width,cy1 + 1)
		painter.end()
		self.isometricBrush=QBrush(i)

	def paintEvent(self, event):
		side = min(self.width(), self.height())
		painter = QtGui.QPainter(self)
		if self.res.getMember("isometric"):
			painter.setBrush(self.isometricBrush)
		else:
			painter.setBrush(self.brush)
		painter.setPen(Qt.NoPen)
		painter.drawRect(0,0,1000,1000)

	def mousePressEvent(self, event):
		self.origin = event.pos()
		self.moveSelection=False
		self.resizeSelection=False
		self.rotateSelection=False
		if app.keyboardModifiers() == Qt.ControlModifier:
			item=self.res.gameFile.GetResourceName(CliClass.GameFile.RtObject, self.roomWindow.activeItem)
			if item:
				inst=self.res.newInstance()
				inst.setMember("x",self.origin.x())
				inst.setMember("y",self.origin.y())
				inst.setMember("object",item)
				self.roomWindow.updateTree()
			return
		for c in reversed(self.children()):
			if type(c)==RoomViewInstance and c.geometry().contains(self.origin):
				if not c.selected:
					for chil in self.children():
						if app.keyboardModifiers() != Qt.ShiftModifier:
							chil.selected=False
							chil.update()
					c.selected=True
					c.update()
				point = self.origin-c.geometry().topLeft()
				if QRect(0,0,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(c.containerWidth-8,0,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(0,c.containerHeight-8,8,8).contains(point):
					CliClass.print_notice("resize unsupported")
				elif QRect(c.containerWidth-8,c.containerHeight-8,8,8).contains(point):
					self.resizeSelection=True
					return
				elif QRect(c.containerWidth-8,(c.containerHeight-8)/2,8,8).contains(point):
					self.rotateSelection=True
					self.origin=QPoint(c.x()+(c.width()/2),c.y()+(c.height()/2))
				self.moveSelection=True
				self.roomWindow.tree.setCurrentItem(c.qTreeWidgetItem)
				return
		self.rubberBand.setGeometry(QRect(self.origin, QSize()))
		self.rubberBand.show()

	def mouseMoveEvent(self, event):
		if self.rotateSelection:
			import math
			x=event.pos().x()-self.origin.x()
			y=event.pos().y()-self.origin.y()
			angle=math.atan2(y,x) * 180 / math.pi
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					angle=(angle+360)%360
					c.setRotation(angle)
					c.update()
			return
		if self.resizeSelection:
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.setScaleImageSize(c.scaledWidth+(event.pos().x()-self.origin.x()),c.scaledHeight+(event.pos().y()-self.origin.y()))
					c.update()
			self.origin=event.pos()
			return
		if self.moveSelection:
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.moveRes(c.pos()+(event.pos()-self.origin))
			self.origin=event.pos()
			return
		if self.rubberBand:
			self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

	def mouseReleaseEvent(self, event):
		if not self.moveSelection and not self.resizeSelection and not self.rotateSelection:
			self.rubberBand.hide()
			for c in self.children():
				if type(c)==RoomViewInstance and c.selected:
					c.selected=False
					c.update()
				if self.origin<event.pos():
					rect=QRect(self.origin,event.pos())
				else:
					rect=QRect(event.pos(),self.origin)
				if rect.intersects(c.geometry()):
					if type(c)==RoomViewInstance:
						c.selected=True
						c.update()

class PropertiesTable(QTableWidget):
	def __init__(self, parent):
		QTableWidget.__init__(self, parent)
		self.res=None
		self.subwindow=None

	def dataChanged(self, topLeft, bottomRight):
		if self.updatedTable:
			if topLeft != bottomRight:
				CliClass.print_notice("multple items change unsupported")
			if topLeft.column() != 1:
				return
			member=str(self.item(topLeft.row(),0).text())
			text=str(self.item(topLeft.row(),topLeft.column()).text())
			checked=self.item(topLeft.row(),topLeft.column()).checkState()
			if self.res:
				value=self.res.getMember(member)
				if type(value)==bool:
					if value!=bool(checked):
						self.res.setMember(member,bool(checked))
						self.subwindow.updatePropertiesTable()
				elif type(value)==int:
					if value!=int(text):
						self.res.setMember(member,int(text))
						self.subwindow.updatePropertiesTable()
				elif type(value)==float:
					if value!=float(text):
						self.res.setMember(member,float(text))
						self.subwindow.updatePropertiesTable()
				else:
					if value!=text:
						self.res.setMember(member,text)
						self.subwindow.updatePropertiesTable()
						if member=="name":
							self.mainwindow.updateHierarchyTree()

class LexerGame(QsciLexerCPP):
	def __init__(self, mainwindow):
		QsciLexerCPP.__init__(self)
		self.mainwindow=mainwindow

	def keywords(self, set):
		if set == 1:
			keywords = "@ev_create @ev_destroy @ev_alarm @ev_step @ev_collision @ev_keyboard @ev_mouse @ev_other @ev_draw @ev_press @ev_release @ev_async "
			#keywords += "@sprite @sound @background @path @script @shader @font @timeline @object @room @trigger "
			keywords += "@action @code @comment "
			keywords += "ANSI_CHARSET ARABIC_CHARSET BALTIC_CHARSET CHINESEBIG5_CHARSET DEFAULT_CHARSET EASTEUROPE_CHARSET GB2312_CHARSET GREEK_CHARSET HANGEUL_CHARSET HEBREW_CHARSET JOHAB_CHARSET MAC_CHARSET OEM_CHARSET RUSSIAN_CHARSET SHIFTJIS_CHARSET SYMBOL_CHARSET THAI_CHARSET TURKISH_CHARSET VIETNAMESE_CHARSET all asset_background asset_font asset_object asset_path asset_room asset_script asset_sound asset_sprite asset_timeline asset_unknown audio_falloff_exponent_distance audio_falloff_exponent_distance_clamped audio_falloff_inverse_distance audio_falloff_inverse_distance_clamped audio_falloff_linear_distance audio_falloff_linear_distance_clamped audio_falloff_none audio_new_system audio_old_system bm_add bm_dest_alpha bm_dest_color bm_inv_dest_alpha bm_inv_dest_color bm_inv_src_alpha bm_inv_src_color bm_max bm_normal bm_one bm_src_alpha bm_src_alpha_sat bm_src_color bm_subtract bm_zero browser_chrome browser_firefox browser_ie browser_not_a_browser browser_opera browser_safari browser_safari_mobile browser_unknown browser_windows_store buffer_bool buffer_f16 buffer_f32 buffer_f64 buffer_fast buffer_fixed buffer_generalerror buffer_grow buffer_invalidtype buffer_outofbounds buffer_outofspace buffer_s16 buffer_s32 buffer_s8 buffer_seek_end buffer_seek_relative buffer_seek_start buffer_string buffer_u16 buffer_u32 buffer_u8 buffer_vbuffer buffer_wrap button_type c_aqua c_black c_blue c_dkgray c_fuchsia c_gray c_green c_lime c_ltgray c_maroon c_navy c_olive c_orange c_purple c_red c_silver c_teal c_white c_yellow cr_appstart cr_arrow cr_arrrow cr_beam cr_cross cr_default cr_drag cr_handpoint cr_help cr_hourglass cr_hsplit cr_multidrag cr_no cr_nodrop cr_none cr_size_all cr_size_nesw cr_size_ns cr_size_nwse cr_size_we cr_sqlwait cr_uparrow cr_vsplit device_emulator device_ios_ipad device_ios_ipad_retina device_ios_iphone device_ios_iphone5 device_ios_iphone_retina device_ios_unknown device_tablet display_landscape display_landscape_flipped display_portrait display_portrait_flipped dll_cdecl dll_stdcall ef_cloud ef_ellipse ef_explosion ef_firework ef_flare ef_rain ef_ring ef_smoke ef_smokeup ef_snow ef_spark ef_star ev_alarm ev_animation_end ev_boundary ev_close_button ev_collision ev_create ev_destroy ev_draw ev_end_of_path ev_game_end ev_game_start ev_global_left_button ev_global_left_press ev_global_left_release ev_global_middle_button ev_global_middle_press ev_global_middle_release ev_global_press ev_global_release ev_global_right_button ev_global_right_press ev_global_right_release ev_gui ev_joystick1_button1 ev_joystick1_button2 ev_joystick1_button3 ev_joystick1_button4 ev_joystick1_button5 ev_joystick1_button6 ev_joystick1_button7 ev_joystick1_button8 ev_joystick1_down ev_joystick1_left ev_joystick1_right ev_joystick1_up ev_joystick2_button1 ev_joystick2_button2 ev_joystick2_button3 ev_joystick2_button4 ev_joystick2_button5 ev_joystick2_button6 ev_joystick2_button7 ev_joystick2_button8 ev_joystick2_down ev_joystick2_left ev_joystick2_right ev_joystick2_up ev_keyboard ev_keypress ev_keyrelease ev_left_button ev_left_press ev_left_release ev_middle_button ev_middle_press ev_middle_release ev_mouse ev_mouse_enter ev_mouse_leave ev_mouse_wheel_down ev_mouse_wheel_up ev_no_button ev_no_more_health ev_no_more_lives ev_other ev_outside ev_right_button ev_right_press ev_right_release ev_room_end ev_room_start ev_step ev_step_begin ev_step_end ev_step_normal ev_trigger ev_user0 ev_user1 ev_user10 ev_user11 ev_user12 ev_user13 ev_user14 ev_user15 ev_user2 ev_user3 ev_user4 ev_user5 ev_user6 ev_user7 ev_user8 ev_user9 fa_archive fa_bottom fa_center fa_directory fa_hidden fa_left fa_middle fa_readonly fa_right fa_sysfile fa_top fa_volumeid false global gp_axislh gp_axislv gp_axisrh gp_axisrv gp_face1 gp_face2 gp_face3 gp_face4 gp_padd gp_padl gp_padr gp_padu gp_select gp_shoulderl gp_shoulderlb gp_shoulderr gp_shoulderrb gp_start gp_stickl gp_stickr input_type leaderboard_type_number leaderboard_type_time_mins_secs local mb_any mb_left mb_middle mb_none mb_right network_socket_bluetooth network_socket_tcp network_socket_udp network_type_connect network_type_data network_type_disconnect noone of_challenge_lose of_challenge_tie of_challenge_win os_android os_ios os_linux os_macosx os_psp os_symbian os_unknown os_win32 os_windows os_winphone other phy_debug_render_aabb phy_debug_render_collision_pairs phy_debug_render_coms phy_debug_render_core_shapes phy_debug_render_joints phy_debug_render_obb phy_debug_render_shapes phy_joint_anchor_1_x phy_joint_anchor_1_y phy_joint_anchor_1_y phy_joint_anchor_2_x phy_joint_angle phy_joint_damping_ratio phy_joint_frequency phy_joint_length_1 phy_joint_length_2 phy_joint_max_motor_force phy_joint_max_motor_torque phy_joint_motor_force phy_joint_motor_speed phy_joint_motor_torque phy_joint_reaction_force_x phy_joint_reaction_force_y phy_joint_reaction_torque phy_joint_speed phy_joint_translation pi pr_linelist pr_linestrip pr_pointlist pr_trianglefan pr_trianglelist pr_trianglestrip ps_change_all ps_change_motion ps_change_shape ps_deflect_horizontal ps_deflect_vertical ps_distr_gaussian ps_distr_invgaussian ps_distr_linear ps_force_constant ps_force_linear ps_force_quadratic ps_shape_diamond ps_shape_ellipse ps_shape_line ps_shape_rectangle pt_shape_circle pt_shape_cloud pt_shape_disk pt_shape_explosion pt_shape_flare pt_shape_line pt_shape_pixel pt_shape_ring pt_shape_smoke pt_shape_snow pt_shape_spark pt_shape_sphere pt_shape_square pt_shape_star se_chorus se_compressor se_echo se_equalizer se_flanger se_gargle se_none se_reverb self text_type true ty_real ty_string vk_add vk_alt vk_anykey vk_backspace vk_control vk_decimal vk_delete vk_divide vk_down vk_end vk_enter vk_escape vk_f1 vk_f10 vk_f11 vk_f12 vk_f2 vk_f3 vk_f4 vk_f5 vk_f6 vk_f7 vk_f8 vk_f9 vk_home vk_insert vk_lalt vk_lcontrol vk_left vk_lshift vk_multiply vk_nokey vk_numpad0 vk_numpad1 vk_numpad2 vk_numpad3 vk_numpad4 vk_numpad5 vk_numpad6 vk_numpad7 vk_numpad8 vk_numpad9 vk_pagedown vk_pageup vk_pause vk_printscreen vk_ralt vk_rcontrol vk_return vk_right vk_rshift vk_shift vk_space vk_subtract vk_tab"
			keywords += "abs achievement_available achievement_login achievement_logout achievement_post achievement_post_score achievement_show_achievements achievement_show_leaderboards action_another_room action_bounce action_change_object action_color action_create_object action_create_object_motion action_create_object_random action_current_room action_draw_arrow action_draw_background action_draw_ellipse action_draw_ellipse_gradient action_draw_gradient_hor action_draw_gradient_vert action_draw_health action_draw_life action_draw_life_images action_draw_line action_draw_rectangle action_draw_score action_draw_sprite action_draw_text action_draw_text_transformed action_draw_variable action_effect action_end_game action_end_sound action_execute_script action_font action_fullscreen action_highscore_clear action_highscore_show action_if action_if_aligned action_if_collision action_if_dice action_if_empty action_if_health action_if_life action_if_mouse action_if_next_room action_if_number action_if_object action_if_previous_room action_if_question action_if_score action_if_sound action_if_variable action_inherited action_kill_object action_kill_position action_linear_step action_load_game action_message action_move action_move_contact action_move_point action_move_random action_move_start action_move_to action_next_room action_partemit_burst action_partemit_create action_partemit_destroy action_partemit_stream action_partsyst_clear action_partsyst_create action_partsyst_destroy action_parttype_color action_parttype_create action_parttype_gravity action_parttype_life action_parttype_secondary action_parttype_speed action_path action_path_end action_path_position action_path_speed action_potential_step action_previous_room action_replace_background action_replace_sound action_replace_sprite action_restart_game action_reverse_xdir action_reverse_ydir action_save_game action_set_alarm action_set_caption action_set_cursor action_set_friction action_set_gravity action_set_health action_set_hspeed action_set_life action_set_motion action_set_score action_set_timeline action_set_timeline_position action_set_timeline_speed action_set_vspeed action_show_info action_show_video action_sleep action_snap action_snapshot action_sound action_splash_image action_splash_settings action_splash_text action_splash_video action_splash_web action_sprite_color action_sprite_set action_sprite_transform action_timeline_pause action_timeline_set action_timeline_start action_timeline_stop action_webpage action_wrap ads_disable ads_enable ads_engagement_active ads_engagement_available ads_engagement_launch ads_get_display_height ads_get_display_width ads_interstitial_available ads_interstitial_display ads_move ads_setup analytics_event analytics_event_ext ansi_char arccos arcsin arctan arctan2 asset_get_index asset_get_type audio_channel_num audio_emitter_create audio_emitter_exists audio_emitter_falloff audio_emitter_free audio_emitter_gain audio_emitter_pitch audio_emitter_position audio_emitter_velocity audio_exists audio_falloff_set_model audio_get_type audio_is_playing audio_listener_orientation audio_listener_position audio_listener_velocity audio_master_gain audio_music_gain audio_pause_all audio_pause_music audio_pause_sound audio_play_music audio_play_sound audio_play_sound_at audio_play_sound_on audio_resume_all audio_resume_music audio_resume_sound audio_sound_gain audio_sound_length audio_sound_pitch audio_stop_all audio_stop_music audio_stop_sound audio_system background_add background_assign background_create_color background_create_from_screen background_create_from_surface background_create_gradient background_delete background_duplicate background_exists background_get_height background_get_name background_get_texture background_get_width background_replace background_save background_set_alpha_from_background base64_decode base64_encode buffer_base64_decode buffer_base64_decode_ext buffer_base64_encode buffer_copy buffer_create buffer_delete buffer_fill buffer_get_size buffer_get_surface buffer_load buffer_load_ext buffer_md5 buffer_peek buffer_poke buffer_read buffer_resize buffer_save buffer_save_ext buffer_seek buffer_set_surface buffer_sha1 buffer_sizeof buffer_tell buffer_write ceil choose chr clamp clickable_add clickable_add_ext clickable_change clickable_change_ext clickable_delete clickable_exists clipboard_get_text clipboard_has_text clipboard_set_text cloud_file_save cloud_string_save cloud_synchronise collision_circle collision_ellipse collision_line collision_point collision_rectangle color_get_blue color_get_green color_get_hue color_get_red color_get_saturation color_get_value cos d3d_draw_block d3d_draw_cone d3d_draw_cylinder d3d_draw_ellipsoid d3d_draw_floor d3d_draw_wall d3d_end d3d_light_define_ambient d3d_light_define_direction d3d_light_define_point d3d_light_enable d3d_model_block d3d_model_clear d3d_model_cone d3d_model_create d3d_model_cylinder d3d_model_destroy d3d_model_draw d3d_model_ellipsoid d3d_model_floor d3d_model_load d3d_model_primitive_begin d3d_model_primitive_end d3d_model_save d3d_model_vertex d3d_model_vertex_color d3d_model_vertex_normal d3d_model_vertex_normal_color d3d_model_vertex_normal_texture d3d_model_vertex_normal_texture_color d3d_model_vertex_texture d3d_model_vertex_texture_color d3d_model_wall d3d_primitive_begin d3d_primitive_begin_texture d3d_primitive_end d3d_set_culling d3d_set_depth d3d_set_fog d3d_set_hidden d3d_set_lighting d3d_set_perspective d3d_set_projection d3d_set_projection_ext d3d_set_projection_ortho d3d_set_projection_perspective d3d_set_shading d3d_set_zwriteenable d3d_start d3d_transform_add_rotation_axis d3d_transform_add_rotation_x d3d_transform_add_rotation_y d3d_transform_add_rotation_z d3d_transform_add_scaling d3d_transform_add_translation d3d_transform_set_identity d3d_transform_set_rotation_axis d3d_transform_set_rotation_x d3d_transform_set_rotation_y d3d_transform_set_rotation_z d3d_transform_set_scaling d3d_transform_set_translation d3d_transform_stack_clear d3d_transform_stack_discard d3d_transform_stack_empty d3d_transform_stack_pop d3d_transform_stack_push d3d_transform_stack_top d3d_vertex d3d_vertex_color d3d_vertex_normal d3d_vertex_normal_color d3d_vertex_normal_texture d3d_vertex_normal_texture_color d3d_vertex_texture d3d_vertex_texture_color date_compare_date date_compare_datetime date_compare_time date_create_date date_create_datetime date_create_time date_current_datetime date_date_of date_date_string date_datetime_string date_day_span date_days_in_month date_days_in_year date_get_day date_get_day_of_year date_get_hour date_get_hour_of_year date_get_minute date_get_minute_of_year date_get_month date_get_second date_get_second_of_year date_get_week date_get_weekday date_get_year date_hour_span date_inc_day date_inc_hour date_inc_minute date_inc_month date_inc_second date_inc_week date_inc_year date_is_today date_leap_year date_minute_span date_month_span date_second_span date_time_of date_time_string date_valid_date date_valid_datetime date_valid_time date_week_span date_year_span degtorad device_get_tilt_x device_get_tilt_y device_get_tilt_z device_ios_get_image device_ios_get_imagename device_is_keypad_open device_mouse_check_button device_mouse_check_button_pressed device_mouse_check_button_released device_mouse_dbclick_enable device_mouse_raw_x device_mouse_raw_y device_mouse_x device_mouse_y directory_create directory_exists display_get_dpi_x display_get_dpi_y display_get_gui_height display_get_gui_width display_get_height display_get_orientation display_get_width display_mouse_get_x display_mouse_get_y display_mouse_set display_reset display_set_gui_size distance_to_object distance_to_point dot_product dot_product_3d dot_product_3d_normalised dot_product_normalised draw_arrow draw_background draw_background_ext draw_background_general draw_background_part draw_background_part_ext draw_background_stretched draw_background_stretched_ext draw_background_tiled draw_background_tiled_ext draw_button draw_circle draw_circle_color draw_clear draw_clear_alpha draw_ellipse draw_ellipse_color draw_enable_alphablend draw_enable_drawevent draw_get_alpha draw_get_alpha_test draw_get_alpha_test_ref_value draw_get_color draw_getpixel draw_healthbar draw_highscore draw_line draw_line_color draw_line_width draw_line_width_color draw_path draw_point draw_point_color draw_primitive_begin draw_primitive_begin_texture draw_primitive_end draw_rectangle draw_rectangle_color draw_roundrect draw_roundrect_color draw_self draw_set_alpha draw_set_alpha_test draw_set_alpha_test_ref_value draw_set_blend_mode draw_set_blend_mode_ext draw_set_circle_precision draw_set_color draw_set_color_write_enable draw_set_font draw_set_halign draw_set_valign draw_sprite draw_sprite_ext draw_sprite_general draw_sprite_part draw_sprite_part_ext draw_sprite_pos draw_sprite_stretched draw_sprite_stretched_ext draw_sprite_tiled draw_sprite_tiled_ext draw_surface draw_surface_ext draw_surface_general draw_surface_part draw_surface_part_ext draw_surface_stretched draw_surface_stretched_ext draw_surface_tiled draw_surface_tiled_ext draw_text draw_text_color draw_text_ext draw_text_ext_color draw_text_ext_transformed draw_text_ext_transformed_color draw_text_transformed draw_text_transformed_color draw_texture_flush draw_triangle draw_triangle_color draw_vertex draw_vertex_color draw_vertex_texture draw_vertex_texture_color ds_grid_add ds_grid_add_disk ds_grid_add_grid_region ds_grid_add_region ds_grid_clear ds_grid_copy ds_grid_create ds_grid_destroy ds_grid_get ds_grid_get_disk_max ds_grid_get_disk_mean ds_grid_get_disk_min ds_grid_get_disk_sum ds_grid_get_max ds_grid_get_mean ds_grid_get_min ds_grid_get_sum ds_grid_height ds_grid_multiply ds_grid_multiply_disk ds_grid_multiply_grid_region ds_grid_multiply_region ds_grid_read ds_grid_resize ds_grid_set ds_grid_set_disk ds_grid_set_grid_region ds_grid_set_region ds_grid_shuffle ds_grid_value_disk_exists ds_grid_value_disk_x ds_grid_value_disk_y ds_grid_value_exists ds_grid_value_x ds_grid_value_y ds_grid_width ds_grid_write ds_list_add ds_list_clear ds_list_copy ds_list_create ds_list_delete ds_list_destroy ds_list_empty ds_list_find_index ds_list_find_value ds_list_insert ds_list_read ds_list_replace ds_list_shuffle ds_list_size ds_list_sort ds_list_write ds_map_add ds_map_clear ds_map_copy ds_map_create ds_map_delete ds_map_destroy ds_map_empty ds_map_exists ds_map_find_first ds_map_find_last ds_map_find_next ds_map_find_previous ds_map_find_value ds_map_read ds_map_replace ds_map_size ds_map_write ds_priority_add ds_priority_change_priority ds_priority_clear ds_priority_copy ds_priority_create ds_priority_delete_max ds_priority_delete_min ds_priority_delete_value ds_priority_destroy ds_priority_empty ds_priority_find_max ds_priority_find_min ds_priority_find_priority ds_priority_read ds_priority_size ds_priority_write ds_queue_clear ds_queue_copy ds_queue_create ds_queue_dequeue ds_queue_destroy ds_queue_empty ds_queue_enqueue ds_queue_head ds_queue_read ds_queue_size ds_queue_tail ds_queue_write ds_set_precision ds_stack_clear ds_stack_copy ds_stack_create ds_stack_destroy ds_stack_empty ds_stack_pop ds_stack_push ds_stack_read ds_stack_size ds_stack_top ds_stack_write effect_clear effect_create_above effect_create_below environment_get_variable event_inherited event_perform event_perform_object event_user exp external_call external_define external_free facebook_accesstoken facebook_dialog facebook_graph_request facebook_init facebook_launch_offerwall facebook_login facebook_logout facebook_post_message facebook_send_invite facebook_status facebook_user_id file_attributes file_bin_close file_bin_open file_bin_position file_bin_read_byte file_bin_rewrite file_bin_seek file_bin_size file_bin_write_byte file_copy file_delete file_exists file_find_close file_find_first file_find_next file_rename file_text_close file_text_eof file_text_eoln file_text_open_append file_text_open_read file_text_open_write file_text_read_real file_text_read_string file_text_readln file_text_write_real file_text_write_string file_text_writeln filename_change_ext filename_dir filename_drive filename_ext filename_name filename_path floor font_add font_add_sprite font_add_sprite_ext font_delete font_exists font_get_bold font_get_first font_get_fontname font_get_italic font_get_last font_get_name font_get_size font_replace font_replace_sprite font_replace_sprite_ext font_set_cache_size frac game_end game_restart gamepad_axis_count gamepad_axis_value gamepad_button_check gamepad_button_check_pressed gamepad_button_check_released gamepad_button_count gamepad_button_value gamepad_get_axis_deadzone gamepad_get_button_threshold gamepad_get_description gamepad_get_device_count gamepad_is_connected gamepad_is_supported gamepad_set_axis_deadzone gamepad_set_button_threshold gamepad_set_vibration get_directory get_directory_alt get_function_address get_integer get_integer_async get_login_async get_open_filename get_open_filename_ext get_save_filename get_save_filename_ext get_string get_string_async get_timer highscore_add highscore_clear highscore_name highscore_value http_get http_post_string iap_acquire iap_activate iap_consume iap_event_queue iap_files_purchased iap_is_downloaded iap_is_purchased iap_product_details iap_product_files iap_product_status iap_restore_all iap_status iap_store_status ini_close ini_key_delete ini_key_exists ini_open ini_read_real ini_read_string ini_section_delete ini_section_exists ini_write_real ini_write_string instance_activate_all instance_activate_object instance_activate_region instance_change instance_copy instance_create instance_deactivate_all instance_deactivate_object instance_deactivate_region instance_destroy instance_exists instance_find instance_furthest instance_nearest instance_number instance_place instance_position instance_sprite io_clear io_handle irandom irandom_range is_real is_string joystick_axes joystick_buttons joystick_check_button joystick_direction joystick_exists joystick_has_pov joystick_name joystick_pov joystick_rpos joystick_upos joystick_vpos joystick_xpos joystick_ypos joystick_zpos json_decode json_encode keyboard_check keyboard_check_direct keyboard_check_pressed keyboard_check_released keyboard_clear keyboard_get_map keyboard_get_numlock keyboard_key_press keyboard_key_release keyboard_set_map keyboard_set_numlock keyboard_unset_map lengthdir_x lengthdir_y lerp ln log10 log2 logn make_color make_color_hsv make_color_rgb math_set_epsilon max max3 md5_file md5_string_unicode md5_string_utf8 mean median merge_color message_caption min min3 motion_add motion_set mouse_check_button mouse_check_button_pressed mouse_check_button_released mouse_clear mouse_wheel_down mouse_wheel_up move_bounce move_bounce_all move_bounce_solid move_contact move_contact_all move_contact_solid move_outside_all move_outside_solid move_random move_snap move_towards_point move_wrap mp_grid_add_cell mp_grid_add_instances mp_grid_add_rectangle mp_grid_clear_all mp_grid_clear_cell mp_grid_clear_rectangle mp_grid_create mp_grid_destroy mp_grid_draw mp_grid_path mp_linear_path mp_linear_path_object mp_linear_step mp_linear_step_object mp_potential_path mp_potential_path_object mp_potential_settings mp_potential_step mp_potential_step_object network_connect network_connect_raw network_create_server network_create_socket network_destroy network_destroy network_resolve network_send_broadcast network_send_packet network_send_raw network_send_udp network_set_timeout object_exists object_get_depth object_get_mask object_get_name object_get_parent object_get_persistent object_get_solid object_get_sprite object_get_visible object_is_ancestor object_set_depth object_set_mask object_set_parent object_set_persistent object_set_solid object_set_sprite object_set_visible ord os_get_config os_get_language os_is_network_connected os_is_paused os_lock_orientation os_powersave_enable parameter_count parameter_string part_emitter_burst part_emitter_clear part_emitter_create part_emitter_destroy part_emitter_destroy_all part_emitter_exists part_emitter_region part_emitter_stream part_particles_clear part_particles_count part_particles_create part_particles_create_color part_system_automatic_draw part_system_automatic_update part_system_clear part_system_create part_system_depth part_system_destroy part_system_draw_order part_system_drawit part_system_exists part_system_position part_system_update part_type_alpha part_type_alpha1 part_type_alpha2 part_type_alpha3 part_type_blend part_type_clear part_type_color part_type_color1 part_type_color2 part_type_color3 part_type_color_hsv part_type_color_mix part_type_color_rgb part_type_create part_type_death part_type_destroy part_type_direction part_type_exists part_type_gravity part_type_life part_type_orientation part_type_scale part_type_shape part_type_size part_type_speed part_type_sprite part_type_step path_add path_add_point path_append path_assign path_change_point path_clear_points path_delete path_delete_point path_duplicate path_end path_exists path_flip path_get_closed path_get_kind path_get_length path_get_name path_get_number path_get_point_speed path_get_point_x path_get_point_y path_get_precision path_get_speed path_get_x path_get_y path_insert_point path_mirror path_rescale path_reverse path_rotate path_set_closed path_set_kind path_set_precision path_shift path_start physics_apply_force physics_apply_impulse physics_apply_local_force physics_apply_local_impulse physics_apply_torque physics_draw_debug physics_fixture_add_point physics_fixture_bind physics_fixture_create physics_fixture_delete physics_fixture_set_angular_damping physics_fixture_set_awake physics_fixture_set_box_shape physics_fixture_set_circle_shape physics_fixture_set_collision_group physics_fixture_set_density physics_fixture_set_friction physics_fixture_set_kinematic physics_fixture_set_linear_damping physics_fixture_set_polygon_shape physics_fixture_set_restitution physics_fixture_set_sensor physics_joint_delete physics_joint_distance_create physics_joint_enable_motor physics_joint_gear_create physics_joint_get_value physics_joint_prismatic_create physics_joint_pulley_create physics_joint_revolute_create physics_joint_set_value physics_mass_properties physics_pause_enable physics_test_overlap physics_world_create physics_world_draw_debug physics_world_gravity physics_world_update_iterations physics_world_update_speed place_empty place_free place_meeting place_snapped pocketchange_display_reward pocketchange_display_shop point_direction point_distance point_distance_3d position_change position_destroy position_empty position_meeting power radtodeg random random_get_seed random_range random_set_seed randomize real room_add room_assign room_duplicate room_exists room_get_name room_goto room_goto_next room_goto_previous room_instance_add room_instance_clear room_next room_previous room_restart room_set_background room_set_background_color room_set_height room_set_persistent room_set_view room_set_view_enabled room_set_width room_tile_add room_tile_add_ext room_tile_clear round screen_save screen_save_part script_execute script_exists script_get_name sha1_file sha1_string_unicode sha1_string_utf8 shop_leave_rating show_debug_message show_error show_message show_message show_message_async show_question show_question_async sign sin sound_add sound_delete sound_discard sound_exists sound_fade sound_get_name sound_get_preload sound_global_volume sound_isplaying sound_loop sound_play sound_replace sound_restore sound_stop sound_stop_all sound_volume sprite_add sprite_add_from_screen sprite_add_from_surface sprite_assign sprite_collision_mask sprite_create_from_screen sprite_create_from_surface sprite_delete sprite_duplicate sprite_exists sprite_get_bbox_bottom sprite_get_bbox_left sprite_get_bbox_right sprite_get_bbox_top sprite_get_height sprite_get_name sprite_get_number sprite_get_texture sprite_get_tpe sprite_get_width sprite_get_xoffset sprite_get_yoffset sprite_merge sprite_replace sprite_save sprite_save_strip sprite_set_alpha_from_sprite sprite_set_cache_size sprite_set_cache_size_ext sprite_set_offset sqr sqrt string string_byte_at string_byte_length string_char_at string_copy string_count string_delete string_digits string_format string_height string_height_ext string_insert string_length string_letters string_lettersdigits string_lower string_pos string_repeat string_replace string_replace_all string_set_byte_at string_upper string_width string_width_ext surface_copy surface_copy_part surface_create surface_create_ext surface_exists surface_free surface_get_height surface_get_texture surface_get_width surface_getpixel surface_reset_target surface_save surface_save_part surface_set_target tan texture_exists texture_get_height texture_get_width texture_preload texture_set_blending texture_set_interpolation texture_set_priority texture_set_repeat tile_add tile_delete tile_delete_at tile_exists tile_find tile_get_alpha tile_get_background tile_get_blend tile_get_depth tile_get_height tile_get_left tile_get_top tile_get_visible tile_get_width tile_get_x tile_get_xscale tile_get_y tile_get_yscale tile_layer_delete tile_layer_delete_at tile_layer_depth tile_layer_find tile_layer_hide tile_layer_shift tile_layer_show tile_set_alpha tile_set_background tile_set_blend tile_set_depth tile_set_position tile_set_region tile_set_scale tile_set_visible timeline_add timeline_clear timeline_delete timeline_exists timeline_get_name timeline_moment_add timeline_moment_clear transition_define transition_exists url_get_domain url_open url_open_ext url_open_full virtual_key_add virtual_key_delete virtual_key_hide virtual_key_show win8_appbar_add_element win8_appbar_enable win8_appbar_remove_element win8_device_touchscreen_available win8_license_initialize_sandbox win8_license_trial_version win8_livetile_badge_clear win8_livetile_badge_notification win8_livetile_queue_enable win8_livetile_tile_clear win8_livetile_tile_notification win8_search_add_suggestions win8_search_disable win8_search_enable win8_secondarytile_badge_notification win8_secondarytile_delete win8_secondarytile_notification win8_secondarytile_pin win8_settingscharm_add_entry win8_settingscharm_add_html_entry win8_settingscharm_remove_entry win8_share_file win8_share_image win8_share_screenshot win8_share_text win8_share_url window_center window_get_caption window_get_color window_get_cursor window_get_fullscreen window_get_height window_get_sizeable window_get_width window_get_x window_get_y window_handle window_mouse_get_x window_mouse_get_y window_mouse_set window_set_caption window_set_color window_set_cursor window_set_fullscreen window_set_position window_set_rectangle window_set_size window_set_sizeable window_view_mouse_get_x window_view_mouse_get_y window_views_mouse_get_x window_views_mouse_get_y winphone_tile_back_content winphone_tile_back_content_wide winphone_tile_back_image winphone_tile_back_image_wide winphone_tile_back_title winphone_tile_background_color winphone_tile_count winphone_tile_cycle_images winphone_tile_front_image winphone_tile_front_image_small winphone_tile_front_image_wide winphone_tile_icon_image winphone_tile_small_background_image winphone_tile_small_icon_image winphone_tile_title"
			#keywords += "and and_eq asm auto bitand bitor bool break case catch char class compl const const_cast continue default delete do double dynamic_cast else enum explicit export extern false float for friend goto if inline int long mutable namespace new not not_eq operator or or_eq private protected public register reinterpret_cast return short signed sizeof static static_cast struct switch template this throw true try typedef typeid typename union unsigned using virtual void volatile wchar_t while xor xor_eq"
			return keywords
		if set == 2:
			return ""
		if set == 3:
			return "a addindex addtogroup anchor arg attention author b brief bug c class code date def defgroup deprecated dontinclude e em endcode endhtmlonly endif endlatexonly endlink endverbatim enum example exception f$ f[ f] file fn hideinitializer htmlinclude htmlonly if image include ingroup internal invariant interface latexonly li line link mainpage name namespace nosubgrouping note overload p page par param post pre ref relates remarks return retval sa section see showinitializer since skip skipline struct subsection test throw todo typedef union until var verbatim verbinclude version warning weakgroup $ @ \ & < > # { }"

	def color(self, style):
		colors = {32: 0xff3c3c3c,0: 0xff808080,1: 0xff007f00,2: 0xff007f00,3: 0xff3f703f,4: 0xff007f7f,5: 0xff00007f,6: 0xff7f007f,7: 0xff7f007f,
		8: 0xff3c3c3c,9: 0xff7f7f00,10: 0xff000000,11: 0xff3c3c3c,12: 0xff000000,13: 0xff007f00,14: 0xff3f7f3f,15: 0xff3f703f,16: 0xff3c3c3c,
		17: 0xff3060a0,18: 0xff804020,19: 0xff3c3c3c,20: 0xff7f007f,40: 0xffb090b0,64: 0xffc0c0c0,65: 0xff90b090,66: 0xff90b090,67: 0xffd0d0d0,
		68: 0xff90b090,69: 0xff9090b0,70: 0xffb090b0,71: 0xffb090b0,72: 0xffc0c0c0,73: 0xffb0b090,74: 0xffb0b0b0,75: 0xffb0b0b0,76: 0xff000000,
		77: 0xff90b090,78: 0xff7faf7f,79: 0xffc0c0c0,80: 0xffc0c0c0,81: 0xffc0c0c0,82: 0xffc0c0c0,83: 0xffb0b0b0}
		colorsbg = {32: 0xffc3c3c3L,0: 0xff7f7f7fL,1: 0xffff80ffL,2: 0xffff80ffL,3: 0xffc08fc0L,4: 0xffff8080L,5: 0xff80ff80L,6: 0xffffff80L,7: 0xff80ff80L,
		8: 0xffc3c3c3L,9: 0xff8080ffL,10: 0xffffffffL,11: 0xffc3c3c3L,12: 0xffffffffL,13: 0xffff80ffL,14: 0xffc080c0L,15: 0xffc08fc0L,16: 0xffc3c3c3L,
		17: 0xffcf9f5fL,18: 0xff7fbfdfL,19: 0xffc3c3c3L,20: 0xff80ff80L,40: 0xff4f6f4fL,64: 0xff3f3f3fL,65: 0xff6f4f6fL,66: 0xff6f4f6fL,67: 0xff2f2f2fL,
		68: 0xff6f4f6fL,69: 0xff6f6f4fL,70: 0xff4f6f4fL,71: 0xff4f6f4fL,72: 0xff3f3f3fL,73: 0xff4f4f6fL,74: 0xff4f4f4fL,75: 0xff4f4f4fL,76: 0xffffffffL,
		77: 0xff6f4f6fL,78: 0xff805080L,79: 0xff3f3f3fL,80: 0xff3f3f3fL,81: 0xff3f3f3fL,82: 0xff3f3f3fL,83: 0xff4f4f4fL}
		if self.mainwindow.ideTheme==1:
			return QColor(colorsbg[style])
		else:
			return QColor(colors[style])

class ResourceWindow(QtGui.QMdiSubWindow):
	def __init__(self, mainwindow, res):
		QtGui.QMdiSubWindow.__init__(self)
		self.mainwindow=mainwindow
		self.res=res
		self.setWindowTitle(res.getMember("name"))
		n=QLabel("Properties panel")
		self.setWidget(n)
		self.propertiesList=[]

	def saveResource(self):
		CliClass.print_warning("save resource unsupported "+str(self.res))

	def closeEvent(self, closeEvent):
		self.mainwindow.propertiesTable.updatedTable=False
		self.mainwindow.propertiesTable.res=None
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		self.hide()
		closeEvent.accept()
		a=self.mdiArea()
		a.removeSubWindow(self)#clifix stop showing in window list
		w=a.activeSubWindow()
		if w:
			w.showMaximized()

	def updatePropertiesTable(self):
		self.mainwindow.propertiesTable.updatedTable=False
		font=QFont("Helvetica", 10)
		fontbold=QFont("Helvetica", 10, QFont.Bold)
		fontitalic=QFont("Helvetica", 10)
		fontitalic.setItalic(True)
		self.mainwindow.propertiesTable.setSortingEnabled(False)
		self.mainwindow.propertiesTable.clearContents()
		self.mainwindow.propertiesTable.setRowCount(1)
		if self.propertiesList:
			propertiesList=self.propertiesList
		else:
			propertiesList=self.res.members
		for m in propertiesList:
			r=self.res.getMember(m)
			if type(r)==str and r.count("\n")>0:
				CliClass.print_warning("not inserting property "+m)
				continue
			ind=self.mainwindow.propertiesTable.rowCount()-1
			self.mainwindow.propertiesTable.insertRow(ind)
			item=QTableWidgetItem(m)
			item.setFlags(Qt.ItemIsEnabled)
			if self.res.ifDefault(m):
				item.setFont(fontitalic)
			else:
				item.setFont(fontbold)
			self.mainwindow.propertiesTable.setItem(ind, 0, item)
			if type(r)==bool:
				item=QTableWidgetItem()
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)#|Qt.ItemIsTristateQt.ItemIsEditable|
				item.setCheckState(Qt.Unchecked)
				if r:
					item.setCheckState(Qt.Checked)
			else:
				item=QTableWidgetItem(str(r))
				item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsEnabled)
			item.setFont(font)
			self.mainwindow.propertiesTable.setItem(ind, 1, item)
		self.mainwindow.propertiesTable.resizeRowsToContents()
		self.mainwindow.propertiesTable.res=self.res
		self.mainwindow.propertiesTable.subwindow=self
		self.mainwindow.propertiesTable.updatedTable=True

class EditorWindow(ResourceWindow):
	def initEditor(self):
		self.sciEditor = QsciScintilla(self)
		self.sciEditor.setFrameStyle(QsciScintilla.NoFrame)
		#self.sciEditor.setWrapMode(QsciScintilla.WrapCharacter)
		self.sciEditor.setCaretLineVisible(True)
		font = QFont("Courier 10 Pitch", 10)
		font.setFixedPitch(True)
		self.sciEditor.setFont(font)
		lexer = LexerGame(self.mainwindow)
		lexer.setFont(font)
		self.sciEditor.setLexer(lexer)
		fontmetrics = QFontMetrics(font)
		self.sciEditor.setMarginWidth(0, fontmetrics.width("__")+8)
		self.sciEditor.setMarginLineNumbers(0, True)
		self.sciEditor.setMarginSensitivity(1, True)
		self.BREAK_MARKER_NUM = 8
		#self.setMarginWidth()
		self.sciEditor.marginClicked.connect(self.handleMarginClicked)
		#connect(sciEditor,SIGNAL(marginClicked(int, int, Qt.KeyboardModifiers)), self,SLOT(on_margin_clicked(int, int, Qt.KeyboardModifiers)))
		self.sciEditor.markerDefine(QImage(resourcePath+"actions/link_break.png"),self.BREAK_MARKER_NUM);
		self.sciEditor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		self.sciEditor.setFolding(QsciScintilla.BoxedTreeFoldStyle, 3)
		self.sciEditor.setMarginsFont(font)
		if self.mainwindow.ideTheme==1:
			self.sciEditor.setMarginsForegroundColor(QColor("#bbbbbb"))
			self.sciEditor.setCaretLineBackgroundColor(QColor("#333333"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#222222"))
			self.sciEditor.setFoldMarginColors(QColor("#282828"), QColor("#282828"))
			lexer.setPaper(QColor("#222222"))
		else:
			self.sciEditor.setCaretLineBackgroundColor(QColor("#ffe4e4"))
			self.sciEditor.setMarginsBackgroundColor(QColor("#dddddd"))
			self.sciEditor.setFoldMarginColors(QColor("#dddddd"), QColor("#dddddd"))
			lexer.setPaper(QColor("#ffffff"))
		#setIndentationWidth
		self.sciEditor.setTabWidth(2)
		self.sciEditor.SendScintilla(QsciScintillaBase.SCI_SETMULTIPASTE,1)
		q=QWidget()
		self.setWidget(q)
		layout = QVBoxLayout(q)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		# sciEditor.setFixedHeight(300);

	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.initEditor()

	def closeEvent(self, closeEvent):
		ResourceWindow.closeEvent(self, closeEvent)

	def handleMarginClicked(self, nmargin, nline, modifiers):
		# Toggle marker for the line the margin was clicked on
		if self.sciEditor.markersAtLine(nline) != 0:
			self.sciEditor.markerDelete(nline, self.BREAK_MARKER_NUM)
		else:
			self.sciEditor.markerAdd(nline, self.BREAK_MARKER_NUM)

class SpriteWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))
		imageLabel = QLabel()
		p=QPixmap()
		if len(res.subimages)>0:
			p.convertFromImage(res.subimages[0].getQImage())
		imageLabel.setPixmap(p)
		imageLabel.setBackgroundRole(QPalette.Base)
		#imageLabel.setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
		imageLabel.setScaledContents(True)
		w=p.size().width()
		h=p.size().height()
		ww = self.size().width()
		wh = self.size().height()
		imageLabel.resize(w,h)
		scrollArea = QScrollArea()
		scrollArea.setBackgroundRole(QPalette.Dark)
		scrollArea.setWidget(imageLabel)
		q=QWidget()
		self.setWidget(q)
		layout = QVBoxLayout(q) # no initialization here
		layout.addWidget(scrollArea) # layout is uninitialized and probably garbage
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)

class SoundWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class BackgroundWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class PathWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class ScriptWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/script.png"))
		self.sciEditor.setText(res.getMember("value"))

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember("value",str(self.sciEditor.text()))

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember("value",str(self.sciEditor.text()))
		EditorWindow.closeEvent(self, closeEvent)

class ShaderWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))
		self.shaderIndex="vertex"
		self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))
		
		q=QWidget(self)
		self.setWidget(q)
		layout = QVBoxLayout(q)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Shader:"))
		self.shaderList=QComboBox(q)
		self.shaderList.addItem("vertex")
		self.shaderList.addItem("fragment")
		self.shaderList.currentIndexChanged.connect(self.handleShaderListChanged)
		layout2.addWidget(self.shaderList)
		q2.setLayout(layout2)

		layout.addWidget(q2)
		layout.addWidget(self.sciEditor)
		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)

	def handleShaderListChanged(self, event):
		self.saveResource()
		self.shaderIndex=self.shaderList.currentText()
		self.sciEditor.setText(self.res.getMember(str(self.shaderIndex)))

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember(str(self.shaderIndex),str(self.sciEditor.text()))

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			self.res.setMember(str(self.shaderIndex),str(self.sciEditor.text()))
		EditorWindow.closeEvent(self, closeEvent)

class FontWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class TimelineWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/sprite.png"))

class ObjectWindow(EditorWindow):
	def __init__(self, mainwindow, res):
		EditorWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/object.png"))
		ggg=res.WriteGGG(False)
		self.sciEditor.setText(ggg)

	def saveResource(self):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			try:
				self.res.ReadGGG(str(self.sciEditor.text()))
			except NotImplementedError:
				CliClass.print_warning("unsupported")
				closeEvent.ignore()
				return

	def closeEvent(self, closeEvent):
		if self.sciEditor.isModified():
			self.mainwindow.projectSetModified(True)
			try:
				self.res.ReadGGG(str(self.sciEditor.text()))
			except NotImplementedError:
				CliClass.print_warning("unsupported")
				closeEvent.ignore()
				return
			#except:
			#	closeEvent.ignore()
			#	return
		EditorWindow.closeEvent(self,closeEvent)

class RoomWindow(ResourceWindow):
	def __init__(self, mainwindow, res):
		ResourceWindow.__init__(self, mainwindow, res)
		self.setWindowIcon(QIcon(resourcePath+"resources/room.png"))
		self.propertiesList=["name","id","caption","width","height","speed","persistent","clearViewBackground","color","code",
		"rememberRoomEditorInfo","roomEditorWidth","roomEditorHeight","showGrid",
		"showObjects","showTiles","showBackgrounds","showForegrounds","showViews",
		"deleteUnderlyingObj","deleteUnderlyingTiles","page","hsnap","vsnap","isometric",
		"bgFlags","showcolor","enableViews","xoffset","yoffset",
		"PhysicsWorld","PhysicsWorldTop","PhysicsWorldLeft","PhysicsWorldRight","PhysicsWorldBottom","PhysicsWorldGravityX",
		"PhysicsWorldGravityY","PhysicsWorldGravityY","PhysicsWorldPixToMeters"]
		splitter = QSplitter(self)
		q=QWidget(splitter)
		splitter.addWidget(q)
		layout = QVBoxLayout(q)
		self.tree=QTreeWidget(q)
		self.tree.header().setVisible(False)
		self.tree.itemSelectionChanged.connect(self.handleItemSelectionChanged)
		layout.addWidget(self.tree)

		q2=QWidget(q)
		layout2 = QHBoxLayout(q2)
		layout2.addWidget(QLabel("Add Object:"))
		self.shaderList=QComboBox(q)
		self.shaderList.addItem("obj")
		layout2.addWidget(self.shaderList)
		q2.setLayout(layout2)
		layout.addWidget(q2)

		layout.setContentsMargins(0, 0, 0, 0)
		q.setLayout(layout)
		self.scrollAreas = QScrollArea(splitter)
		self.updateTree()
		splitter.addWidget(self.scrollAreas)
		splitter.setSizes([self.width()*.25,self.width()*.75])
		self.setWidget(splitter)
		self.activeItem=None
		self.res.addListener(self.resListener)

	def resListener(self,type,member,value,val):
		self.updateTree()

	def keyReleaseEvent(self, event):
		QWidget.keyReleaseEvent(self, event)
		if event.matches(QKeySequence.Delete):
			item=self.tree.currentItem()
			if item:
				if type(item.res) == CliClass.GameRoomInstance:
					self.res.instances.remove(item.res)
			self.updateTree()

	def handleItemSelectionChanged(self):
		item=self.tree.selectedItems()
		if len(item)>0:
			self.activeItem=item[0].text(0)

	def updateTree(self):
		self.tree.clear()
		self.instancesItem = QTreeWidgetItem(self.tree,["Instances"])
		self.instancesItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.instancesItem.setExpanded(True)
		self.instancesItem.res=None
		self.viewsItem = QTreeWidgetItem(self.tree,["Views"])
		self.viewsItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.viewsItem.setExpanded(True)
		self.viewsItem.res=None
		self.backgroundsItem = QTreeWidgetItem(self.tree,["Backgrounds"])
		self.backgroundsItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.backgroundsItem.setExpanded(True)
		self.backgroundsItem.res=None
		self.tilesItem = QTreeWidgetItem(self.tree,["Tiles"])
		self.tilesItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		self.tilesItem.setExpanded(True)
		self.tilesItem.res=None
		for i in self.res.instances:
			if i.getMember("object"):
				name=i.getMember("object").getMember("name")
			else:
				name=""
			item = QTreeWidgetItem(self.instancesItem,[name,str(i.getMember("x"))+","+str(i.getMember("y"))])
			item.res=i
		for i in self.res.views:
			item = QTreeWidgetItem(self.viewsItem,[str(i.getMember("objectFollowingIndex"))])
			item.res=i
		for i in self.res.backgrounds:
			item = QTreeWidgetItem(self.backgroundsItem,[str(i.getMember("imageIndex"))])
			item.res=i
		for i in self.res.tiles:
			item = QTreeWidgetItem(self.tilesItem,[str(i.getMember("id")),str(i.getMember("backgroundIndex"))])
			item.res=i

		roomView=RoomView(self.scrollAreas, self.res, self)
		roomView.gridX=self.res.getMember("hsnap")
		roomView.gridY=self.res.getMember("vsnap")
		roomView.updateBrush()
		self.scrollAreas.setWidget(roomView)

class MainWindow(QtGui.QMainWindow):
	def __init__(self, app):
		QtGui.QMainWindow.__init__(self)
		self.app=app
		self.ideTheme=1
		self.projectModified=False
		self.projectTitle="noname"
		self.projectLoadPluginLib=False
		self.projectPath=None
		self.debuggerCommands=[]
		self.projectSavingEnabled=False
		CliClass.print_error=self.outputLine
		CliClass.print_warning=self.outputLine
		CliClass.print_notice=self.outputLine
		self.exitAction = QAction("E&xit", self)
		self.exitAction.setShortcuts(QKeySequence.Quit)
		self.exitAction.triggered.connect(self.handleCloseApplication)
		#self.mdiAction = QAction("&Multiple Document Interface", self)
		#self.mdiAction.triggered.connect(self.handleToggleMdiTabs)
		self.licenseAction = QAction("&License", self)
		self.licenseAction.triggered.connect(self.handleShowLicenseDialog)
		self.aboutAction = QAction("&About", self)
		self.aboutAction.triggered.connect(self.handleShowAboutDialog)
		mainMenuBar = QMenuBar(self)
		fileMenu = QMenu("&File", self)
		buildMenu = QMenu("&Build", self)
		debugMenu = QMenu("&Debug", self)
		editMenu = QMenu("&Edit", self)
		viewMenu = QMenu("&View", self)
		#viewMenu.addAction(self.mdiAction)
		updAction = QAction("&Update", self)
		updAction.triggered.connect(self.updateHierarchyTree)
		viewMenu.addAction(updAction)
		resourceMenu = QMenu("&Resources", self)
		windowMenu = QMenu("&Window", self)
		helpMenu = QMenu("&Help", self)
		helpMenu.addAction(self.licenseAction)
		helpMenu.addAction(self.aboutAction)
		mainMenuBar.addMenu(fileMenu)
		mainMenuBar.addMenu(buildMenu)
		mainMenuBar.addMenu(debugMenu)
		mainMenuBar.addMenu(editMenu)
		mainMenuBar.addMenu(viewMenu)
		mainMenuBar.addMenu(resourceMenu)
		mainMenuBar.addMenu(windowMenu)
		mainMenuBar.addMenu(helpMenu)
		self.setMenuBar(mainMenuBar)
		fileToolbar = QToolBar()
		newAction = QAction(QIcon(resourcePath+"actions/new.png"), "&New", self)
		newAction.triggered.connect(self.handleNewAction)
		newAction.setShortcuts(QKeySequence.New)
		fileToolbar.addAction(newAction)
		fileMenu.addAction(newAction)
		openAction = QAction(QIcon(resourcePath+"actions/open.png"), "&Open", self)
		openAction.triggered.connect(self.handleOpenAction)
		openAction.setShortcuts(QKeySequence.Open)
		fileToolbar.addAction(openAction)
		fileMenu.addAction(openAction)
		saveAction = QAction(QIcon(resourcePath+"actions/save.png"), "&Save", self)
		saveAction.triggered.connect(self.handleSaveAction)
		saveAction.setShortcuts(QKeySequence.Save)
		fileToolbar.addAction(saveAction)
		fileMenu.addAction(saveAction)
		saveAsAction = QAction(QIcon(resourcePath+"actions/save-as.png"), "Save As", self)
		saveAsAction.triggered.connect(self.handleSaveAsAction)
		saveAsAction.setShortcuts(QKeySequence.SaveAs)
		fileToolbar.addAction(saveAsAction)
		fileMenu.addAction(saveAsAction)
		fileMenu.addSeparator()
		# add recent projects list
		fileMenu.addSeparator()
		preferencesAction = QAction(QIcon(resourcePath+"actions/preferences.png"), "Preferences", self)
		preferencesAction.triggered.connect(self.actionPreferences)
		fileMenu.addAction(preferencesAction)
		fileMenu.addSeparator()
		fileMenu.addAction(self.exitAction)
		self.addToolBar(fileToolbar)
		buildToolbar = QToolBar(self)
		runAction = QAction(QIcon(resourcePath+"actions/execute.png"), "Run", self)
		runAction.triggered.connect(self.handleRunAction)
		runAction.setShortcuts(QKeySequence("F5"))
		buildToolbar.addAction(runAction)
		buildMenu.addAction(runAction)
		debugAction = QAction(QIcon(resourcePath+"actions/debug.png"), "Debug", self)
		debugAction.triggered.connect(self.handleDebugAction)
		buildToolbar.addAction(debugAction)
		buildMenu.addAction(debugAction)
		"""designAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Design", self)
		buildToolbar.addAction(designAction)
		buildMenu.addAction(designAction)
		compileAction = QAction(QIcon(resourcePath+"actions/compile.png"), "Compile", self)
		buildToolbar.addAction(compileAction)
		buildMenu.addAction(compileAction)
		rebuildAction = QAction(QIcon(resourcePath+"actions/debug.png"), "Rebuild All", self)
		buildToolbar.addAction(rebuildAction)
		buildMenu.addAction(rebuildAction)"""
		self.addToolBar(buildToolbar)
		debugToolbar = QToolBar(self)
		contAction = QAction("Cont", self)
		contAction.triggered.connect(self.handleContAction)
		debugToolbar.addAction(contAction)
		debugMenu.addAction(contAction)
		pauseAction = QAction("Pause", self)
		pauseAction.triggered.connect(self.handlePauseAction)
		debugToolbar.addAction(pauseAction)
		debugMenu.addAction(pauseAction)
		stopAction = QAction("Stop", self)
		stopAction.triggered.connect(self.handleStopAction)
		debugToolbar.addAction(stopAction)
		debugMenu.addAction(stopAction)
		self.addToolBar(debugToolbar)
		"""resourceToolbar = QToolBar(self)
		spriteAction = QAction(QIcon(resourcePath+"resources/sprite.png"), "New Sprite", self)
		spriteAction.triggered.connect(self.actionNewSprite)
		resourceToolbar.addAction(spriteAction)
		soundAction = QAction(QIcon(resourcePath+"resources/sound.png"), "New Sound", self)
		resourceToolbar.addAction(soundAction)
		backgroundAction = QAction(QIcon(resourcePath+"resources/background.png"), "New Background", self)
		resourceToolbar.addAction(backgroundAction)
		pathAction = QAction(QIcon(resourcePath+"resources/path.png"), "New Path", self)
		resourceToolbar.addAction(pathAction)
		scriptAction = QAction(QIcon(resourcePath+"resources/script.png"), "New Script", self)
		scriptAction.triggered.connect(self.actionNewScript)
		resourceToolbar.addAction(scriptAction)
		shaderAction = QAction(QIcon(resourcePath+"resources/shader.png"), "New Shader", self)
		resourceToolbar.addAction(shaderAction)
		fontAction = QAction(QIcon(resourcePath+"resources/font.png"), "New Font", self)
		resourceToolbar.addAction(fontAction)
		timelineAction = QAction(QIcon(resourcePath+"resources/timeline.png"), "New Timeline", self)
		resourceToolbar.addAction(timelineAction)
		objectAction = QAction(QIcon(resourcePath+"resources/object.png"), "New Object", self)
		objectAction.triggered.connect(self.actionNewObject)
		resourceToolbar.addAction(objectAction)
		roomAction = QAction(QIcon(resourcePath+"resources/room.png"), "New Room", self)
		roomAction.triggered.connect(self.actionNewRoom)
		resourceToolbar.addAction(roomAction)
		self.addToolBar(resourceToolbar)"""
		settingsToolbar = QToolBar(self)
		settingsToolbar.addAction(preferencesAction)
		gameSettingsAction = QAction(QIcon(resourcePath+"resources/gm.png"), "Global Game Settings", self)
		gameSettingsAction.triggered.connect(self.actionShowGameSettings)
		settingsToolbar.addAction(gameSettingsAction)
		gameInformationAction = QAction(QIcon(resourcePath+"resources/info.png"), "Game Information", self)
		gameInformationAction.triggered.connect(self.actionShowGameInformation)
		settingsToolbar.addAction(gameInformationAction)
		extensionsAction = QAction(QIcon(resourcePath+"resources/extension.png"), "Extensions", self)
		settingsToolbar.addAction(extensionsAction)
		manualAction = QAction(QIcon(resourcePath+"actions/manual.png"), "Manual", self)
		settingsToolbar.addAction(manualAction)
		self.addToolBar(settingsToolbar)
		self.hierarchyDock = QDockWidget("Hierarchy", self)
		self.hierarchyTree = QTreeWidget(self)
		self.hierarchyTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.hierarchyTree.customContextMenuRequested.connect(self.handleContextMenu)
		#self.hierarchyTree.setContextMenuPolicy(Qt.ActionsContextMenu)
		#self.hierarchyTree.addAction(self.aboutAction)
		self.hierarchyTree.itemActivated.connect(self.handleItemActivated)
		self.hierarchyTree.header().setVisible(False)
		self.hierarchyTree.setIconSize(QSize(18, 18))
		self.hierarchyDock.setWidget(self.hierarchyTree)
		self.hierarchyDock.setMaximumWidth(200)#160
		#self.hierarchyDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.hierarchyDock)
		windowMenu.addAction(self.hierarchyDock.toggleViewAction())
		self.setCorner( Qt.TopLeftCorner, Qt.LeftDockWidgetArea )
		self.setCorner( Qt.TopRightCorner, Qt.RightDockWidgetArea )
		self.setCorner( Qt.BottomLeftCorner, Qt.LeftDockWidgetArea )
		self.setCorner( Qt.BottomRightCorner, Qt.RightDockWidgetArea )
		self.propertiesTable = PropertiesTable(self)
		self.propertiesTable.setColumnCount(2)
		self.propertiesTable.setRowCount(0)
		self.propertiesTable.mainwindow=self
		headers=[]
		headers.append("Name")
		headers.append("Value")
		self.propertiesTable.setHorizontalHeaderLabels(headers)
		self.propertiesTable.verticalHeader().setVisible(False)
		self.propertiesTable.horizontalHeader().resizeSection(0,150)
		#self.propertiesTable.setSortingEnabled(True)
		self.propertiesDock = QDockWidget("Properties", self)
		self.propertiesDock.setWidget(self.propertiesTable)
		self.addDockWidget(Qt.RightDockWidgetArea, self.propertiesDock)
		windowMenu.addAction(self.propertiesDock.toggleViewAction())
		self.logDock = QDockWidget("Log", self)
		self.logText = QTextEdit(self)
		self.logText.setReadOnly(True)
		self.logText.setMaximumHeight(100)
		self.logDock.setWidget(self.logText)
		#self.logDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
		self.addDockWidget(Qt.BottomDockWidgetArea, self.logDock)
		windowMenu.addAction(self.logDock.toggleViewAction())
		#self.tabifyDockWidget(self.logDock, messagesDock)
		self.mainMdiArea = QMdiArea(self)
		# MDIArea's can bet set to tabs, interesting...
		self.mainMdiArea.setDocumentMode(True)
		self.mainMdiArea.setViewMode(QMdiArea.TabbedView)
		#self.mainMdiArea.setBackground(QBrush(QPixmap(resourcePath+"lgm1.png")))
		self.mainMdiArea.setTabsClosable(True)
		self.mainMdiArea.subWindowActivated.connect(self.handleSubWindowActivated)
		self.setCentralWidget(self.mainMdiArea)
		mainStatusBar = QStatusBar(self)
		self.setStatusBar(mainStatusBar)
		mainStatusBar.addWidget(QLabel("Ready"), 0)
		#mainProgressBar = QProgressBar()
		#mainProgressBar.setValue(75)
		#mainStatusBar.addWidget(mainProgressBar)
		self.setWindowIcon(QIcon(resourcePath+"lgm-logo.png"))
		self.projectUpdateWindowTitle()
		self.resize(1000, 600)
		self.showMaximized()
		self.aboutDialog = None
		self.handleNewAction()
		self.updateHierarchyTree()

	def handleContextMenu(self, aPosition):
		item = self.hierarchyTree.itemAt(aPosition)
		if item:
			if item.res:
				menu=QMenu(self)
				openAction = QAction("Open", menu)
				openAction.triggered.connect(lambda x:self.openTreeResource(item))
				menu.addAction(openAction)
				openWindowAction = QAction("Open Window", menu)
				openWindowAction.triggered.connect(lambda x:self.openWindowTreeResource(item))
				menu.addAction(openWindowAction)
				openGGGWindowAction = QAction("Open GGG", menu)
				#openGGGWindowAction.triggered.connect(lambda x:self.openGGGWindowTreeResource(item))
				menu.addAction(openGGGWindowAction)
				renameAction = QAction("Rename", menu)
				renameAction.triggered.connect(lambda x:self.renameTreeResource(item))
				menu.addAction(renameAction)
				deleteAction = QAction("Delete", menu)
				deleteAction.triggered.connect(lambda x:self.deleteTreeResource(item))
				menu.addAction(deleteAction)
				aPosition.setX(aPosition.x()+20)
				aPosition.setY(aPosition.y()+80)
				menu.popup(self.mapToGlobal(aPosition))
			else:
				menu=QMenu(self)
				newAction = QAction("New Resource", menu)
				newAction.triggered.connect(lambda x:self.newTreeResource(item))
				menu.addAction(newAction)
				newGroupAction = QAction("New Group", menu)
				newGroupAction.triggered.connect(lambda x:self.newTreeGroup(item))
				menu.addAction(newGroupAction)
				renameAction = QAction("Rename", menu)
				renameAction.triggered.connect(lambda x:self.renameTreeGroup(item))
				menu.addAction(renameAction)
				deleteAction = QAction("Delete", menu)
				deleteAction.triggered.connect(lambda x:self.deleteTreeGroup(item))
				menu.addAction(deleteAction)
				aPosition.setX(aPosition.x()+20)
				aPosition.setY(aPosition.y()+80)
				menu.popup(self.mapToGlobal(aPosition))

	def deleteTreeResource(self, item):
		if item.res:
			self.gmk.DeleteResource(item.res)
			for w in self.mainMdiArea.subWindowList():
				if w.res==item.res:
					w.close()
					#self.mainMdiArea.setActiveSubWindow(w)
					return
		self.updateHierarchyTree()

	def newTreeResource(self, item):
		group=item.text(0)
		if group=="Sprites":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtSprite)
			s=CliClass.GameSprite(self.gmk,id+1)
			self.gmk.sprites.append(s)
		elif group=="Sounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtSound)
			s=CliClass.GameSound(self.gmk,id+1)
			self.gmk.sounds.append(s)
		elif group=="Backgrounds":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtBackground)
			s=CliClass.GameBackground(self.gmk,id+1)
			self.gmk.backgrounds.append(s)
		elif group=="Paths":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtPath)
			s=CliClass.GamePath(self.gmk,id+1)
			self.gmk.paths.append(s)
		elif group=="Scripts":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtScript)
			s=CliClass.GameScript(self.gmk,id+1)
			self.gmk.scripts.append(s)
		elif group=="Shaders":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtShader)
			s=CliClass.GameShader(self.gmk,id+1)
			self.gmk.shaders.append(s)
		elif group=="Fonts":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtFont)
			s=CliClass.GameFont(self.gmk,id+1)
			self.gmk.fonts.append(s)
		elif group=="Timelines":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtTimeline)
			s=CliClass.GameTimeline(self.gmk,id+1)
			self.gmk.timelines.append(s)
		elif group=="Objects":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtObject)
			s=CliClass.GameObject(self.gmk,id+1)
			self.gmk.objects.append(s)
		elif group=="Rooms":
			id=self.gmk.GetResourceHighestId(CliClass.GameFile.RtRoom)
			s=CliClass.GameRoom(self.gmk,id+1)
			self.gmk.rooms.append(s)
		self.updateHierarchyTree()
		i=self.findTreeItemRes(s)
		self.handleItemActivated(i,0)

	def findTreeItemRes(self, res):
		for c in xrange(self.hierarchyTree.topLevelItemCount()):
			i=self.hierarchyTree.topLevelItem(c)
			for c in xrange(i.childCount()):
				x=i.child(c)
				if x.res==res:
					return x
		return None

	def handleSubWindowActivated(self,window):
		if window:
			window.updatePropertiesTable()
			i=self.findTreeItemRes(window.res)
			if i:
				self.hierarchyTree.setCurrentItem(i)
				return
			CliClass.print_warning("not found activate")

	def handleItemActivated(self, item, column):
		if not item.res:
			return
		for w in self.mainMdiArea.subWindowList():
			if w.res==item.res:
				self.mainMdiArea.setActiveSubWindow(w)
				return
		if item.res.__class__==CliClass.GameSprite:
			s = SpriteWindow(self,item.res)
		elif item.res.__class__==CliClass.GameSound:
			s = SoundWindow(self,item.res)
		elif item.res.__class__==CliClass.GameBackground:
			s = BackgroundWindow(self,item.res)
		elif item.res.__class__==CliClass.GamePath:
			s = PathWindow(self,item.res)
		elif item.res.__class__==CliClass.GameScript:
			s = ScriptWindow(self,item.res)
		elif item.res.__class__==CliClass.GameShader:
			s = ShaderWindow(self,item.res)
		elif item.res.__class__==CliClass.GameFont:
			s = FontWindow(self,item.res)
		elif item.res.__class__==CliClass.GameTimeline:
			s = TimelineWindow(self,item.res)
		elif item.res.__class__==CliClass.GameObject:
			s = ObjectWindow(self,item.res)
		elif item.res.__class__==CliClass.GameRoom:
			s = RoomWindow(self,item.res)
		else:
			CliClass.print_notice("unsupported class "+str(item.res))
			return
		self.mainMdiArea.addSubWindow(s, Qt.Window)
		s.showMaximized()

	def saveOpenResources(self):
		for w in self.mainMdiArea.subWindowList():
			w.saveResource()

	def projectUpdateWindowTitle(self):
		self.setWindowTitle("IDE - "+self.projectTitle+" "+["","*"][self.projectModified])

	def projectSetModified(self,m):
		self.projectModified = m
		self.projectUpdateWindowTitle()

	def updateHierarchyTree(self):
		self.hierarchyTree.clear()
		self.addResourceGroup("Sprites")
		self.addResourceGroup("Sounds")
		self.addResourceGroup("Backgrounds")
		self.addResourceGroup("Paths")
		self.addResourceGroup("Scripts")
		self.addResourceGroup("Shaders")
		self.addResourceGroup("Fonts")
		self.addResourceGroup("Timelines")
		self.addResourceGroup("Objects")
		self.addResourceGroup("Rooms")
		self.addResource("Game Information", QIcon(resourcePath+"resources/info.png"))
		self.addResource("Global Game Settings", QIcon(resourcePath+"resources/gm.png"))
		self.addResource("Extensions", QIcon(resourcePath+"resources/extension.png"))
		for t in self.gmk.triggers:
			self.addResourceToGroup("Triggers",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.constants:
			self.addResourceToGroup("Constants",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.sounds:
			self.addResourceToGroup("Sounds",t,QIcon(resourcePath+"resources/sound.png"))
		for t in self.gmk.sprites:
			self.addResourceToGroup("Sprites",t,QIcon(resourcePath+"resources/sprite.png"))
		for t in self.gmk.backgrounds:
			self.addResourceToGroup("Backgrounds",t,QIcon(resourcePath+"resources/background.png"))
		for t in self.gmk.paths:
			self.addResourceToGroup("Paths",t,QIcon(resourcePath+"resources/path.png"))
		for t in self.gmk.scripts:
			self.addResourceToGroup("Scripts",t,QIcon(resourcePath+"resources/script.png"))
		for t in self.gmk.shaders:
			self.addResourceToGroup("Shaders",t,QIcon(resourcePath+"resources/shader.png"))
		for t in self.gmk.fonts:
			self.addResourceToGroup("Fonts",t,QIcon(resourcePath+"resources/font.png"))
		for t in self.gmk.timelines:
			self.addResourceToGroup("Timelines",t,QIcon(resourcePath+"resources/timeline.png"))
		for t in self.gmk.objects:
			self.addResourceToGroup("Objects",t,QIcon(resourcePath+"resources/object.png"))
		for t in self.gmk.rooms:
			self.addResourceToGroup("Rooms",t,QIcon(resourcePath+"resources/room.png"))

	def addResourceToGroup(self,groupName,res,icon):
		if type(res)==tuple:
			resName=res[0]
		else:
			resName=res.getMember("name")
		for c in xrange(self.hierarchyTree.topLevelItemCount()):
			i=self.hierarchyTree.topLevelItem(c)
			if i.text(0)==groupName:
				treeItem = QTreeWidgetItem(i,[resName])
				treeItem.res=res
				treeItem.setIcon(0, icon)
				return
		#clifix missing resource group
		treeItem = QTreeWidgetItem(self.hierarchyTree,[groupName])
		treeItem.res=None
		treeItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		treeItem.setExpanded(True)
		treeItem = QTreeWidgetItem(treeItem,[resName])
		treeItem.res=res
		treeItem.setIcon(0, icon)

	def handleRunAction(self):
		self.saveOpenResources()
		#es=self.gmk.WriteES()
		if self.projectLoadPluginLib==False:
			CliClass.LoadPluginLib()
			self.projectLoadPluginLib=True
		self.gmk.compileRunEnigma("/tmp/testgame",3)
		self.gameProcessGdb=False
		self.gameProcess = QProcess()
		self.gameProcess.start("/tmp/testgame")
		self.gameProcess.readyReadStandardOutput.connect(self.handleProcessOutput)
		self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.gameProcess.finished.connect(self.handleProcessFinished)

	def handleDebugAction(self):
		self.gameProcessGdb=True
		self.gameProcess = QProcess()
		self.gameProcess.start("gdb /tmp/testgame")
		self.gameProcess.setProcessChannelMode(QProcess.MergedChannels)
		#self.gameProcess.start("/tmp/testgame.exe")
		self.debuggerCommands=["b main","run"]
		self.debuggerCommands.reverse()
		self.gameProcess.readyRead.connect(self.handleProcessOutput)
		self.gameProcess.readyReadStandardError.connect(self.handleProcessErrorOutput)
		self.gameProcess.error.connect(self.handleProcessError)
		self.gameProcess.finished.connect(self.handleProcessFinished)
		
	def handleContAction(self):
		self.outputText("c")
		self.gameProcess.write("c\n")
		pass

	def handlePauseAction(self):
		#clifix get child
		p=self.gameProcess.pid()
		os.kill(p,2)

	def handleStopAction(self):
		self.outputText("quit")
		self.gameProcess.write("quit\n")

	def handleProcessError(self,error):
		self.outputLine("Error "+str(error))

	def handleProcessFinished(self,exit):
		self.outputLine("Finished "+str(exit))

	def handleProcessErrorOutput(self):
		self.gameProcess.setReadChannel(QProcess.StandardError)
		while 1:
			s=self.gameProcess.read(600)
			CliClass.print_notice(str(s))
			if s=="":
				return
			for l in s.split("\n"):
				if l != "":
					self.outputLine(l)

	def handleProcessOutput(self):
		self.gameProcess.setReadChannel(QProcess.StandardOutput)
		while 1:
			s=self.gameProcess.read(600)
			CliClass.print_notice(str(s))
			if s=="":
				return
			for l in s.split("\n"):
				if l != "":
					self.outputLine(l)
				if self.gameProcessGdb and l=="(gdb) ":
					if len(self.debuggerCommands)>0:
						c=self.debuggerCommands.pop()
						self.gameProcess.write(c+"\n")
						self.outputLine(c)

	def actionPreferences(self):
		pass

	def actionNewSprite(self):
		pass

	def actionNewScript(self):
		pass

	def actionNewObject(self):
		pass

	def actionNewRoom(self):
		pass

	def actionShowGameSettings(self):
		pass

	def actionShowGameInformation(self):
		pass

	def handleNewAction(self):
		self.gmk = CliClass.GameFile()
		self.gmk.app=self.app
		self.projectTitle="noname"
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()

	def openProject(self,fileName):
		fileName=str(fileName)
		self.gmk = CliClass.GameFile()
		self.gmk.app=self.app
		self.gmk.Read(fileName)
		self.projectTitle=os.path.split(fileName)[1]
		self.projectUpdateWindowTitle()
		self.updateHierarchyTree()

	def handleOpenAction(self):
		self.projectPath = QFileDialog.getOpenFileName(self,"Open", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if self.projectPath!="":
			CliClass.print_notice(self.projectPath)
			self.openProject(self.projectPath)

	def handleSaveAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_error("saving not enabled")
			return
		if self.projectPath:
			CliClass.print_notice("save file "+fileName)
			self.gmk.Save(fileName)
			self.projectSetModified(False)
		else:
			self.handleSaveAsAction()

	def handleSaveAsAction(self):
		self.saveOpenResources()
		if not self.projectSavingEnabled:
			CliClass.print_error("saving not enabled")
			return
		self.projectPath = QFileDialog.getSaveFileName(self,"Save", "", "Game Files (*.gmk *.gm81 *.gm6 *.egm *.gmx)")
		if self.projectPath!="":
			CliClass.print_notice("save file "+fileName)
			self.gmk.Save(fileName)
			self.projectSetModified(False)

	def handleCloseApplication(self):
		self.saveOpenResources()
		if self.projectModified:
			CliClass.print_notice("close modified")
		self.close()

	def handleShowLicenseDialog(self):
		if self.aboutDialog == None:
			self.aboutDialog = AboutDialog()
		self.aboutDialog.show(":/license.html", "License")

	def handleShowAboutDialog(self):
		if self.aboutDialog == None:
			self.aboutDialog = AboutDialog()
		self.aboutDialog.show(":/about.html", "About");

	#def handleToggleMdiTabs(self):
	#	self.mainMdiArea.setDocumentMode(True);
	#	if self.mainMdiArea.viewMode()==QMdiArea.TabbedView:
	#		self.mainMdiArea.setViewMode(QMdiArea.SubWindowView)
	#	if self.mainMdiArea.viewMode()==QMdiArea.SubWindowView:
	#		self.mainMdiArea.setViewMode(QMdiArea.TabbedView)

	def outputClear(self):
		self.logText.clear()

	def outputText(self, text):
		self.logText.insertPlainText(text)

	def outputLine(self, text):
		self.logText.append(text)

	#def outputMessage(self, origin, location, description):
	#	ind = self.messagesTable.rowCount()
	#	self.messagesTable.insertRow(ind)
	#	self.messagesTable.setItem(ind, 0, QTableWidgetItem(QString.number(ind)))
	#	self.messagesTable.setItem(ind, 1, QTableWidgetItem(origin))
	#	self.messagesTable.setItem(ind, 2, QTableWidgetItem(location))
	#	self.messagesTable.setItem(ind, 3, QTableWidgetItem(description))

	def addResourceGroup(self, name):
		treeItem = QTreeWidgetItem(self.hierarchyTree,[name])
		treeItem.res=None
		treeItem.setIcon(0, QIcon(resourcePath+"resources/group.png"))
		treeItem.setExpanded(True)
	def addResource(self, name, icon):
		treeItem = QTreeWidgetItem(self.hierarchyTree,[name])
		treeItem.setIcon(0, icon)
		treeItem.res=None

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	#app.setStyleSheet(open(resourcePath+"theme.qss").read())
	app.setStyleSheet(" QTabBar::tab { height: 24px; } QStatusBar::item { border: 0px solid black; }");
	window = MainWindow(app)
	window.show()
	if len(sys.argv)>1:
		window.openProject(sys.argv[1])
	sys.exit(app.exec_())
