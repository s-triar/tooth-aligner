import numpy as np

from vedo import Point
from constant.enums import ArchType, LandmarkType, ToothType
from utility.arch import Arch
from utility.calculation import find_closest_point_between_a_point_and_a_3pts_plane


def get_flat_plane(self):
    if Arch._is_complete():
        coords = []
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            
            pts = np.array([
                mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
                np.mean([
                    mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
                    mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]]
                ], axis=0),
                mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]]
            ])
            for pp in pts:
                self.model_plot.add(Point(pp, c="violet"))
            print("pts plane",pts)
            # n = np.cross(pts[0]-pts[1],pts[2]-pts[1])
            # n = n/np.linalg.norm(n)
            pts_cusps=np.array([
                mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
                mesh.points()[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
                mesh.points()[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
                mesh.points()[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
                mesh.points()[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.CUSP.value]],
                mesh.points()[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.CUSP.value]],
                mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
                
                mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]],
                mesh.points()[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.CUSP.value]],
                mesh.points()[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.CUSP.value]],
                mesh.points()[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
                mesh.points()[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
                mesh.points()[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
                mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            ])
            
            print("pts_cusps",pts_cusps)
            new_coords = []
            for pt in pts_cusps:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords.append(new_coord)
            coords.append(new_coords)
        return coords
    else:
        return []
            
            

    