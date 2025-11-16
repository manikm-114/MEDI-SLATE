# DatasetPaper/code/build_pipeline_diagram.py

from graphviz import Digraph
from utils import ensure_dir

# DatasetPaper/code/build_pipeline_diagram.py

import os

# Add the correct Graphviz path explicitly
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz-14.0.4-win64\bin"

from graphviz import Digraph
from utils import ensure_dir




def build_pipeline():
    ensure_dir("../figures")

    dot = Digraph(comment="MILU23 Dataset Pipeline")
    dot.attr(rankdir='LR', size='9,5')

    dot.node('A', 'Classroom Lecture\n(Video Recording)')
    dot.node('B', 'Audio Extraction')
    dot.node('C', 'Raw Speech-to-Text')
    dot.node('D', 'Script Refinement\n(ChatGPT)')
    dot.node('E', 'Slide Images\n(Exported JPG)')
    dot.node('F', 'Slide–Text Alignment')
    dot.node('G', 'Final Dataset\n(Images + Refined Scripts)')

    dot.edge('A','B')
    dot.edge('B','C')
    dot.edge('C','D')
    dot.edge('D','F')
    dot.edge('E','F')
    dot.edge('F','G')

    dot.render('../figures/fig_pipeline_diagram', format='png', cleanup=True)
    print("✔ Pipeline diagram generated.")

if __name__ == "__main__":
    build_pipeline()
