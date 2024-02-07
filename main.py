# grupy:
# - Zarząd 4 (+20)
# - Administratora Forum 22 (+10)
# - Zasłużony 26 (+10)
# - Weteran/Admin/Skrypter 56,8,62  (+7)
# - Moderator Globalny 6, 23 (+5)
# - Sponsor 13 (+3)
#
# Obecni admini:
#
#
# Query:
_ = '''
SELECT v.ip_address, m.member_group_id, v.member_choices 
FROM pro_core_members m 
JOIN pro_core_voters v ON m.member_id = v.member_id 
WHERE m.joined < 1706745600 -- 1 lutego 1:00
    AND v.poll=3719 
GROUP BY v.ip_address HAVING count(*)=1;
'''

import json
import pandas as pd

# Load the uploaded CSV file
file_path = 'votes.csv'
data = pd.read_csv(file_path)

# Define a function to merge and modify the choices as per the instructions
def merge_and_modify_choices(member_choices_str):
    # Load the JSON string to a Python dictionary
    choices = json.loads(member_choices_str)

    # Merge "1" with "2" and "3" with "4", adding 30 to every value inside "2" and "4"
    merged_1_2 = choices["1"] + [x + 30 for x in choices["2"]]
    merged_3_4 = choices["3"] + [x + 30 for x in choices["4"]]

    # Create a new dictionary with the merged lists
    new_choices = {"1": merged_1_2, "2": merged_3_4}

    # Convert the dictionary back to a JSON string
    return json.dumps(new_choices)

# Apply the function to each row in the 'member_choices' column
data['member_choices'] = data['member_choices'].apply(merge_and_modify_choices)
data.head()

#%% count votes with multipliers
# multipliers table
multipliers = {
    4: 20, # Zarząd
    22: 10, # Administratora Forum
    26: 10, # Zasłużony
    56: 7,  # Weteran
    8: 7, # Admin
    62: 7, # Skrypter
    6: 5, # Moderator Globalny
    23: 5, # Starszy Moderator
    13: 3 # Sponsor
}

# Initialize dictionaries to count occurrences of each number in "positives" and "negatives"
positives_counts = {
    3: 15, # Blake_Varisco
    6: 15, # James_Baron
    7: 15, # James_Duble
    10: 15, # Howard_Woods
    11: 15, # Virginia_Grissom
    14: 15, # Michael_Wizard
    18: 15, # Max_Light
    29: 15, # James_Wolfridson
}
negatives_counts = {}

# Iterate through each row to count occurrences, taking the multiplier into account
for index, row in data.iterrows():
    # Extract member_group_id to determine the multiplier
    member_group_id = row['member_group_id']
    multiplier = multipliers.get('member_group_id', 1)  # Use 1 as default if not found in multipliers

    # Load the member_choices JSON string to a Python dictionary
    choices = json.loads(row['member_choices'])

    # Process "positives" (key "1")
    for num in choices["1"]:
        if num in positives_counts:
            positives_counts[num] += multiplier
        else:
            positives_counts[num] = multiplier

    # Process "negatives" (key "2")
    for num in choices["2"]:
        if num in negatives_counts:
            negatives_counts[num] += multiplier
        else:
            negatives_counts[num] = multiplier

# Sort the dictionaries by their keys
positives_counts_sorted = dict(sorted(positives_counts.items()))
negatives_counts_sorted = dict(sorted(negatives_counts.items()))

#%% Plotting
import matplotlib.pyplot as plt

# Plot for Positives
plt.figure(figsize=(20, 8))

# Positives
plt.subplot(1, 2, 1)
plt.bar(positives_counts_sorted.keys(), positives_counts_sorted.values(), color='green')
plt.title('Positives')
plt.xlabel('Number')
plt.ylabel('Count')
plt.xticks(rotation=90)

# Negatives
plt.subplot(1, 2, 2)
plt.bar(negatives_counts_sorted.keys(), negatives_counts_sorted.values(), color='red')
plt.title('Negatives')
plt.xlabel('Number')
plt.ylabel('Count')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()


#%% Sum positives with negatives and plot
# Adjust the calculation to multiply negatives by -1 before summing with positives
adjusted_negatives_counts = {key: value * -1 for key, value in negatives_counts_sorted.items()}
combined_adjusted_counts = {num: positives_counts_sorted.get(num, 0) + adjusted_negatives_counts.get(num, 0) for num in set(positives_counts_sorted) | set(adjusted_negatives_counts)}

# Sort the combined adjusted counts by keys
combined_adjusted_counts_sorted = dict(sorted(combined_adjusted_counts.items()))

# Plotting the adjusted combined counts
plt.figure(figsize=(10, 8))
plt.bar(combined_adjusted_counts_sorted.keys(), combined_adjusted_counts_sorted.values(), color='purple')
plt.title('Combined Positives and Adjusted Negatives')
plt.xlabel('Number')
plt.ylabel('Adjusted Total Count')
plt.xticks(rotation=90)
plt.show()



#%% Add names to plot
names = [
    'Morasznik (Frank_Morashi)',
    '_Michał_ (Danny_Bartolocci)',
    'Kenji (Blake_Varisco)',
    'Smoker3S (Shoji_Ertubo)',
    'FuRRy (Cody_Evans)',
    'Baron (James_Baron)',
    'Duble (James_Duble)',
    '0Pluszak (Jonny_Derp)',
    'Cegła (Thomas_Brick)',
    'Eriket (Howard_Woods)',
    'PRT (Virginia_Grissom)',
    'alicja (Alexys_Montechiaro)',
    'Bratva (Aksziej_Lyubochka)',
    'Darek (Michael_Wizard)',
    'Hubii (Dylan_Crowley)',
    'ShaKeR (Norman_Klama)',
    'Blastuś (Jack_Evans)',
    'Light (Max_Light)',
    'PiTu (Bishop_Dunleavy)',
    'lionelek (Latif_Abassi)',
    'rfvcaperd (Neville_Garnett)',
    'White (Scott_White)',
    'Adam1284 (Adam_Pitterson)',
    'Parker (Brandon_Parker)',
    'Morisson (Johny_Morisson)',
    'kresher (Antonio_Rossi)',
    'Quiks (Todd_Moore)',
    'Copernik (Fenrir_Skjolberg)',
    'Konio (James_Wolfridson)',
    'pogrom (Bae_Bee_Bamby)',
    'M power (Herman_Kroos)',
    'Nikuś (Nicola_Monroe)',
    'Satius (Kinsley_Carrey)',
    'KuKis (Max_Enzo)',
    'eSowaty (Sean_Vance)',
    'Jaro (Quentin_Torrado)',
    'Guerra (Hector_Guerra)',
    'Najemnik (George_Meyer)',
    'onez (Onez_Phahovitch)',
    'domi_nicek (Agatha_Fonk)',
    'MorasznikV2 (Jonathan_Morashi)',
    'Ramsey (Vlad_Iwanow)',
    'Moore Hejzy (Matthew_Ramsey)',
    'Harpaganik (Christopher_Deyoung)',
    'Inmate (Davide_Dinorscio)',
    'kerszer (William_Eisenberg, Felix_Aldredge)',
    'Carlito (Carlito_Brasi)',
    'msr (Novel_Efremov)',
    'Junek (Jun_Sone)',
    'pacmaneq (Ljubomir_Lainovic)',
    'INOX (Raymond_Durrett)'
]

# Adjust the combined_adjusted_counts_sorted dictionary to use names as labels
# This requires matching the index (key in combined_adjusted_counts_sorted) with the names array
# Since names are more than the keys, we match by the index position + 1 to the name
adjusted_labels_combined_counts = {names[key-1]: value for key, value in combined_adjusted_counts_sorted.items() if key-1 < len(names)}

# Plotting the adjusted combined counts with names as labels
plt.figure(figsize=(12, 14))
plt.barh(list(reversed(list(adjusted_labels_combined_counts.keys()))), list(reversed(list(adjusted_labels_combined_counts.values()))), color='orange')
plt.title('Combined Positives and Adjusted Negatives with Names (Descending)')
plt.xlabel('Adjusted Total Count')
plt.ylabel('Names')
plt.tight_layout()
plt.show()

adjusted_labels_combined_counts = {k: v for k, v in sorted(adjusted_labels_combined_counts.items(), key=lambda item: item[1], reverse=True)}

#%% final touch, mark green, change names
# Adjust the plot to color bars green if the count is positive, otherwise orange
colors = ['green' if value > 2 else 'orange' for value in reversed(list(adjusted_labels_combined_counts.values()))]

# Replot with color adjustments
plt.figure(figsize=(12, 14))
plt.barh(list(reversed(list(adjusted_labels_combined_counts.keys()))), list(reversed(list(adjusted_labels_combined_counts.values()))), color=colors)
plt.title('Wyniki wyborów an administratora Mrucznik Role Play')
plt.xlabel('Otrzymane punkty')
plt.ylabel('Names')
plt.tight_layout()
plt.show()


#%% add green labels & sort by values
plt.figure(figsize=(12, 14))

# Create the bars with the previously defined colors
bars = plt.barh(list(reversed(list(adjusted_labels_combined_counts.keys()))), list(reversed(list(adjusted_labels_combined_counts.values()))), color=colors)

# Adjusting tick params to color the labels
ax = plt.gca()
tick_labels = ax.get_yticklabels()

# Set the color of the tick labels based on the value
for label, value in zip(reversed(tick_labels), adjusted_labels_combined_counts.values()):
    label.set_color('green' if value > 2 else 'black')

plt.title('Wyniki wyborów an administratora Mrucznik Role Play')
plt.xlabel('Otrzymane punkty')
plt.ylabel('Names')
plt.tight_layout()
plt.show()
