from pybaseball import batting_stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from adjustText import adjust_text
import pandas as pd

def get_stats(year, stat1, stat2, min_pa=500):
    """
    Fetches Fangraphs batting stats for a given year.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The filtered DataFrame for plotting individual players.
            - dict: A dictionary with the league-wide average for each stat.
    """
   
    print(f"Fetching Fangraphs batting stats for the {year} season...")
    all_stats = batting_stats(year)

    league_averages = {
        'avg_stat1': all_stats[stat1].mean(),
        'avg_stat2': all_stats[stat2].mean()
    }

    filtered_stats = all_stats[all_stats['PA'] >= min_pa]

    batting = filtered_stats[['Name', 'Team', stat1, stat2]]

    return batting, league_averages

def make_scatter_plot(data_to_plot, league_averages, year, stat1, stat2, n=17):
    """
    Creates and displays a scatterplot of individual player stats,
    including league average lines and a curated list of labeled players.
    """
    print("\nCreating scatterplot of individual player stats with league averages...")
    
    avg_stat1 = league_averages['avg_stat1']
    avg_stat2 = league_averages['avg_stat2']

    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Plot all players
    ax.scatter(data_to_plot[stat1], data_to_plot[stat2], alpha=0.5, label='Players')

    # Add average lines
    ax.axvline(x=avg_stat1, color='r', linestyle='--', label=f'League Avg {stat1}: {avg_stat1:.3f}')
    ax.axhline(y=avg_stat2, color='g', linestyle='--', label=f'League Avg {stat2}: {avg_stat2:.3f}')

    # Set axis tick formats to three decimal places
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))

    # Identify top and bottom players for each stat
    top_stat1 = data_to_plot.nlargest(n, stat1)
    bottom_stat1 = data_to_plot.nsmallest(n, stat1)
    top_stat2 = data_to_plot.nlargest(n, stat2)
    bottom_stat2 = data_to_plot.nsmallest(n, stat2)

    # Combine all players to label into a single DataFrame and remove duplicates
    players_to_label = pd.concat([top_stat1, bottom_stat1, top_stat2, bottom_stat2]).drop_duplicates()

    texts = []
    for _, row in players_to_label.iterrows():
        # Adjust 'ha' (horizontal alignment) and 'va' (vertical alignment) 
        # based on the player's quadrant
        ha = 'left' if row[stat1] >= avg_stat1 else 'right'
        va = 'bottom' if row[stat2] >= avg_stat2 else 'top'
        
        text = ax.text(row[stat1], row[stat2], row['Name'], ha=ha, va=va, fontsize=7.5)
        texts.append(text)

    # Use adjust_text to prevent label overlaps with fine-tuned parameters
    adjust_text(texts, 
                arrowprops=dict(arrowstyle='-', color='black', lw=0.5, shrinkA=20),
                expand_points=(1.0, 1.0), # Add more space around data points
                force_text=(0.5, 0.75), # Increase text repulsion force
                force_points=(0.5, 0.5) # Increase point repulsion force
               )

    ax.legend()
    ax.set_title(f'{stat1} vs {stat2} in {year}', weight='bold')
    ax.set_xlabel(f'{stat1}', weight='bold')
    ax.set_ylabel(f'{stat2}', weight='bold')
    ax.grid(True)
    plt.show()

if __name__ == "__main__":

    year_to_analyze = 2025
    x_stat = 'Zone%'
    y_stat = 'ISO'
    player_data, league_avg = get_stats(year_to_analyze, x_stat, y_stat)
    make_scatter_plot(player_data, league_avg, year_to_analyze, x_stat, y_stat)

