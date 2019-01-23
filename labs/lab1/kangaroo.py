from numpy import array

from lab1.outline import Outline
from lab1.utils import transform_point


def get_kangaroo():
    points = [
        ((60, 1200), (50, 1178)),
        ((50, 1178), (12, 1143)),
        ((12, 1143), (32, 1070)),
        ((32, 1070), (42, 990)),
        ((42, 990), (50, 930)),
        ((50, 930), (112, 768)),
        ((112, 768), (110, 684)),
        ((110, 684), (68, 596)),
        ((68, 596), (16, 510)),
        ((16, 510), (46, 424)),
        ((46, 424), (114, 358)),
        ((114, 358), (184, 306)),
        ((184, 306), (200, 278)),
        ((200, 278), (200, 236)),
        ((200, 236), (142, 168)),
        ((142, 168), (182, 134)),
        ((182, 134), (256, 214)),
        ((256, 214), (316, 226)),
        ((316, 226), (416, 146)),
        ((416, 146), (456, 184)),
        ((456, 184), (442, 210)),
        ((442, 210), (604, 284)),
        ((604, 284), (700, 50)),
        ((700, 50), (716, 6)),
        ((716, 6), (822, 150)),
        ((822, 150), (654, 366)),
        ((654, 366), (640, 438)),
        ((640, 438), (648, 526)),
        ((648, 526), (576, 682)),
        ((576, 682), (394, 922)),
        ((394, 922), (344, 1030)),
        ((344, 1030), (320, 1064)),
        ((320, 1064), (310, 1090)),
        ((310, 1090), (186, 1166)),
        ((186, 1166), (148, 1190)),
        ((148, 1190), (130, 1178)),
        ((130, 1178), (198, 1090)),
        ((198, 1090), (260, 1006)),
        ((260, 1006), (310, 934)),
        ((310, 934), (360, 762)),
        ((360, 762), (340, 694)),
        ((340, 694), (282, 720)),
        ((282, 720), (244, 742)),
        ((244, 742), (146, 950)),
        ((146, 950), (114, 1030)),
        ((114, 1030), (112, 1066)),
        ((112, 1066), (94, 1168)),
        ((94, 1168), (60, 1200)),
    ]

    helper_points = [
        ((56, 1200), (48, 1196)),
        ((34, 1184), (16, 1174)),
        ((8, 1118), (14, 1096)),
        ((44, 1054), (52, 1002)),
        ((32, 984), (36, 940)),
        ((96, 876), (118, 824)),
        ((112, 768), (110, 684)),
        ((88, 668), (74, 630)),
        ((68, 596), (16, 510)),
        ((0, 494), (6, 446)),
        ((78, 410), (104, 378)),
        ((120, 344), (144, 318)),
        ((188, 290), (194, 284)),
        ((200, 278), (200, 236)),
        ((175, 222), (154, 200)),
        ((136, 140), (168, 124)),
        ((220, 140), (256, 180)),
        ((264, 222), (280, 230)),
        ((330, 180), (418, 136)),
        ((450, 134), (460, 152)),
        ((460, 186), (454, 196)),
        ((516, 220), (572, 248)),
        ((674, 248), (734, 130)),
        ((678, 28), (684, 8)),
        ((787, 40), (810, 74)),
        ((818, 222), (736, 324)),
        ((658, 388), (652, 418)),
        ((646, 513), (649, 543)),
        ((641, 609), (595, 670)),
        ((472, 763), (434, 808)),
        ((382, 984), (365, 1015)),
        ((317, 1058), (321, 1048)),
        ((322, 1076), (318, 1089)),
        ((207, 1175), (188, 1177)),
        ((186, 1166), (148, 1190)),
        ((145, 1196), (129, 1195)),
        ((138, 1132), (161, 1109)),
        ((229, 1073), (261, 1028)),
        ((257, 988), (272, 965)),
        ((348, 878), (366, 812)),
        ((345, 745), (333, 722)),
        ((325, 714), (305, 721)),
        ((270, 715), (253, 722)),
        ((190, 801), (158, 865)),
        ((142, 988), (134, 1009)),
        ((101, 1046), (103, 1057)),
        ((124, 1110), (120, 1137)),
        ((94, 1168), (60, 1200)),
    ]

    for i in range(len(points)):
        points[i] = tuple(transform_point(point, 604, 120, 20) for point in points[i])

    for i in range(len(helper_points)):
        helper_points[i] = tuple(transform_point(point, 604, 120, 20) for point in helper_points[i])

    sections = []
    for (p1, p4), (p2, p3) in zip(points, helper_points):
        sections.append((
            array(p1),
            array(p2),
            array(p3),
            array(p4),
        ))

    return Outline(sections)
