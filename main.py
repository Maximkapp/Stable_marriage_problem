from algorithm import gale_shapley
from visualize import visualize_matching_step_by_step
from data import men_preferences, women_preferences

if __name__ == "__main__":
    print("=== Алгоритм Гэйла-Шепли ===")
    result = gale_shapley(men_preferences, women_preferences)
    for man, woman in result.items():
        print(f"{man} — {woman}")

    print("\n=== Визуализация ===")
    visualize_matching_step_by_step(men_preferences, women_preferences)
