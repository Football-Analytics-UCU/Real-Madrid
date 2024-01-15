import matplotlib.pyplot as plt
import re
import json
from matplotlib.font_manager import FontProperties


# get data from json file
with open('barca-rm.json', 'r') as file:
    data = json.load(file)
data = data
main_content = data['props']['pageProps']['content']


def show_stats_data(data: dict):
    labels = list(data.keys())
    values = list(data.values())

    def extract_numeric(value):
        if isinstance(value, str):
            # Extract numeric part using regular expression
            numeric_part = re.search(r'\d+(\.\d+)?', value)
            if numeric_part:
                return float(numeric_part.group())
        return float(value)

    float_values = [[extract_numeric(value)
                    for value in sublist] for sublist in values]

    first_team = [el[0] for el in float_values]
    second_team = [el[1] for el in float_values]

    sum_team = [first_team[i] + second_team[i]
                for i in range(min(len(first_team), len(second_team)))]

    first_team_normalized = [first_team[i] * 100 / sum_team[i]
                             for i in range(min(len(first_team), len(sum_team)))]
    second_team_normalized = [second_team[i] * 100 / sum_team[i]
                              for i in range(min(len(second_team), len(sum_team)))]

    fig, ax = plt.subplots(figsize=(10, 6))

    p1 = ax.barh(labels, first_team_normalized,
                 color='firebrick', label='Barcelona')
    p2 = ax.barh(labels, [-val for val in second_team_normalized],
                 color='skyblue', label='Real Madrid')

    for rect in p1:
        width = rect.get_width()
        ax.text(width, rect.get_y() + rect.get_height() / 2,
                f'{first_team[p1.index(rect)]}', ha='left', va='center')

    for rect in p2:
        width = rect.get_width()
        ax.text(width, rect.get_y() + rect.get_height() / 2,
                f'{second_team[p2.index(rect)]}', ha='right', va='center')

    ax.legend()
    ax.set_xticks([])
    plt.show()


def show_table_data(columns: list, table_data: dict, scaleX: float, scaleY: float, fig_size: tuple, title: str, pad=int):
    header_colors = ['lightsteelblue'] * len(columns)
    fig, ax = plt.subplots(figsize=(fig_size), dpi=300)

    the_table = plt.table(
        cellText=table_data, colLabels=columns, loc='center', cellLoc='center', colColours=header_colors, colWidths=[0.1 if len(x) < 15 else 0.15 for x in columns])
    the_table.auto_set_column_width([0])
    the_table.auto_set_font_size(False)
    the_table.scale(scaleX, scaleY)

    ax.set_axis_off()
    ax.set_title(f'Barcelona vs Real Madrid - {title}', pad=pad, fontdict={
                 'fontweight': 'bold', 'fontsize': 16})

    for (row, col), cell in the_table.get_celld().items():
        cell.set_text_props(
            fontproperties=FontProperties(family='serif', size=14))
        if (row == 0) or (col == -1):
            cell.set_text_props(
                fontproperties=FontProperties(weight='bold', size=14))

    plt.show()
