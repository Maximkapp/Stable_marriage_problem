import matplotlib.pyplot as plt
import networkx as nx


def visualize_matching_step_by_step(men_prefs, women_prefs):
    G = nx.DiGraph()
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())

    x_men = 0
    x_women = 10  # ещё дальше вправо

    y_step = 4  # увеличиваем вертикальный шаг

    positions = {}
    for i, man in enumerate(men):
        positions[man] = (x_men, -i * y_step)
        G.add_node(man, bipartite=0)
    for i, woman in enumerate(women):
        positions[woman] = (x_women, -i * y_step)
        G.add_node(woman, bipartite=1)

    plt.ion()
    fig, ax = plt.subplots(figsize=(14, max(len(men), len(women)) * 0.7 + 4))

    # Фиксируем границы и выключаем автоматическое масштабирование
    ax.set_xlim(x_men - 2, x_women + 2)
    ax.set_ylim(-max(len(men), len(women)) * y_step, y_step)
    ax.invert_yaxis()  # для читаемости сверху вниз

    ax.axis('off')

    ax.text(x_men, y_step - 1, "Мужчины", fontsize=16, fontweight='bold', ha='center')
    ax.text(x_women, y_step - 1, "Женщины", fontsize=16, fontweight='bold', ha='center')

    engagements = {}
    women_partners = {w: None for w in women}
    women_rankings = {
        woman: {man: rank for rank, man in enumerate(prefs)}
        for woman, prefs in women_prefs.items()
    }
    free_men = list(men)

    step = 0
    while free_men:
        man = free_men.pop(0)
        for woman in men_prefs[man]:
            current = women_partners[woman]
            step += 1

            G.clear_edges()
            for m, w in engagements.items():
                G.add_edge(m, w, color='green', weight=2)

            G.add_edge(man, woman, color='red', weight=2, style='dashed')

            ax.clear()
            ax.set_xlim(x_men - 2, x_women + 2)
            ax.set_ylim(-max(len(men), len(women)) * y_step, y_step)
            ax.invert_yaxis()
            ax.axis('off')

            ax.text(x_men, y_step - 1, "Мужчины", fontsize=16, fontweight='bold', ha='center')
            ax.text(x_women, y_step - 1, "Женщины", fontsize=16, fontweight='bold', ha='center')

            ax.set_title(f"Шаг {step}: Мужчина {man} предлагает женщине {woman}", fontsize=14)

            edges = G.edges(data=True)
            colors = [edata.get('color', 'black') for _, _, edata in edges]
            styles = [edata.get('style', 'solid') for _, _, edata in edges]
            weights = [edata.get('weight', 1) for _, _, edata in edges]

            nx.draw_networkx_nodes(G, pos=positions, nodelist=men, node_color='skyblue', node_size=2000, ax=ax)
            nx.draw_networkx_nodes(G, pos=positions, nodelist=women, node_color='lightpink', node_size=2000, ax=ax)
            nx.draw_networkx_labels(G, pos=positions, font_size=12, font_weight='bold', ax=ax)

            for i, (u, v, edata) in enumerate(edges):
                nx.draw_networkx_edges(G, pos=positions, edgelist=[(u, v)],
                                       edge_color=colors[i], style=styles[i],
                                       width=weights[i], ax=ax,
                                       connectionstyle='arc3,rad=0.15')

            plt.pause(1)

            if current is None:
                engagements[man] = woman
                women_partners[woman] = man
                break
            elif women_rankings[woman][man] < women_rankings[woman][current]:
                free_men.append(current)
                del engagements[current]
                engagements[man] = woman
                women_partners[woman] = man
                break

        G.clear_edges()
        for m, w in engagements.items():
            G.add_edge(m, w, color='green', weight=3)

        ax.clear()
        ax.set_xlim(x_men - 2, x_women + 2)
        ax.set_ylim(-max(len(men), len(women)) * y_step, y_step)
        ax.invert_yaxis()
        ax.axis('off')

        ax.text(x_men, y_step - 1, "Мужчины", fontsize=16, fontweight='bold', ha='center')
        ax.text(x_women, y_step - 1, "Женщины", fontsize=16, fontweight='bold', ha='center')

        ax.set_title(f"После шага {step}: Текущие пары", fontsize=14)

        nx.draw_networkx_nodes(G, pos=positions, nodelist=men, node_color='skyblue', node_size=2000, ax=ax)
        nx.draw_networkx_nodes(G, pos=positions, nodelist=women, node_color='lightpink', node_size=2000, ax=ax)
        nx.draw_networkx_labels(G, pos=positions, font_size=12, font_weight='bold', ax=ax)

        edges = G.edges(data=True)
        for i, (u, v, edata) in enumerate(edges):
            nx.draw_networkx_edges(G, pos=positions, edgelist=[(u, v)],
                                   edge_color=edata.get('color', 'green'),
                                   width=edata.get('weight', 3), ax=ax,
                                   connectionstyle='arc3,rad=0.15')
        plt.pause(1.5)

    plt.ioff()
    plt.show()
