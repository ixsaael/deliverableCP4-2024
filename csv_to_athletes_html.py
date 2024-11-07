import csv
import os
import re

def generate_html_links(directory, current_filename):
    links = []
    
    filename_sorted = sorted(os.listdir(directory)) 

    for filename in filename_sorted:
       if filename.endswith(".html") and filename != current_filename:
        name_without_extension = os.path.splitext(filename)[0]
        display_name = re.sub(r'\d+$', '', name_without_extension)  
        link = f' <a href = "./../mens_team/{filename}" > {display_name} </a><br>'
        links.append(link)
        
    links_html = "\n".join(links)
    nav_links = f""" <nav><details><summary class="nav-button">Men's Roster</summary><div class="dropdown-content">\n{links_html}\n</div></details></nav>"""
    
    return nav_links

def generate_html_links2(directory, current2_filename):
    links = []
    
    filename_sorted = sorted(os.listdir(directory)) 
    
    for filename in filename_sorted:
       if filename.endswith(".html") and filename != current2_filename:
        name_without_extension = os.path.splitext(filename)[0]
        display_name = re.sub(r'\d+$', '', name_without_extension)  
        link = f' <a href = "./../womens_team/{filename}" > {display_name} </a><br>'
        links.append(link)
        
    links_html = "\n".join(links)
    nav_links = f""" <nav><details><summary class="nav-button">Women's Roster</summary><div class="dropdown-content">\n{links_html}\n</div></details></nav>""" 
    
    return nav_links

dir = os.getcwd()

def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
    # Start building the HTML structure with updated elements and classes
    
    nav_html = generate_html_links(dir + "/mens_team", os.path.basename(outfile))
    nav_html2 = generate_html_links2(dir + "/womens_team", os.path.basename(outfile))
    
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://kit.fontawesome.com/YOUR_ID.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/style.css">
    <title>{data["name"]}</title>
</head>
<body data-theme="light">

    <!-- Navigation links -->
    <div class="button-row">
        <details><summary class="nav-button">Content</summary>
            <div class="dropdown-content">
                <a href="./../index.html">Home</a><br>
                <a href="#header">Profile</a><br>
                <a href="#athlete-sr-table">Year-stats</a><br>
                <a href="#athlete-result-table">Race stats</a><br>
                <a href="#footer">Other</a>
        </div>
    </details>
        {nav_html}
        {nav_html2}
    </div>

    <!-- Header with athlete name and profile image -->
    <header id="header" class="sticky-header">
        <h1>{data["name"]}</h1>
        <img src="../images/profiles/{data["athlete_id"]}.jpg" 
             alt="Profile picture of {data["name"]}" 
             class="athlete-profile1" 
             onclick="openLightbox(this.src)" 
             onerror="this.onerror=null; this.src='../images/default_image.jpg'; this.setAttribute('onclick', 'openLightbox(this.src)');">
    </header>
    
    <!-- Lightbox overlay structure -->
    <div class="lightbox" id="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <img id="lightbox-img" src="" alt="Enlarged profile image">
    </div>

    <main id="main">
        <!-- Seasonal Records Section -->
        <section id="athlete-sr-table" class="table-container">
            <h2 class="section-title">Athlete's Seasonal Records (SR) per Year</h2>
            <table>
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Season Record (SR)</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Season Records Rows Here -->
    '''
    for sr in data["season_records"]:
        html_content += f'''
                    <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                    </tr>
        '''
    html_content += '''
                </tbody>
            </table>
        </section>

        <!-- Race Results Section -->
        <section id="athlete-result-table" class="table-container">
            <h2 class="section-title">Race Results</h2>
            <table id="athlete-table">
                <thead>
                    <tr>
                        <th>Race</th>
                        <th>Athlete Time</th>
                        <th>Athlete Place</th>
                        <th>Race Comments</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Race Results Rows Here -->
    '''
    for race in data["race_results"]:
        html_content += f'''
                    <tr class="result-row">
                        <td><a href="{race["url"]}">{race["meet"]}</a></td>
                        <td>{race["time"]}</td>
                        <td>{race["finish"]}</td>
                        <td>{race["comments"]}</td>
                    </tr>
        '''
    html_content += '''
                </tbody>
            </table>
    </main>

    <!-- Footer Section -->
    <footer id="footer">
        <p>
            Skyline High School<br>
            <address>
                2552 North Maple Road<br>
                Ann Arbor, MI 48103<br><br>
            </address>
            <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
            Follow us on <a href="https://www.instagram.com/a2skylinexc/"><strong>Instagram</strong></a>
        </p>
    </footer>
    
    <!-- Floating Theme Toggle Button -->
    <div class="theme-toggle-container">
        <button class="toggle-arrow" onclick="toggleThemeOptions()">&#9650;</button>
         <div class="theme-options">
            <button onclick="setTheme('light')">Light</button>
            <button onclick="setTheme('dark')">Dark</button>
            <button onclick="setTheme('high-contrast')">High Contrast</button>
        </div>
    </div>

    <!-- JavaScript for theme toggling and lightbox functionality (New addition) -->
    <script>
    document.addEventListener("DOMContentLoaded", function() {
    const allLinks = document.querySelectorAll("a");
    const visitedLinksKey = "visitedLinks";
    const openTabsKey = "openTabsCount";

    // Retrieve the visited links from localStorage or initialize as an empty array
    let visitedLinks = JSON.parse(localStorage.getItem(visitedLinksKey)) || [];

    // Retrieve the open tabs count from localStorage or initialize to zero
    let openTabsCount = parseInt(localStorage.getItem(openTabsKey)) || 0;

    // Increment the open tabs count and update localStorage
    openTabsCount += 1;
    localStorage.setItem(openTabsKey, openTabsCount);

    // Function to mark visited links
    function markVisitedLinks() {
        allLinks.forEach(link => {
            if (visitedLinks.includes(link.href)) {
                link.style.color = "purple"; // Change to your preferred "active" color
            }
        });
    }

    // Call markVisitedLinks on page load to apply color to visited links
    markVisitedLinks();

    // Event listener to track link clicks and save to visited links
    allLinks.forEach(link => {
        link.addEventListener("click", function() {
            if (!visitedLinks.includes(link.href)) {
                visitedLinks.push(link.href);
                localStorage.setItem(visitedLinksKey, JSON.stringify(visitedLinks));
            }
        });
    });

    // Reset visited links if this is the first tab after all were closed
    if (openTabsCount === 1) {
        localStorage.removeItem(visitedLinksKey); // Clear the visited links
        visitedLinks = []; // Reset the local visitedLinks array
    }

    // Handle closing of the tab to decrease the open tab count
    window.addEventListener("beforeunload", function() {
        openTabsCount -= 1;
        if (openTabsCount <= 0) {
            // If this is the last tab, reset the visited links
            localStorage.removeItem(visitedLinksKey);
        }
        localStorage.setItem(openTabsKey, openTabsCount);
    });
});
        document.addEventListener("DOMContentLoaded", function() {
            const header = document.getElementById("header");
            const detailsElements = document.querySelectorAll("details");

            // Function to check if any dropdown is open
            function checkDropdowns() {
                const anyOpen = Array.from(detailsElements).some(details => details.open);
        
                // Toggle sticky class based on whether any dropdown is open
                if (anyOpen) {
                    header.classList.remove("sticky");
                } else {
                    header.classList.add("sticky");
                }
            }

            // Attach toggle event listeners to all dropdowns
            detailsElements.forEach(details => {
                details.addEventListener("toggle", checkDropdowns);
            });

            // Initial check on page load
            checkDropdowns();
        });
        
        document.addEventListener("DOMContentLoaded", function() {
    const detailsElements = document.querySelectorAll("details");
    const dropdownLinks = document.querySelectorAll(".dropdown-content a");

    // Function to close all dropdowns except the one containing the clicked link
    function closeOtherDropdowns(excludeElement) {
        detailsElements.forEach(details => {
            if (details !== excludeElement) {
                details.open = false; // Close each details element except the one clicked in
            }
        });
    }

    // Attach click event to each dropdown link
    dropdownLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            const parentDetails = link.closest("details"); // Find the closest details element (the dropdown that contains the clicked link)
            closeOtherDropdowns(parentDetails);
        });
    });
});
    
        function setTheme(theme) {
            document.body.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
        }
        
        // Load saved theme or apply the browser's default theme on first visit
        document.addEventListener("DOMContentLoaded", function () {
        const savedTheme = localStorage.getItem("theme");

        if (savedTheme) {
            setTheme(savedTheme); // Use saved theme if it exists
        } else {
        // Detect the browser's default theme
            const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
            setTheme(prefersDarkMode ? "dark" : "light");
            }
        });
        
        function toggleThemeOptions() {
            const themeOptions = document.querySelector('.theme-options');
            themeOptions.classList.toggle('active');
        }

        function openLightbox(imageSrc) {
            document.getElementById("lightbox-img").src = imageSrc;
            document.getElementById("lightbox").style.display = "flex";
        }

        function closeLightbox() {
            document.getElementById("lightbox").style.display = "none";
        }
    </script>
</body>
</html>
    '''

    # Write the generated HTML content to the specified output file
    with open(outfile, 'w', encoding='utf-8') as output:
        output.write(html_content)



def main():

   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()