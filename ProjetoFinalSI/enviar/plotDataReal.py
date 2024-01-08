## Gabriel Conte, João Carvalho, Maria Pedroso
# Código usado para exibir os dados obtidos pela implementacao em tempo real
import matplotlib.pyplot as pt
import seaborn as sn
import pandas as pd

# Dados obtidos pela implementação e anotados em outro software
matConfFrame = [[4,1],[2,3]]
matConfConj = [[4,1],[3,2]]

# plota a matrix de confusao para a implementação frame a frame
df_cm = pd.DataFrame(matConfFrame, range(2), range(2))
sn.set(font_scale=1.4) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size

pt.show()

# plota a matrix de confusao para a implementação de conjunto
df_cm = pd.DataFrame(matConfConj, range(2), range(2))
sn.set(font_scale=1.4) # for label size
sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size

pt.show()