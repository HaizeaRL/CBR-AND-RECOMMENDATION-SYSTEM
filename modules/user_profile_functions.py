# user profile functions
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Image as PlatypusImage, Table, TableStyle
from markdown2 import markdown  # Use markdown2 for better HTML conversion
from bs4 import BeautifulSoup  # Use BeautifulSoup for parsing HTML
from reportlab.lib import colors
from datetime import datetime

# wine catalogues 
df_red = pd.read_parquet(os.path.join("../data", "red_wines_clustered.parquet"), engine ="pyarrow")
df_white = pd.read_parquet(os.path.join("../data", "white_wines_clustered.parquet"), engine ="pyarrow")

# Wine descripors
wine_descriptors = ["Sweetness","Nuance", "Tannicity", "Body", "Vibrancy"]

# Wine descriptors position map
descriptor_values = {"Sweetness":["Dry", "Semi-Dry", "Sweet"],
                     "Nuance": ["Simple", "Complex,Spicy", "Intense"],
                     "Tannicity": ["Soft", "Balanced,Structured", "Robust"],
                     "Body": ["Light", "Medium", "Full-Bodied"],
                     "Vibrancy":["Liveliness", "Live", "Brilliant"]}

# relation of columns and new descriptors
descriptor_dict = {"residual sugar" : "Sweetness",
     "chlorides": "Nuance",
     "sulphates": "Tannicity",
     "Body_tmp": "Body",
     "Vibrancy_tmp": "Vibrancy"}


def get_user_list(path, json_file):
    """
    Function that gets all users wine distribution configuration.

    Parameters:
        path (str): path to users distribution json
        json_file(json): json file to open and get user list.

    Returns:
       list: a list of all users wine distribution configuration.
    """   
    json_file_path = os.path.join(path,json_file)
    
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)
    

def get_users_references(users_list):
    """
    Function that gets all users ids

    Parameters:
        users_list (list):  list of all users wine distribution configuration.

    Returns:
       list(str): a list of all users id.
    """   
    if len(users_list)> 0:
        return [x["user"] for x in users_list]
    
def get_wines_rows(zones):
    """
    Function that list corresponding wines from wine catalogue.

    Parameters:
        zones:  wine distribution per zone.

    Returns:
       list(int): a list indexes to get from wine catalogue.
    """   
    # Loop through each zone and extract the row indices
    row_idx = []
    for zone in zones:
        for key, value in zone.items():
            if '_rows' in key:  # Check if the key ends with '_rows'
                row_idx.extend(value)
    return row_idx
    
def get_specific_wines(df, wine_distr):
    """
    Function that gets corresponding wines from wine catalogue.

    Parameters:
        df:  wine catalogue
        wine_distr: wine distribution per zone.

    Returns:
       Extract selected wines from wine catalogue.
    """  
    
    # get wine rows
    wines_rows = get_wines_rows(wine_distr)
    
    #filter & return user's wines from catalogue
    return df.iloc[wines_rows]
    
def get_specific_user_info (users_list, user_id):
    """
    Function that obtain specific users wine data.

    Parameters:
        users_list (list):  list of all users wine distribution configuration.
        user_id (str): user id to find in all users list

    Returns: user_data, user_red_catalogue, user_white_catalogue
       user_data : users wine profile
       user_red_catalogue : users' red wines list obtained for red wine catalogue.
       user_white_catalogue: users' white wines list obtained for white wine catalogue.
    """   
    
    # initialize data
    user_data = None
    user_red_catalogue = None
    user_white_catalogue = None
    
    # get specific user's data
    user_info = [x for x in users_list if x["user"] == user_id]
    if len(user_info) == 1:
        
        user_data = user_info[0]
                
        # filter and obtain user wine catalogue to create profile
        user_red_catalogue = get_specific_wines(df_red, user_info[0]["red_distribution"])
        user_white_catalogue = get_specific_wines(df_white, user_info[0]["white_distribution"])
    
    return user_data, user_red_catalogue, user_white_catalogue

def map_value_to_position(key, val):
    """
    Function that return the corresponding list position of the categorization

    Parameters:
        key (str): descriptor column name.
        val (str): descriptr column value.

    Returns:
       int position of the list
    """    
    return descriptor_values[key].index(val)

def create_radar_plot(average_df, title, user_id, save_path):
    """
    Function that plots a radar or spider plot according to average wine profile.
    
    Parameters:
        average_df (pd.DataFrame): DataFrame containing average positions for each descriptor.
        user_id (str): User identification code.
        title (str): Title to assign to the plot
        save_path (str) : Path to save the plot
    Returns:
       Plots radar graph corresponding to average wine profile and saves as png.
    """  

    # Prepare categories and corresponding values
    categories = average_df['Descriptor'].tolist()
    values = average_df['Average Position'].tolist()
    values += values[:1]  # Repeat the first value at the end to close the circle

    # Calculate angles for the plot
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Start creating the radar plot
    fig, ax = plt.subplots(1, 2, figsize=(8, 8), subplot_kw=dict(polar=True))

    # Draw one axis per variable and add labels
    ax[0].set_xticks(angles[:-1])
    ax[0].set_xticklabels(categories, size=15)

    # Draw y-labels (customizable based on your data scale)
    ax[0].set_rlabel_position(30)
    plt.yticks([0, 1, 2], ["0", "1", "2"], color="grey", size=7)
    plt.ylim(0, 2)  # Adjust depending on your value range 

    # Plot the radar chart
    ax[0].plot(angles, values, linewidth=2, linestyle='solid', label=title)
    ax[0].fill(angles, values, alpha=0.25)  # Fill area under the graph
    
    # Summary on the right side
    ax[1].axis('off')  # Turn off the axis

    # Add summary text
    summary_text ='\n'.join([f"'{row['Descriptor']}': {round(row['Average Position'],2)}," for index, row in average_df.iterrows()])
    ax[1].text(0.05, 0.05, summary_text, fontsize=16, ha='center', va='center', wrap=False,
              bbox=dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.75'))

    # Set title for the radar plot
    
    ax[1].set_title(title, size=20, color='navy', y=0.90)

    # save file
    title1 = f"{title}_user_{str(user_id)}"
    plt.savefig(os.path.join(save_path, title1 + '.png'), bbox_inches='tight', pad_inches=0.5)

def create_wine_profile_plots(df, title, user_id, save_path):
    """
    Function that creates users wine profile radar plots

    Parameters:
        df (dataframe):  users wine catalogue
        title (str): title to give to created radar plot.
        user_id (str): user identification code.
        save_path (str): path to save created radar plot.

    Returns: user_data, user_red_catalogue, user_white_catalogue
       user_data : users wine profile
       user_red_catalogue : users' red wines list obtained for red wine catalogue.
       user_white_catalogue: users' white wines list obtained for white wine catalogue.
    """   
    
    # Applying the mapping function to each row
    df_f = pd.DataFrame()
    for descriptor in wine_descriptors:
        df_f[descriptor] = df[descriptor].apply(lambda val: map_value_to_position(descriptor, val))

  
    # Calculate average value per each descriptor based on position columns
    average_values = {
        descriptor: df_f[descriptor].mean() for descriptor in wine_descriptors
    }


    # Create a DataFrame for the average values
    average_df = pd.DataFrame.from_dict(average_values, orient='index', columns=['Average Position']).reset_index()
    average_df.rename(columns={'index': 'Descriptor'}, inplace=True)

    # create plots & save
    create_radar_plot(average_df, title, user_id, save_path)

def create_intro_paragraph(user_data):
    """
    Function that creates introductory first paragraph of markdown text.

    Parameters:
        user_data:  users wine data
        
    Returns: 
       first_paragraph (str) : text to add as introductory text.
    """   

    first_paragraph = ""
    total_wines = user_data['wine_qty']
    distribution = user_data["distribution"]
    
    if distribution == "equal":
        first_paragraph = f"Based on {total_wines} wines you tasted, you have no preference between red and white wines."
    else:
        who_more = distribution.split('_')[1]  # "white" or "red"
        other = "red" if who_more == "white" else "white"
        how_more = user_data['how_more']
        
        first_paragraph = (f"Based on the {total_wines} wines you tasted, you tend to prefer {who_more} wines.\n"
                           f"You have tasted {how_more} more {who_more} wines than {other} wines.\n")
    
    return first_paragraph

def zones_distribution_text(user_data):
    """
    Function that creates a red and white wines comparative table by zone in markdown form.

    Parameters:
        user_data:  users wine data
        
    Returns: 
       markdown_text (str) : markdown_text composed by a comparative table.
    """   
    # get wines zones distribution data
    red_zones = {k: v for d in user_data['red_distribution'] for k, v in d.items() if "_rows" not in k}
    red_zones_l = {k: v for d in user_data['red_distribution'] for k, v in d.items() if "_rows" in k}
    white_zones = {k: int(v) for d in user_data['white_distribution'] for k, v in d.items() if "_rows" not in k}
    white_zones_l = {k: v for d in user_data['white_distribution'] for k, v in d.items() if "_rows" in k}
    

    # Ensure all keys (zones) are considered and sort them alphabetically
    all_keys = list(set(red_zones.keys()).union(white_zones.keys()))
    sorted_all_keys = sorted(all_keys, key=lambda x: x.replace('_', ''))

    # Create markdown for wine zone distribution, displaying both red and white side by side
    reds = user_data['red_wines']
    whites = user_data['white_wines']
    markdown_text = f"| Zone | Red Wines ({int(reds)} total) | White Wines ({int(whites)} total) |\n"
    markdown_text += "|------|-----------|-------------|\n"

    # Iterate through sorted zones and present both red and white values
    for k in sorted_all_keys:
        red_value = red_zones.get(k, 0)  # Default to 0 if zone does not exist
        white_value = white_zones.get(k, 0)  # Default to 0 if zone does not exist
        
        # Get wine rows values as wine references
        red_refs = red_zones_l.get(f"{k}_rows", [])  
        white_refs = white_zones_l.get(f"{k}_rows", [])  

       # Convert references array to strings. If there is no references for specific zone "No references" as text.
        red_refs_str = ", ".join(map(str, red_refs)) if red_value > 0 else "No references."
        white_refs_str = ", ".join(map(str, white_refs)) if white_value > 0 else "No references."

        # create table row presenting values side by side
        markdown_text += f"| {k} | {'No references.' if red_value == 0 else f'({int(red_value)}) Wine refs: [{red_refs_str}]'} | {'No references.' if white_value == 0 else f'({int(white_value)}) Wine refs: [{white_refs_str}]'} |\n"

    return markdown_text


def create_profile_text(user_data):
    """
    Function that creates markdown text to set into recommendation pdf.

    Parameters:
        user_data:  users wine data
        
    Returns: 
       profile_text (str) : text to add to pdf file.
    """   
    title = f"Profile of the user: {user_data['user']}"
    first_paragraph = create_intro_paragraph(user_data)
    zones_distribution = zones_distribution_text(user_data)

    # Build the final markdown text for the profile
    profile_text = [
        f"# {title}\n",      
        f"{first_paragraph}\n\n", 
        "## Zones Distribution:\n",
        "Your tendency for wines by zones is as follows:\n\n",
        f"{zones_distribution}\n\n",
        "## Tasting Preferences:\n"
        "Based on wine descriptors, your wine tasting preferences are distributed as follows:\n\n"
    ]
    
    return profile_text  

def create_user_profiles_elements(user_data, user_red_cat, 
                                  user_white_cat, user_id):    
    """
    Function that creates corresponding users elements to complete recommendation pdf.

    Parameters:
        user_data: users wine profile.
        user_red_cat (dataframe): users red wine catalogue. 
        user_white_cat  (dataframe): users white wine catalogue.
        user_id (str): User identification reference.

    Returns: 
       report_tmp (str): path where temporal elements are created
       title_red (str): red wines profile plot filename.
       title_white (str): white wines profile plot filename.
       markdown_text (str) : introductory user profile text to add to pdf
    """   

    # create new folder to save temporal elements
    report_tmp = "../report_tmp"
    os.makedirs(report_tmp, exist_ok=True)
 
        
    # 2- create red / white wines profiling graphs
    title_red = f"red_wine_profile"
    create_wine_profile_plots(user_red_cat, title_red, user_id , report_tmp)
    title_white = f"white_wine_profile"
    create_wine_profile_plots(user_white_cat,title_white, user_id , report_tmp)
    
    # 3 - create text in markdown
    markdown_text = create_profile_text(user_data)
    
    return report_tmp, title_red, title_white, markdown_text

def parse_markdown_table(text):
    """
    Function that parse markdown table.

    Parameters:
        text (str):  markdown_text defined as table.
    Returns:
       Parse passed text.
    """   

    lines = text.strip().split("\n")
    table_data = []

    # Parse the header row (first row)
    headers = [cell.strip() for cell in lines[0].split("|")[1:-1]]  # Ignore first and last empty cell
    table_data.append(headers)

    # Parse the data rows
    for line in lines[2:]:  # Skip the separator line
        row = [cell.strip() for cell in line.split("|")[1:-1]]  # Ignore first and last empty cell
        table_data.append(row)

    return table_data

def format_table(table_data):
    """
    Function that give format to parsed markdown table type text.

    Parameters:
        table_data (str):  parsed markdown table text

    Returns:
       Formate table
    """   
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#c6dcec")),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines for the table
    ]))
    return table

def parse_markdown_text(markdown_texts, styles):
    """
    Function that process and formated markdown text to set in pdf.

    Parameters:
        markdown_texts (str):  markdown_text to process
        styles (getSampleStyleSheet): pdf getSampleStyleSheet file

    Returns:
       Formate text as need.
    """   
    story = []
    for markdown_text in markdown_texts:
        # Convert Markdown to HTML
        html_text = markdown(markdown_text)
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')
        
        for element in soup:
            if element.name in ['h1', 'h2', 'h3']:
                heading_style = f'Heading{element.name[1]}'
                paragraph = Paragraph(element.get_text(), styles[heading_style])
                story.append(paragraph)
            elif element.name == 'ul':  # Handle unordered lists
                for li in element.find_all('li'):
                    bullet_point = Paragraph(f'• {li.get_text()}', styles['Normal'])
                    story.append(bullet_point)
            elif "|" in element.get_text():  # Handle tables
                table_data = parse_markdown_table(element.get_text())
                table = format_table(table_data)
                story.append(Spacer(1, 12))
                story.append(table)
            else:  # Handle regular paragraphs
                paragraph_text = element.get_text().replace("\n", "<br />")
                paragraph = Paragraph(paragraph_text, styles['Normal'])
                story.append(paragraph)
    return story

def create_image_table(image1_path, image2_path):
    """
    Function that create an image table to visualize both wine types plots side by side.

    Parameters:
        image1_path (str):  first image path
        image2_path (str) : second image path.

    Returns:
       an image table to visualize both wine types plots side by side.
    """   
    image_height = 2 * inch
    image_width = 3.5 * inch

    image1 = PlatypusImage(image1_path)
    image1.drawHeight = image_height
    image1.drawWidth = image_width

    image2 = PlatypusImage(image2_path)
    image2.drawHeight = image_height
    image2.drawWidth = image_width

    data = [[image1, image2]]
    table = Table(data)
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    return table

def create_comparative_plot_title (type, solution_df):
    """
    Function that generates title for comparative radar plots.

    Parameters:
        type (str): string that says if title is for red or white wines.
        solution_df (dataframe): dataframe with corresponding recommendation comparative data.

    Returns:
       title (str): comparative plots title.
    """   

    title =""
    if type == "white":
        orig_ref = solution_df['Selected'][0]
        sim_ref = solution_df['Nearest'][0]
        zone = solution_df['Nearest'][len(solution_df)-1]
        title = f"Taste comparation between {type} wines: #{orig_ref+1} and #{sim_ref+1} ({zone})"
    else:
        orig_ref = solution_df['Selected'][0]
        sim_ref = solution_df['Nearest'][0]
        zone = solution_df['Nearest'][len(solution_df)-1]
        title = f"Taste comparation between {type} wines: #{orig_ref+1} and #{sim_ref+1} ({zone})"

    return title

def create_comparative_plots(user_data, solution_red, solution_white, save_path):
    
    """
    Function that generates comparative radar plots.

    Parameters:
        user_data: users wine profile.
        solution_red: red wine recomendation if correspond.
        solution_white: white wine recommendation if correspond.
        save_path: path where to save the plots.

    Returns:
       creates plot and returns
       red_png_title (str): title of generated comparative red wines plot.
       white_png_title (str): title of generated comparative white wines plot.
    """   

    red_png_title = ""
    white_png_title = ""
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    if user_data["distribution"] == "equal":

        # red wines comparative plot
        title = create_comparative_plot_title ("red", solution_red)
        red_png_title = f"Red_comparation_{user_data['user']}_{current_date_str}.png"
        create_comparative_radar_plot(df_red.loc[solution_red["Selected"][0]],
                                      df_red.loc[solution_red["Nearest"][0]],
                                      title, save_path, red_png_title)
        # white wines comparative plot
        title = create_comparative_plot_title ("white", solution_white)
        white_png_title = f"White_comparation_{user_data['user']}_{current_date_str}.png"
        create_comparative_radar_plot(df_white.loc[solution_white["Selected"][0]],
                                      df_white.loc[solution_white["Nearest"][0]],
                                      title, save_path, white_png_title)

    elif user_data["distribution"] == "more_white":

        # white wines comparative plot
        title = create_comparative_plot_title ("white", solution_white)
        white_png_title = f"White_comparation_{user_data['user']}_{current_date_str}.png"
        create_comparative_radar_plot(df_white.loc[solution_white["Selected"][0]],
                                      df_white.loc[solution_white["Nearest"][0]],
                                      title, save_path, white_png_title)
    else:

        # red wines comparative plot
        title = create_comparative_plot_title ("red", solution_red)
        red_png_title = f"Red_comparation_{user_data['user']}_{current_date_str}.png"
        create_comparative_radar_plot(df_red.loc[solution_red["Selected"][0]],
                                      df_red.loc[solution_red["Nearest"][0]],
                                      title, save_path, red_png_title)
    return red_png_title, white_png_title

def add_images_based_on_distribution(story, user_data, report_tmp, red_png_title, white_png_title):
    """
    Function to add images based on the user's distribution preference.
    
    Parameters:
        story (list): The list of story elements for the PDF.
        user_data (dict): User's data including distribution preference.
        report_tmp (str): Path to the temporary report directory.
        red_png_title (str): Filename for the red wine comparison image.
        white_png_title (str): Filename for the white wine comparison image.
    """
    if user_data["distribution"] == "equal":
        # Add both images as a table
        comp_image1_path = os.path.join(report_tmp, red_png_title)
        comp_image2_path = os.path.join(report_tmp, white_png_title)
        story.append(create_image_table(comp_image1_path, comp_image2_path))
    
    elif user_data["distribution"] == "more_red":
        # red path
        comp_image1_path = os.path.join(report_tmp, red_png_title)
        image_height = 3 * inch
        image_width = 5.5 * inch

        image1 = PlatypusImage(comp_image1_path)
        image1.drawHeight = image_height
        image1.drawWidth = image_width
        story.append(image1)
    else:
        # red path
        comp_image1_path = os.path.join(report_tmp, white_png_title)
        image_height = 3 * inch
        image_width = 5.5 * inch

        image1 = PlatypusImage(comp_image1_path)
        image1.drawHeight = image_height
        image1.drawWidth = image_width
        story.append(image1)

    story.append(Spacer(1, 12))  # Add space after images

def create_recomendation_pdf(user_data, user_red_cat, user_white_cat, user_id, 
                              solution_red, solution_white, recommendation_text):
    """
    Function that generates elements to add to pdf and compose report pdf.
    Elements created to add: 
     - Markdown text composed by paragraph and table for user profile definition.
     - Corresponding radar plots for each wine type profile of user.
     - Recommendation markdown text, comparing reference wine with recommended one.
     - Recommendation comparative radar plots.     

    Parameters:
        user_data (dict): User's wine profile.
        user_red_cat (dataframe): User's red wine catalogue. 
        user_white_cat (dataframe): User's white wine catalogue.
        user_id (str): User identification reference.
        solution_red: Red wine recommendation, if applicable.
        solution_white: White wine recommendation, if applicable.
        recommendation_text (str): Recommendation text to add to recommendation pdf.

    Returns:
        str: Path to the generated recommendation PDF.
    """   
    # Create temporal data
    report_tmp, title_red, title_white, markdown_text = create_user_profiles_elements(
        user_data, user_red_cat, user_white_cat, user_id
    )

    # Create corresponding comparative radar plots
    red_png_title, white_png_title = create_comparative_plots(
        user_data, solution_red, solution_white, report_tmp
    )

    # Create a folder to save the last report
    pdf_path = report_tmp.rsplit('_tmp', 1)[0]
    os.makedirs(pdf_path, exist_ok=True)
    
    # Create pdf file name
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    pdf_filename = f"user_{user_id}_recomendation_{current_date_str}.pdf"
    
    # Create a PDF canvas    
    output_file = os.path.join(pdf_path, pdf_filename)
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    
    # Add text content (Markdown or plain text)
    styles = getSampleStyleSheet()
    story.extend(parse_markdown_text(markdown_text, styles))
    story.append(Spacer(1,12))
    
    # Add user profile images
    image1_name = f"{title_red}_user_{str(user_id)}.png"
    image2_name = f"{title_white}_user_{str(user_id)}.png"
    image1_path = os.path.join(report_tmp, image1_name)
    image2_path = os.path.join(report_tmp, image2_name)
    story.append(create_image_table(image1_path, image2_path))
 
    # Insert a page break 
    story.append(PageBreak())

    # Add recommendation text to pdf
    story.extend(parse_markdown_text(recommendation_text, styles))

    # Add comparative images based on the user's distribution
    add_images_based_on_distribution(story, user_data, report_tmp, red_png_title, white_png_title)

    # Build the PDF
    doc.build(story)
    
    return output_file

def key_from_value(value):
    """
    Function that return the corresponding descriptor according to its value from descriptor_dict
    dictionary.

    Parameters:
        value (str): descriptor category.

    Returns:
       returns descriptor value, dictionary key
    """    
    for key,val in descriptor_dict.items():
        if val == value:
            return key


def create_comparative_radar_plot(row, row2, title, save_path, image_title):
    """
    Function that plots radar or spider plot according to wine profile.
    
    Parameters:
        row (pd.DataFrame row): row corresponding to a reference wine profile.
        row2 (pd.DataFrame row): row corresponding to a nearest wine profile.
        title (str): title to assign to the plot.
        save_path (str): path where to save the plot.
        image_title (str): title to assign to the plot.

    Returns:
       plots comparative radar plots between two similar wines.
    """  

    # Prepare categories and corresponding values
    categories = ['Sweetness', 'Nuance', 'Tannicity', 'Body', 'Vibrancy']    

    # reference
    values = [map_value_to_position(key, row[key]) for key in categories]
    values += values[:1]  # Repeat the first value at the end to close the circle
    
    # nearest
    values1 = [map_value_to_position(key, row2[key]) for key in categories]
    values1 += values1[:1]  # Repeat the first value at the end to close the circle

    # Calculate angles for the plot
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Close the loop

    # Start creating the radar plot
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), subplot_kw=dict(polar=True))  # Adjust figure size

    # Draw one axis per variable and add labels
    ax[0].set_xticks(angles[:-1])
    ax[0].set_xticklabels(categories, size=15)

    # Draw y-labels (customizable based on your data scale)
    ax[0].set_rlabel_position(30)
    plt.yticks([0, 1, 2], ["0", "1", "2"], color="grey", size=7)
    plt.ylim(0, 2)  # Adjust depending on your value range 

    # Plot the radar charts
    # reference
    ax[0].plot(angles, values, linewidth=2, linestyle='solid', label="reference")
    ax[0].fill(angles, values, alpha=0.25)  # Fill area under the graph
    # nearest
    ax[0].plot(angles, values1, linewidth=2, linestyle='solid', label="nearest")
    ax[0].fill(angles, values1, alpha=0.25)  
    ax[0].legend()

    # Summary on the right side
    ax[1].axis('off')  # Turn off the axis

    # Add summary text, moving it further to the left    
    summary_text = "\n".join([
        f"$\\bf{{{cat}}}$ " + 
        f":\n{row[cat]} vs {row2[cat]}\n" + 
        f"(V:{round(row[key_from_value(cat)], 2)}) vs (V:{round(row2[key_from_value(cat)], 2)})"
        for i, cat in enumerate(categories)
    ])
    ax[1].text(-0.1, 0.08, summary_text, fontsize=16, ha='left', va='center', wrap=True) 
    
    # Adjust layout for minimal spacing
    plt.subplots_adjust(top=0.85, wspace=0.01, left=0.01, right=0.99)  # Minimal horizontal spacing
    
    # Set title for the radar plot
    fig.suptitle(title, size=20, color='navy', y=0.95) 
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    #plt.show()

    # save file
    plt.savefig(os.path.join(save_path, image_title), bbox_inches='tight', pad_inches=0.5)
    