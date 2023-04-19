import dearpygui.dearpygui as dpg
from .misc import *
from multiprocessing import Queue
from stp_conf.load_json import *
from typing import Any

def draw_info_table(bmk:str, data_for_table:dict[str, str]) -> None:
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("БМК:")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[0]])), tag=f"row{bmk}_{0}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("БМКC:")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[1]])), tag=f"row{bmk}_{1}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("БМКCК:")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[2]])), tag=f"row{bmk}_{2}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[3]])), tag=f"row{bmk}_{3}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление 0 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[4]])), tag=f"row{bmk}_{4}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Температура: 1")
        dpg.add_text(str(data_for_table[list(data_for_table)[6]])[0] + str(data_for_table[list(data_for_table)[6]])[1:-1] +'.'+ data_for_table[list(data_for_table)[6]][3:], tag=f"row{bmk}_{6}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 0,5 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[7]])), tag=f"row{bmk}_{7}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 1,0 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[8]])), tag=f"row{bmk}_{8}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 1,5 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[9]])), tag=f"row{bmk}_{9}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 2,0 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[10]])), tag=f"row{bmk}_{10}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 2,5 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[11]])), tag=f"row{bmk}_{11}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 3,0 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[12]])), tag=f"row{bmk}_{12}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Давление ступени 3,5 (кПа):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[13]])), tag=f"row{bmk}_{13}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Напряжение питания:")
        dpg.add_text(str(str(int(data_for_table[list(data_for_table)[15]]))) + "B", tag=f"row{bmk}_{15}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Температура для вкл. обогрева:")
        dpg.add_text(data_for_table[list(data_for_table)[16]][0] + str(int(data_for_table[list(data_for_table)[16]][1:])), tag=f"row{bmk}_{16}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Время работы (C):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[17]])), tag=f"row{bmk}_{17}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Калибровка первого датчика:")
        dpg.add_text(data_for_table[list(data_for_table)[18]], tag=f"row{bmk}_{18}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Калибровка второго датчика:")
        dpg.add_text(data_for_table[list(data_for_table)[19]], tag=f"row{bmk}_{19}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Код ступени:")
        dpg.add_text(styp_torm(data_for_table[list(data_for_table)[20]]), tag=f"row{bmk}_{20}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Состояние управляющих цепей:")
        dpg.add_text(state_l(data_for_table[list(data_for_table)[21]]), tag=f"row{bmk}_{21}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Температура от второго датчика:")
        dpg.add_text(data_for_table[list(data_for_table)[22]][0] + str(data_for_table[list(data_for_table)[22]])[1:-1] +'.'+str(data_for_table[list(data_for_table)[22]])[3:], tag=f"row{bmk}_{22}")
    with dpg.table_row(parent= f"MT_{bmk}"):
        dpg.add_text("Общее время работы (Часы):")
        dpg.add_text(str(int(data_for_table[list(data_for_table)[23]])), tag=f"row{bmk}_{23}")
    

def draw_scheme_at_run_time() -> None:
    windows_bmk_pos: list[list[int]] = []
    for bmk in list_of_bmk.keys():
        windows_bmk_pos.append(dpg.get_item_pos(f"BMK:{bmk}"))
    w, h, c, d = dpg.load_image('./img/post.png')
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=w, height=h, default_value=d, tag="post_tag")
    dpg.add_text(parent="Main window", pos=(
        470, 40), default_value="СТП АРС-4",       color=(0, 0, 0, 255), tag="Main lable")
    with dpg.window(tag=f"TIME", pos=(480, 60), no_background=True, no_resize=True, no_close=True, no_title_bar=True, min_size=(60, 60), height=60, no_move=True):
        dpg.add_text(tag='time_tag', pos=(15, 3),
                     default_value="TIME", color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(480, 42), p2=(570, 42), thickness=20, color=(
        int(0.70 * 255), int(1.00 * 255), int(0.70 * 255), int(1.00 * 255)))

    dpg.add_image(parent="Main window", texture_tag='post_tag',
                  pos=(350, 570), width=300, height=200)
    dpg.add_text(parent="Main window", pos=(180, 60),
                 default_value="МОСКВА",          color=(0, 0, 0, 255))
    dpg.add_text(parent="Main window", pos=(740, 60),
                 default_value="САНКТ-ПЕТЕРБУРГ", color=(0, 0, 0, 255))
    dpg.add_text(parent="Main window", pos=(
        180, windows_bmk_pos[2][1] - 20), default_value="107СПУ")
    dpg.add_text(parent="Main window", pos=(
        280, windows_bmk_pos[2][1] + 5), default_value="107")
    dpg.add_text(parent="Main window", pos=(
        100, windows_bmk_pos[7][1] - 20), default_value="106-119СПУ")
    dpg.add_text(parent="Main window", pos=(
        210, windows_bmk_pos[7][1] - 20), default_value="119-120АПУ")
    dpg.add_text(parent="Main window", pos=(
        280, windows_bmk_pos[7][1] + 5), default_value="120")
    dpg.add_text(parent="Main window", pos=(
        140, windows_bmk_pos[7][1] + 5), default_value="119")
    dpg.draw_arrow(parent="Main window", p1=(100, 50), p2=(
        300, 50), thickness=3, color=(0, 0, 0, 255))
    dpg.draw_arrow(parent="Main window", p1=(900, 50), p2=(
        700, 50), thickness=3, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(90,  windows_bmk_pos[2][1] - 25), p2=(
        300, windows_bmk_pos[2][1] - 25), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(300, windows_bmk_pos[2][1] - 25), p2=(
        windows_bmk_pos[0][0], windows_bmk_pos[0][1] + 29), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(300, windows_bmk_pos[2][1] - 25), p2=(
        windows_bmk_pos[2][0], windows_bmk_pos[2][1] + 30), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(300, windows_bmk_pos[7][1] - 25), p2=(
        windows_bmk_pos[4][0], windows_bmk_pos[4][1] + 29), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(300, windows_bmk_pos[7][1] - 25), p2=(
        windows_bmk_pos[7][0], windows_bmk_pos[7][1] + 29), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(160, windows_bmk_pos[7][1] - 25), p2=(
        windows_bmk_pos[10][0], windows_bmk_pos[10][1] + 29), thickness=4, color=(0, 0, 0, 255))
    dpg.draw_line(parent="Main window", p1=(90,  windows_bmk_pos[7][1] - 25), p2=(
        300, windows_bmk_pos[7][1] - 25), thickness=4, color=(0, 0, 0, 255))
    for i in range(len(windows_bmk_pos)):
        if i == 1 or i == 3 or i == 6 or i == 9 or i == 11:
            dpg.draw_line(parent="Main window", p1=(400, windows_bmk_pos[i][1] + 29), p2=(
                900, windows_bmk_pos[i][1] + 29), thickness=4, color=(0, 0, 0, 255))

def draw_bmk_at_runtime(q_task: Any) -> None:
    for bmk in list_of_bmk.keys():
        with dpg.window(tag=f"BMK:{bmk}", pos=win_pos, no_background=True, no_resize=True, no_close=True, no_title_bar=True, autosize=True, no_move=True, no_collapse=True):
            dpg.add_button(label=" ИНФ.", tag=f"bmk_{bmk}", pos=(7, 18))
            dpg.add_button(
                label="ДАВЛ.", tag=f'pr_{bmk}', user_data=q_task, pos=(70, 18))
            dpg.add_button(label="ОШИБ.", tag=f"err_{bmk}", pos=(133, 18))
            dpg.add_text(f"{list_of_bmk[bmk]}",
                         pos=(75, 40), tag=f'text_{bmk}')
            dpg.draw_line(p1=(0, 53), p2=(200, 53), thickness=4,
                          color=(0, 0, 0, 255), tag=f'line_{bmk}')
            dpg.draw_line(p1=(70, 65), p2=(115, 65), thickness=12,
                          color=(255, 0, 255, 255), tag=f'line_bmk_{bmk}')
        win_pos[0] += 200
        current_index_bmk = (list(list_of_bmk.keys()).index(bmk) + 1)
        if current_index_bmk == 2 or current_index_bmk == 4 or current_index_bmk == 7 or current_index_bmk == 10:
            win_pos[1] += 100
            win_pos[0] = 400


def create_theme_imgui_light():
    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (191, 191, 191, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (1 * 255, 1 * 255, 1 * 255, 1 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0 * 255, 1 * 255, 0 * 255, 1 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (int(0.60 * 255), int(0.60 * 255), int(0.60 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(0.98 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (int(0), int(0), int(0), int(191)))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.40 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.67 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (int(0.96 * 255), int(0.96 * 255), int(0.96 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (int(0.82 * 255), int(0.82 * 255), int(0.82 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(0.51 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (int(0.86 * 255), int(0.86 * 255), int(0.86 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (int(0.98 * 255), int(0.98 * 255), int(0.98 * 255), int(0.53 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (int(0.69 * 255), int(0.69 * 255), int(0.69 * 255), int(0.80 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (int(0.49 * 255), int(0.49 * 255), int(0.49 * 255), int(0.80 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (int(0.49 * 255), int(0.49 * 255), int(0.49 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.78 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (int(0.46 * 255), int(0.54 * 255), int(0.80 * 255), int(0.60 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (int(0.70 * 255), int(1.00 * 255), int(0.70 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.31 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.80 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (int(0.39 * 255), int(0.39 * 255), int(0.39 * 255), int(0.62 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (int(0.14 * 255), int(0.44 * 255), int(0.80 * 255), int(0.78 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (int(0.14 * 255), int(0.44 * 255), int(0.80 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (int(0.35 * 255), int(0.35 * 255), int(0.35 * 255), int(0.17 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.67 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.95 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (int(0.76 * 255), int(0.80 * 255), int(0.84 * 255), int(0.93 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.80 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (int(0.60 * 255), int(0.73 * 255), int(0.88 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (int(0.92 * 255), int(0.93 * 255), int(0.94 * 255), int(0.99 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (int(0.74 * 255), int(0.82 * 255), int(0.91 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.22 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (int(0.20 * 255), int(0.20 * 255), int(0.20 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (int(0.39 * 255), int(0.39 * 255), int(0.39 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (int(1.00 * 255), int(0.43 * 255), int(0.35 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (int(0.90 * 255), int(0.70 * 255), int(0.00 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (int(1.00 * 255), int(0.45 * 255), int(0.00 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (int(0.78 * 255), int(0.87 * 255), int(0.98 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (int(0.57 * 255), int(0.57 * 255), int(0.64 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (int(0.68 * 255), int(0.68 * 255), int(0.74 * 255), int(1.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.00 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (int(0.30 * 255), int(0.30 * 255), int(0.30 * 255), int(0.09 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.35 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.95 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (int(0.26 * 255), int(0.59 * 255), int(0.98 * 255), int(0.80 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (int(0.70 * 255), int(0.70 * 255), int(0.70 * 255), int(0.70 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (int(0.20 * 255), int(0.20 * 255), int(0.20 * 255), int(0.20 * 255)))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (int(0.20 * 255), int(0.20 * 255), int(0.20 * 255), int(0.35 * 255)))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg       , (191, 191, 191, int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg        , (int(0.0 * 255), int(0.0 * 255), int(0.00 * 255), int(1 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder    , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg      , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder  , (int(0 * 255), int(0 * 255), int(0 * 255), int(1 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText    , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText     , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText     , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_XAxis         , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_XAxisGrid     , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis         , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid     , (int(1.00 * 255), int(1.00 * 255), int(1.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis2        , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid2    , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.50 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis3        , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid3    , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.50 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection     , (int(0.82 * 255), int(0.64 * 255), int(0.03 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Query         , (int(0.00 * 255), int(0.84 * 255), int(0.37 * 255), int(1.00 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs    , (int(0.00 * 255), int(0.00 * 255), int(0.00 * 255), int(0.50 * 255)), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (248, 248, 248, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (66, 150, 250, 100), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (66, 150, 250, 160), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (90, 170, 250, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (90, 170, 250, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (225, 225, 225, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (180, 180, 180, 100), category=dpg.mvThemeCat_Nodes)
    return theme_id
