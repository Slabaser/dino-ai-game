# score_plot.py
import matplotlib.pyplot as plt

with open("scores_reflex.txt") as f:
    reflex_scores = [int(line.strip()) for line in f]

with open("scores_heuristic.txt") as f:
    heuristic_scores = [int(line.strip()) for line in f]

# Son skorları al
last_reflex_score = reflex_scores[-1] if reflex_scores else 0
last_heuristic_score = heuristic_scores[-1] if heuristic_scores else 0

# Bar grafiği oluştur
labels = ['Reflex Agent', 'Heuristic Agent']
scores = [last_reflex_score, last_heuristic_score]
colors = ['red', 'blue']

plt.bar(labels, scores, color=colors)
plt.ylabel("Skor")
plt.title("Son Oyun Skor Karşılaştırması")
plt.ylim(0, max(scores) + 50)
plt.grid(axis='y')
plt.show()