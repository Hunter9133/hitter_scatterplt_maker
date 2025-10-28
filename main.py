from pybaseball import batting_stats
import matplotlib.pyplot as plt
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
    print(batting.head())

    return batting, league_averages

def make_scatter_plot(data_to_plot, league_averages, year, stat1, stat2):
    """
    Creates and displays a scatterplot of individual player stats,
    including league average lines and a curated list of labeled players from each quadrant.
    
    """
    print("\nCreating scatterplot of individual player stats with league averages...")
    
    avg_stat1 = league_averages['avg_stat1']
    avg_stat2 = league_averages['avg_stat2']

    fig, ax = plt.subplots(figsize=(15, 10))
    
    ax.scatter(data_to_plot[stat1], data_to_plot[stat2], alpha=0.5, label='Players')

    ax.axvline(x=avg_stat1, color='r', linestyle='--', label=f'League Avg {stat1}: {avg_stat1:.3f}')
    ax.axhline(y=avg_stat2, color='g', linestyle='--', label=f'League Avg {stat2}: {avg_stat2:.3f}')

    ax.legend()
    
    ax.set_title(f'{stat1} vs {stat2} in {year}', weight='bold')
    ax.set_xlabel(f'{stat1}', weight='bold')
    ax.set_ylabel(f'{stat2}', weight='bold')
    ax.grid(True)
    plt.show()


if __name__ == "__main__":

    year_to_analyze = 2025
    x_stat = 'OBP'
    y_stat = 'SLG'
    player_data, league_avg = get_stats(year_to_analyze, x_stat, y_stat)
    make_scatter_plot(player_data, league_avg, year_to_analyze, x_stat, y_stat)

