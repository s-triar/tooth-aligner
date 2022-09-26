from constant.enums import ArchType
from utility.bolton_studi_model import Bolton
def init_var_bolton(self):
    self.bolton_studi_model = Bolton()

def get_bolton_prediction_line(self):
    anterior_ratio, overall_ratio = self.bolton_studi_model.get_anterior_overall()
    kmno, kmxo, kmna, kmxa = self.bolton_studi_model.get_overjet()
    print("Bolton: anterior_ratio, overall_ratio => ",anterior_ratio, overall_ratio)
    correction_anterior=0
    correction_overall=0
    correction_arch_anterior = None
    correction_arch_overall = None
    if(anterior_ratio > 77.2):
        # mandibular terlalu besar
        correction_arch_anterior = ArchType.LOWER.value
        correction_anterior = kmna
    elif(anterior_ratio < 77.2):
        # maxillary terlalu besar
        correction_arch_anterior = ArchType.UPPER.value
        correction_anterior = kmxa
    if(overall_ratio > 91.3):
        # mandibular terlalu besar
        correction_arch_overall = ArchType.LOWER.value
        correction_overall = kmno
    elif(overall_ratio < 91.3):
        # maxillary terlalu besar
        correction_arch_overall = ArchType.UPPER.value
        correction_overall = kmxo
    
    ratio_text = "Anterior Ratio: \t {:.3f}\nOverall Ratio: \t {:.3f}".format(anterior_ratio, overall_ratio)
    correction_text = "Anterior {}: \t {:.3f}\nOverall {}: \t {:.3f}".format(
        ArchType.LOWER.name if correction_arch_anterior == ArchType.LOWER.value else ArchType.UPPER.name,
        correction_anterior,
        ArchType.LOWER.name if correction_arch_overall == ArchType.LOWER.value else ArchType.UPPER.name,
        correction_overall
    )
    final_text = "{}\nPembenaran\n{}".format(ratio_text, correction_text)
    print("Bolton",final_text)
    
    pts, pts_correction = self.bolton_studi_model.draw_line_correction_anterior(
            self.models,
            correction_arch_anterior,
            correction_anterior,
        )
    
    pts_not_affected, pts_correction_not_affected = self.bolton_studi_model.draw_line_correction_anterior(
            self.models,
            ArchType.UPPER.value if correction_arch_anterior == ArchType.LOWER.value else ArchType.LOWER.value ,
            0
        )
    return pts, pts_correction, pts_not_affected, pts_correction_not_affected
    
    
    